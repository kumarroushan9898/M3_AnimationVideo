#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/TeX/texbin:$PATH"
if [[ -d "$PWD/.build/tex/TinyTeX/bin/universal-darwin" ]]; then
  export PATH="$PWD/.build/tex/TinyTeX/bin/universal-darwin:$PATH"
fi
project_python="${M3_PYTHON:-python3}"
"$project_python" -c 'import sys; print(sys.version); assert (3, 12) <= sys.version_info < (3, 15), "Use Python 3.12, 3.13 or 3.14."'
if [[ ! -x .venv/bin/python ]]; then
  "$project_python" -m venv .venv
fi
missing=()
for tool in ffmpeg ffprobe latex dvisvgm pkg-config; do
  command -v "$tool" >/dev/null || missing+=("$tool")
done
if (( ${#missing[@]} )); then
  printf 'Missing tools: %s\n' "${missing[*]}" >&2
  printf 'Install the macOS dependencies listed in README.md and rerun setup.\n' >&2
  exit 1
fi
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m unittest discover -s Tests -v
printf 'Run source .venv/bin/activate to use the project environment.\n'
