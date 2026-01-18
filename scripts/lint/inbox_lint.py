#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from typing import Iterable, Tuple

INBOX_PATTERN = re.compile(r"^INBOX/[0-9]{8}/T0[1-8]/")
BASENAME_PATTERN = re.compile(
    r"^[0-9]{8}_T0[1-8]_[A-Z]+_[A-Z]+_[a-z0-9_-]+_v[0-9]+\.[0-9]+\.[a-z0-9]+$"
)
REQUIRED_KEYS = [
    "tr3c_terminal",
    "area",
    "type",
    "version",
    "status",
    "intended_path",
    "source_inputs",
]


def get_paths_from_git() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        check=False,
        capture_output=True,
        text=True,
    )
    return [p for p in result.stdout.splitlines() if p.strip()]


def iter_files(paths: Iterable[str]) -> Iterable[str]:
    for path in paths:
        if not path or not os.path.exists(path):
            continue
        if os.path.isdir(path):
            continue
        yield path


def read_front_matter(path: str) -> Tuple[bool, str]:
    with open(path, "r", encoding="utf-8") as handle:
        lines = handle.readlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines) or lines[index].strip() != "<!--":
        return False, ""
    index += 1
    block_lines = []
    while index < len(lines):
        line = lines[index]
        if line.strip() == "-->":
            return True, "".join(block_lines)
        block_lines.append(line)
        index += 1
    return False, ""


def check_required_keys(block: str) -> list[str]:
    missing = []
    for key in REQUIRED_KEYS:
        if f"{key}:" not in block:
            missing.append(key)
    return missing


def main() -> int:
    paths = sys.argv[1:]
    if not paths:
        paths = get_paths_from_git()

    maintainer_override = os.environ.get("TR3C_MAINTAINER", "").lower() in {"1", "true", "yes"}

    errors = []

    for path in iter_files(paths):
        if not maintainer_override and not INBOX_PATTERN.match(path):
            errors.append(f"Non-INBOX change detected: {path}")
            continue

        if not path.startswith("INBOX/"):
            continue

        basename = os.path.basename(path)
        if not BASENAME_PATTERN.match(basename):
            errors.append(f"Invalid filename: {path}")
            continue

        _, ext = os.path.splitext(basename)
        if ext.lower() == ".md":
            has_front_matter, block = read_front_matter(path)
            if not has_front_matter:
                errors.append(f"Missing front-matter block: {path}")
                continue
            missing = check_required_keys(block)
            if missing:
                errors.append(f"Missing keys in front-matter for {path}: {', '.join(missing)}")

    if errors:
        print("INBOX lint failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
