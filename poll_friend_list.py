import os, asyncio, hashlib, time
from typing import List, Optional
import httpx
from pydantic import BaseModel, field_validator

FRIEND_LIST_URL = os.getenv("FRIEND_LIST_URL", "https://r7host.com/friend_list.json")
DISCORD_WEBHOOK = os.getenv("WEBHOOK_FRIENDS", "https://discord.com/api/webhooks/XXXX/AAAA")
GUILD_NAME = os.getenv("GUILD_NAME", "Sua Guild")
WORLD_NAME = os.getenv("WORLD_NAME", "Seu Mundo")
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "60"))

class Player(BaseModel):
    name: str
    level: Optional[int] = None
    vocation: Optional[str] = None
    @field_validator("level", mode="before")
    @classmethod
    def parse_level(cls, v):
        if v is None or v == "":
            return None
        try:
            return int(str(v).strip())
        except Exception:
            return None

class FriendList(BaseModel):
    Players: List[Player]

def content_fingerprint(players: List[Player]) -> str:
    raw = "|".join(f"{p.name}#{p.level}#{p.vocation or ''}" for p in players)
    return hashlib.sha256(raw.encode()).hexdigest()

def players_to_embed_fields(players: List[Player]):
    if not players:
        return [{"name": "Amigos", "value": "_(vazio)_", "inline": False}]
    lines = []
    for p in players[:50]:
        bits = [f"**{p.name}**"]
        if p.level is not None:
            bits.append(f"Lv {p.level}")
        if p.vocation:
            bits.append(p.vocation)
        lines.append(" — ".join(bits))
    if len(players) > 50:
        lines.append(f"… +{len(players)-50} nomes")
    return [{"name": "Amigos", "value": "\n".join(lines), "inline": False}]

def build_discord_embed(players: List[Player]):
    return {
        "title": "Lista de Amigos",
        "footer": {"text": f"{GUILD_NAME} • {WORLD_NAME}"},
        "fields": players_to_embed_fields(players),
        "timestamp": None,
    }

async def post_discord(webhook: str, embeds: list):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(webhook, json={"content": "", "embeds": embeds})
        r.raise_for_status()

async def main():
    etag: Optional[str] = None
    last_fp: Optional[str] = None
    print(f"[start] polling {FRIEND_LIST_URL} a cada {POLL_SECONDS}s")
    async with httpx.AsyncClient(timeout=15) as client:
        while True:
            try:
                headers = {}
                if etag:
                    headers["If-None-Match"] = etag
                resp = await client.get(FRIEND_LIST_URL, headers=headers)
                if resp.status_code == 304:
                    print(f"[{time.strftime('%H:%M:%S')}] 304 Not Modified")
                elif resp.status_code == 200:
                    etag = resp.headers.get("ETag", etag)
                    data = resp.json()
                    payload = FriendList(**data)
                    players = payload.Players
                    fp = content_fingerprint(players)
                    if fp != last_fp:
                        last_fp = fp
                        embeds = [build_discord_embed(players)]
                        await post_discord(DISCORD_WEBHOOK, embeds)
                        print(f"[{time.strftime('%H:%M:%S')}] publicado {len(players)} players no Discord")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] sem mudanças (hash igual)")
                else:
                    print(f"[warn] HTTP {resp.status_code} ao buscar friend_list")
            except Exception as e:
                print(f"[erro] {e}")
            await asyncio.sleep(POLL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[stop] encerrado pelo usuário")
