#!/bin/sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 /path/to/target-project [independent-verification|crosscheck]" >&2
  exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_dir=$(dirname -- "$script_dir")
skill_name=${2:-independent-verification}
case "$skill_name" in
  independent-verification) source_dir="$repo_dir/plugins/qa-agent/skills/independent-verification" ;;
  crosscheck)
    source_dir="$repo_dir/plugins/crosscheck/skills/crosscheck"
    for file in SKILL.md references/task-profiles.md references/evidence-bundle.md references/result-publication.md references/runtime-integration.md; do
      if [ ! -s "$source_dir/$file" ]; then
        echo "BLOCKED: managed Crosscheck skill source is incomplete; use a complete reviewed candidate package." >&2
        exit 2
      fi
    done
    ;;
  *) echo "Unknown skill name" >&2; exit 2 ;;
esac
target_project=$1
target_dir="$target_project/.claude/skills/$skill_name"

if [ ! -d "$target_project" ]; then
  echo "Target project does not exist: $target_project" >&2
  exit 1
fi

if [ -e "$target_dir" ] || [ -L "$target_dir" ]; then
  echo "Refusing to overwrite existing skill: $target_dir" >&2
  exit 1
fi

mkdir -p "$(dirname -- "$target_dir")"
cp -R "$source_dir" "$target_dir"
echo "Installed $skill_name in $target_dir"
