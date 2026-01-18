#!/usr/bin/env python3
import os
import subprocess
import sys
from typing import Iterable

TEXT_EXTENSIONS = {".md", ".txt", ".yml", ".yaml", ".sh", ".py", ".csv", ".ics"}


def get_paths_from_git() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        check=False,
        capture_output=True,
        text=True,
    )
    paths = [p for p in result.stdout.splitlines() if p.strip()]
    return paths


def iter_text_files(paths: Iterable[str]) -> Iterable[str]:
    for path in paths:
        if not path or not os.path.exists(path):
            continue
        if os.path.isdir(path):
            continue
        _, ext = os.path.splitext(path)
        if ext.lower() in TEXT_EXTENSIONS:
            yield path


def has_non_ascii_bytes(path: str) -> bool:
    with open(path, "rb") as handle:
        data = handle.read()
    return any(byte > 0x7F for byte in data)


def main() -> int:
    paths = sys.argv[1:]
    if not paths:
        paths = get_paths_from_git()
    errors = []
    for path in iter_text_files(paths):
        if has_non_ascii_bytes(path):
            errors.append(path)
    if errors:
        print("ASCII lint failed. Non-ASCII bytes found in:")
        for path in errors:
            print(f"- {path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
