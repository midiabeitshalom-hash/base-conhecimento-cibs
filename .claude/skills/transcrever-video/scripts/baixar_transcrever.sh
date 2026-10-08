#!/bin/bash
# Baixa um vídeo (yt-dlp), extrai áudio (ffmpeg) e transcreve (whisper.cpp).
# NÃO apaga o vídeo/áudio — isso é feito por limpar.sh, depois de qualquer
# checagem visual (frame) que ainda seja necessária.
#
# Uso: baixar_transcrever.sh <url> [pasta_de_trabalho] [idioma]
set -e

URL="$1"
WORKDIR="${2:-$(mktemp -d "${TMPDIR:-/tmp}/transcricao.XXXXXX")}"
LANG="${3:-pt}"

if [ -z "$URL" ]; then
  echo "Uso: baixar_transcrever.sh <url> [pasta_de_trabalho] [idioma]" >&2
  exit 1
fi

MODEL="${WHISPER_MODEL:-$HOME/whisper-models/ggml-large-v3-turbo-q8_0.bin}"
if [ ! -f "$MODEL" ]; then
  echo "Modelo do Whisper não encontrado em: $MODEL" >&2
  echo "Ajuste a variável de ambiente WHISPER_MODEL ou baixe o modelo pra esse caminho." >&2
  exit 1
fi

for cmd in yt-dlp ffmpeg whisper-cli; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Comando obrigatório não encontrado no PATH: $cmd" >&2; exit 1; }
done

mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "== Baixando vídeo =="
yt-dlp -o "video.%(ext)s" --write-info-json "$URL"

VIDEO_FILE=$(ls video.* 2>/dev/null | grep -v '\.info\.json$' | head -1)
if [ -z "$VIDEO_FILE" ] || [ ! -f "$VIDEO_FILE" ]; then
  echo "Download falhou — nenhum arquivo de vídeo encontrado em $WORKDIR." >&2
  exit 1
fi

echo "== Extraindo áudio =="
ffmpeg -y -i "$VIDEO_FILE" -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -loglevel error

echo "== Transcrevendo com Whisper (pode levar alguns segundos) =="
whisper-cli -m "$MODEL" -f audio.wav -l "$LANG" -otxt -osrt -of transcript 2>&1 | tail -8

echo "== Extraindo metadados =="
if [ -f video.info.json ]; then
  python3 - "video.info.json" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1]))
campos = ["uploader", "uploader_id", "like_count", "comment_count",
          "description", "upload_date", "duration"]
with open("metadata.txt", "w") as f:
    for c in campos:
        f.write(f"{c}: {d.get(c)}\n")
PYEOF
fi

DUR=$(ffprobe -v quiet -print_format json -show_format "$VIDEO_FILE" 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['format'].get('duration','?'))" 2>/dev/null || echo "?")

echo
echo "== Pronto =="
echo "Pasta de trabalho: $WORKDIR"
echo "  transcript.txt / transcript.srt  → transcrição (com timestamps no .srt)"
echo "  metadata.txt                     → engajamento, autor, legenda do post"
echo "  video.info.json                  → metadados completos (raw)"
echo "  $VIDEO_FILE (duração: ${DUR}s) e audio.wav ainda estão aqui — NÃO apagados."
echo
echo "Se precisar conferir algo visual (texto na tela, gráfico, lista), extraia"
echo "frames de \"$VIDEO_FILE\" agora, antes de limpar."
echo "Quando terminar, rode: limpar.sh \"$WORKDIR\""
