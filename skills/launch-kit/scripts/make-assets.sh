#!/usr/bin/env bash
# Generates the launch image set with ImageMagick.
# Usage: make-assets.sh --out DIR [--icon FILE] [--cover FILE] [--bg COLOR] [SCREENSHOT...]
#   --icon   square source, ideally 1024px with transparency  -> icon-512.png
#   --cover  wide source image                                 -> cover-devto.png (1000x420), cover-hashnode.png (1600x840)
#   SCREENSHOT files, in display order                         -> screenshot-N.png (PNG copy), gallery-N.png (1270x760, padded)
set -euo pipefail

out="" icon="" cover="" bg="#16171b"
shots=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) out="$2"; shift 2 ;;
    --icon) icon="$2"; shift 2 ;;
    --cover) cover="$2"; shift 2 ;;
    --bg) bg="$2"; shift 2 ;;
    -h|--help) sed -n '2,6p' "$0"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) shots+=("$1"); shift ;;
  esac
done

if [[ -z "$out" ]]; then echo "--out is required" >&2; exit 2; fi
if ! command -v magick >/dev/null; then echo "ImageMagick 7 (magick) is required" >&2; exit 3; fi
for f in "$icon" "$cover" "${shots[@]+"${shots[@]}"}"; do
  if [[ -n "$f" && ! -f "$f" ]]; then echo "not found: $f" >&2; exit 2; fi
done
mkdir -p "$out"

if [[ -n "$icon" ]]; then
  magick "$icon" -background none -resize 512x512 -gravity center -extent 512x512 "$out/icon-512.png"
  echo "$out/icon-512.png"
fi

if [[ -n "$cover" ]]; then
  magick "$cover" -resize '1000x420^' -gravity center -extent 1000x420 "$out/cover-devto.png"
  magick "$cover" -resize '1600x840^' -gravity center -extent 1600x840 "$out/cover-hashnode.png"
  echo "$out/cover-devto.png"
  echo "$out/cover-hashnode.png"
fi

i=1
for s in "${shots[@]+"${shots[@]}"}"; do
  magick "$s" "$out/screenshot-$i.png"
  magick "$s" -resize 1190x700 -background "$bg" -gravity center -extent 1270x760 "$out/gallery-$i.png"
  echo "$out/screenshot-$i.png"
  echo "$out/gallery-$i.png"
  i=$((i + 1))
done
