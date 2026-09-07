#!/bin/sh
set -eu
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 NEW_VENV [crosscheck|final-boss|independent-verification|independent-qa-agent|qa-agent|workboard-qa-agent]" >&2
  exit 2
fi
case "${2:-crosscheck}" in
  crosscheck|final-boss|independent-verification|independent-qa-agent|qa-agent|workboard-qa-agent) ;;
  *) echo "Unknown compatibility name" >&2; exit 2 ;;
esac
if [ -e "$1" ] || [ -L "$1" ]; then
  echo "Refusing to overwrite an existing environment" >&2
  exit 1
fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 -m venv "$1"
"$1/bin/python" -m pip install "$(dirname -- "$script_dir")"
"$1/bin/crosscheck" --help
