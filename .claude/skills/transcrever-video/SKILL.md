---
name: transcrever-video
description: Baixa um vídeo de um link (Instagram, TikTok, YouTube etc. via yt-dlp), transcreve com Whisper (whisper.cpp local), documenta a transcrição + metadados, e apaga o vídeo/áudio baixado logo em seguida pra não pesar a máquina. Use quando o Mike mandar um link de vídeo pra transcrever, resumir ou analisar — em qualquer projeto.
---

# /transcrever-video

Fluxo pra transcrever vídeo de link: baixar → transcrever → documentar →
apagar mídia. Dois scripts, não um só — porque às vezes é preciso conferir
algo visual (texto na tela, gráfico, lista) antes de apagar o vídeo, e um
script único que apaga tudo de cara elimina essa chance.

## Passo a passo

1. **Baixar + transcrever:**
   ```
   .claude/skills/transcrever-video/scripts/baixar_transcrever.sh "<url>" [pasta_de_trabalho] [idioma]
   ```
   - `pasta_de_trabalho` é opcional — se omitida, cria uma pasta temporária
     e imprime o caminho.
   - `idioma` é opcional — padrão `pt`.
   - Gera na pasta: `transcript.txt`, `transcript.srt` (com timestamps),
     `metadata.txt` (engajamento, autor, legenda do post), `video.info.json`
     (metadados completos), e o vídeo + `audio.wav` (ainda não apagados).

2. **Ler a transcrição** (`transcript.srt` pros timestamps, `transcript.txt`
   pro texto corrido) e o `metadata.txt`.

3. **Se o conteúdo depender de algo visual** (a fala menciona "isso aqui",
   lista mostrada só em texto na tela, gráfico, etc.) — extrair frame(s) do
   arquivo de vídeo agora, com `ffmpeg`, antes do próximo passo. Se o áudio
   já é autossuficiente, pular direto pro passo 4.

4. **Limpar a mídia:**
   ```
   .claude/skills/transcrever-video/scripts/limpar.sh "<pasta_de_trabalho>"
   ```
   Apaga só o vídeo e o `audio.wav` — preserva transcrição, metadados e
   qualquer frame extraído no passo 3.

5. **Documentar o resultado** — depende do que foi pedido e de onde
   estamos trabalhando:
   - Se for só "transcreve esse vídeo pra mim" → mostrar a transcrição
     direto no chat, sem salvar nada em arquivo.
   - Se o projeto atual já tiver uma convenção própria de biblioteca/base
     de conhecimento (ex: um `indice.md` ou `CLAUDE.md` explicando como
     documentar conteúdo analisado) → seguir essa convenção do projeto.
   - Em qualquer outro contexto → perguntar onde documentar, se não
     estiver óbvio pelo pedido.

## Requisitos (verificar uma vez por máquina)

`yt-dlp`, `ffmpeg`, `whisper-cli` (via `brew install whisper-cpp`) no PATH,
e um modelo do Whisper em `~/whisper-models/ggml-large-v3-turbo-q8_0.bin`
(ajustável pela variável de ambiente `WHISPER_MODEL`). Se algo estiver
faltando, o script avisa o quê e para — não segue com transcrição
incompleta.

## Erros comuns

- **yt-dlp falha em post do Instagram** → o post pode estar indisponível,
  privado ou o link corrompido. Confirmar abrindo o link direto no
  navegador antes de insistir no download.
- **Vídeo mais longo (> 1min)** → mesmo fluxo, só demora mais na
  transcrição — não precisa de ajuste.
