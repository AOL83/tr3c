#!/usr/bin/env bash
set -euo pipefail

term_input="${1:-${TERM:-${TR3C_TERM:-}}}"
if [ -z "$term_input" ]; then
  echo "Usage: $0 T03" >&2
  exit 1
fi

if ! echo "$term_input" | grep -Eq '^T0[1-8]$'; then
  echo "Invalid terminal. Use T01 to T08." >&2
  exit 1
fi

date_str=$(date +%Y%m%d)
root_dir=$(pwd)

drop_dir="$root_dir/INBOX/$date_str/$term_input"
mkdir -p "$drop_dir"

manifest_src="$root_dir/06_TEMPLATES/manifest_template.md"
manifest_dst="$drop_dir/manifest_${date_str}_${term_input}.md"

sed "s/{{DATE}}/${date_str}/g; s/{{TERM}}/${term_input}/g" "$manifest_src" > "$manifest_dst"

echo "Created: $drop_dir"
echo "Manifest: $manifest_dst"
echo "Reminder: use filename pattern YYYYMMDD_${term_input}_AREA_TYPE_slug_vMAJOR.MINOR.ext"
