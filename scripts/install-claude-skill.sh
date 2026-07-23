#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/target-project" >&2
  exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_dir=$(dirname -- "$script_dir")
source_dir="$repo_dir/plugins/qa-agent/skills/independent-verification"
target_project=$1
target_dir="$target_project/.claude/skills/independent-verification"

if [ ! -d "$target_project" ]; then
  echo "Target project does not exist: $target_project" >&2
  exit 1
fi

if [ -e "$target_dir" ]; then
  echo "Refusing to overwrite existing skill: $target_dir" >&2
  exit 1
fi

mkdir -p "$(dirname -- "$target_dir")"
cp -R "$source_dir" "$target_dir"
echo "Installed independent-verification in $target_dir"
