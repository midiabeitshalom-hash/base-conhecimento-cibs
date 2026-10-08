#!/bin/bash
# Apaga só o vídeo e o áudio baixados por baixar_transcrever.sh — preserva
# transcrição, metadados e qualquer frame/imagem que tenha sido extraído.
#
# Uso: limpar.sh <pasta_de_trabalho>
set -e

WORKDIR="$1"
if [ -z "$WORKDIR" ] || [ ! -d "$WORKDIR" ]; then
  echo "Uso: limpar.sh <pasta_de_trabalho>" >&2
  exit 1
fi

cd "$WORKDIR"
APAGADOS=""

for f in video.*; do
  [ -f "$f" ] || continue
  case "$f" in
    *.info.json) continue ;;
  esac
  rm -f "$f"
  APAGADOS="$APAGADOS $f"
done

if [ -f audio.wav ]; then
  rm -f audio.wav
  APAGADOS="$APAGADOS audio.wav"
fi

if [ -z "$APAGADOS" ]; then
  echo "Nada pra apagar em $WORKDIR (vídeo/áudio já não estavam aqui)."
else
  echo "Apagados:$APAGADOS"
fi

echo
echo "Ficou em $WORKDIR:"
ls -la "$WORKDIR"
