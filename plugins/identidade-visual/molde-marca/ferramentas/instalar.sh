#!/bin/bash
# Instala as ferramentas do fluxo identidade em ~/.cache/design-squad-identidade (sem sudo, sem Homebrew).
# Python: fonttools, uharfbuzz, pillow, pymupdf. Node: playwright (+ Chromium), ffmpeg-static.
set -e
F=${FERRAMENTAS:-$HOME/.cache/design-squad-identidade}
mkdir -p "$F"; cd "$F"
export PATH="$HOME/.local/node/bin:$HOME/.local/bin:$PATH"
command -v node >/dev/null || { echo "FALTA: node. Instale o Node oficial em ~/.local/node (sem sudo) e rode de novo."; exit 1; }
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q fonttools uharfbuzz pillow pymupdf
[ -f package.json ] || echo '{"name":"design-squad-identidade","private":true}' > package.json
npm install -s playwright ffmpeg-static >/dev/null
npx -y playwright install chromium >/dev/null
echo "ferramentas prontas em $F"
echo "python: $F/.venv/bin/python   node: FERRAMENTAS=$F node <script>"
