#!/usr/bin/env bash
# Tests for skills/launch-kit/scripts/make-assets.sh. Run: bash tests/make-assets.test.sh
set -euo pipefail
script="$(cd "$(dirname "$0")/.." && pwd)/skills/launch-kit/scripts/make-assets.sh"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
fail=0
check() { if [[ "$2" == "$3" ]]; then echo "ok   $1"; else echo "FAIL $1: expected '$3', got '$2'"; fail=1; fi; }
dims() { magick identify -format '%wx%h' "$1"; }

magick -size 1024x1024 xc:none -fill '#3b82f6' -draw 'circle 512,512 512,100' "$tmp/icon.png"
magick -size 2000x1125 xc:'#222' "$tmp/cover.png"
magick -size 2304x934 xc:white "$tmp/wide.webp"
magick -size 640x812 xc:white "$tmp/tall.png"

"$script" --out "$tmp/out" --icon "$tmp/icon.png" --cover "$tmp/cover.png" "$tmp/wide.webp" "$tmp/tall.png" >/dev/null

check "icon is 512x512" "$(dims "$tmp/out/icon-512.png")" "512x512"
check "icon keeps transparency" "$(magick "$tmp/out/icon-512.png" -format '%[pixel:p{0,0}]' info:)" "srgba(0,0,0,0)"
check "dev.to cover is 1000x420" "$(dims "$tmp/out/cover-devto.png")" "1000x420"
check "hashnode cover is 1600x840" "$(dims "$tmp/out/cover-hashnode.png")" "1600x840"
check "wide gallery is 1270x760" "$(dims "$tmp/out/gallery-1.png")" "1270x760"
check "tall gallery is 1270x760" "$(dims "$tmp/out/gallery-2.png")" "1270x760"
check "webp screenshot becomes png" "$(magick identify -format '%m' "$tmp/out/screenshot-1.png")" "PNG"
check "screenshot keeps its size" "$(dims "$tmp/out/screenshot-1.png")" "2304x934"

set +e
"$script" --icon "$tmp/icon.png" >/dev/null 2>&1; check "missing --out exits 2" "$?" "2"
"$script" --out "$tmp/x" "$tmp/nope.png" >/dev/null 2>&1; check "missing input exits 2" "$?" "2"
set -e

exit $fail
