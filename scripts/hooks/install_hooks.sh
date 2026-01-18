#!/usr/bin/env bash
set -euo pipefail

root_dir=$(pwd)
install_path="$root_dir/.git/hooks/pre-commit"

cp "$root_dir/scripts/hooks/pre-commit" "$install_path"
chmod +x "$install_path"

echo "Installed pre-commit hook to $install_path"
