# TS3 Discord Bot (Railway-ready)

Bot que faz polling de uma URL JSON com lista de amigos e envia para um webhook do Discord.

## Deploy na Railway

1. Crie um novo projeto e selecione este repositório.
2. Em **Variables**, adicione:
   - `FRIEND_LIST_URL` (ex: https://r7host.com/friend_list.json)
   - `WEBHOOK_FRIENDS` (seu webhook do Discord)
   - `GUILD_NAME` (ex: Guardians)
   - `WORLD_NAME` (ex: Pacera)
   - `POLL_SECONDS` (opcional, ex: 60)
3. Railway detecta Python automaticamente. Este repositório inclui:
   - `main.py` (entrypoint)
   - `Procfile` (comando de start)
   - `railway.toml` (fallback do start command)

Se preferir, nas **Service Settings** da Railway, defina manualmente o Start Command para:
```
python -u poll_friend_list.py
```

## Execução local
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' .env.example | xargs)  # opcional
python -u poll_friend_list.py
```
