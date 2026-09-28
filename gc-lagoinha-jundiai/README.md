# Encontre seu GC · Lagoinha Jundiaí

Site estático para **gc.lagoinhajundiai.com.br**. A pessoa digita o endereço ou CEP (ou usa a localização do celular), vê os três GCs mais próximos e fala com o líder pelo WhatsApp. Os dados vêm direto da planilha do Google Sheets: quando alguém atualiza a planilha, o site acompanha.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `index.html` | O site inteiro (visual e código num arquivo só) |
| `config.js` | Chave do Mapbox (não vai para o GitHub; envie para a hospedagem) |
| `gcs-backup.csv` | Cópia da planilha, usada se o Google estiver fora do ar |
| `logo.png` | *(opcional)* Envie o logo da igreja com esse nome. Se não houver, aparece um “L” |

## 1. Ligar a planilha ao site

1. Abra a planilha no Google Sheets.
2. **Arquivo → Compartilhar → Publicar na Web**.
3. Em “Link”, escolha a aba **Página1** e o formato **Valores separados por vírgula (.csv)** → **Publicar**.
4. Copie o link gerado (termina em `output=csv`).
5. No `index.html`, cole o link em `SHEET_CSV_URL`:

```js
SHEET_CSV_URL: 'https://docs.google.com/spreadsheets/d/e/XXXX/pub?gid=0&single=true&output=csv',
```

O Google leva até 5 minutos para refletir uma alteração no link publicado.

## 2. Colunas que o site lê

O cabeçalho pode estar em qualquer linha. O site procura pelo nome da coluna:

`QTD · DIA · HORARIO · LOCAL · MINISTERIAL · CONTATO LIDERES · ENDEREÇO · COORDENADOR`

- **DIA**: `TERÇA`, `QUINTA`, `SABADO`… (com ou sem acento)
- **HORARIO**: `20H`, `19H30` ou `19:30`
- **LOCAL**: o bairro vira o nome do GC (`MEDEIROS` → *GC Medeiros*). `ONLINE` marca o GC como online. `IGREJA` vira *GC na Igreja*. Cidade depois de hífen (`JARDIM PEROLA - ITUPEVA`) é reconhecida.
- **CONTATO LIDERES**: nome e telefone juntos, do jeito que já está (`VAVA 1199815-7587 GRACIELE 1198347-5457`). O botão de WhatsApp vai para o primeiro telefone.

Colunas opcionais que você pode criar:

- **LAT** e **LNG**: coordenadas do GC (veja o passo 3).
- **ATIVO**: escreva `NÃO` para esconder um GC sem apagar a linha.

## 3. Deixar a busca instantânea (recomendado, uma vez só)

Sem coordenadas, o site localiza cada endereço no mapa na hora da busca. Funciona, mas a primeira busca de cada visitante demora alguns segundos. Para resolver:

1. Crie duas colunas no fim da planilha: **LAT** e **LNG**.
2. Abra `gc.lagoinhajundiai.com.br/?admin`.
3. Confira os pontos no mapa (link “ver” em cada linha). Onde aparecer *aprox.*, o endereço não foi achado e foi usado o centro do bairro.
4. Clique em **Copiar LAT/LNG** e cole na célula LAT do primeiro GC.

Quando cadastrar um GC novo, repita o processo ou preencha só a linha nova. Para pegar a coordenada no Google Maps, clique com o botão direito no local e copie os números.

## 4. Publicar na hospedagem

Envie `index.html`, `config.js`, `gcs-backup.csv` e `logo.png` para a pasta raiz do subdomínio `gc.lagoinhajundiai.com.br` (FTP ou gerenciador de arquivos do painel). Não precisa de banco de dados, PHP ou build.

O subdomínio precisa de **HTTPS** (SSL ativo). Sem ele, o navegador bloqueia o botão “Usar minha localização”.

## Outros ajustes no `CONFIG` (topo do script)

- `MOSTRAR_ENDERECO: false`: mostra só bairro e cidade. O endereço completo passa a ser dado pelo líder no WhatsApp. Pense nisso, porque são casas de famílias com o telefone ao lado.
- `MENSAGEM_WHATSAPP`: texto que já vem escrito quando a pessoa abre o WhatsApp.

## Mapbox

A busca de quem visita o site usa o **Mapbox**: sugere endereços enquanto a pessoa digita e localiza com mais precisão. A chave fica no arquivo `config.js` (modelo em `config.example.js`). Ele fica fora do GitHub, que bloqueia chaves no código, mas **precisa ser enviado para a hospedagem** junto com o `index.html`.

1. No painel do Mapbox, em **Tokens**, edite a chave e, em **URL restrictions**, adicione `https://gc.lagoinhajundiai.com.br`. Assim ninguém consegue usar a chave em outro site.
2. A busca é temporária: nada do Mapbox é salvo. Por isso as coordenadas dos GCs (colunas LAT/LNG) continuam vindo do OpenStreetMap ou do Google Maps, como no passo 3. Os termos do Mapbox não permitem guardar resultados do plano gratuito.
3. Se o Mapbox falhar ou a chave for removida, o site volta sozinho para o OpenStreetMap.

## Serviços externos

- **Mapbox**: busca e sugestões do endereço do visitante.
- **Photon / OpenStreetMap**: localiza os GCs sem LAT/LNG e serve de reserva (com Nominatim).
- **ViaCEP**: quando a pessoa digita só o CEP.
- **Google Fonts**: tipografia (Sora e Plus Jakarta Sans).
