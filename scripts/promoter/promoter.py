#!/usr/bin/env python3
import argparse
import filecmp
import os
import shutil
from dataclasses import dataclass
from typing import Dict, List, Optional

AREA_MAP = {
    "GOV": "01_GOVERNANCE",
    "ONB": "00_ONBOARDING",
    "CAL": "04_CALIBRATION",
    "AUD": "07_AUDIT",
    "LIC": "02_LICENSES",
    "FRE": "03_MODULES/FRE",
    "CPS": "03_MODULES/CPS",
    "PEPP": "03_MODULES/PEPP",
    "WAVNS": "03_MODULES/WAVNS",
    "AURA": "03_MODULES/AURA",
    "AIFC": "03_MODULES/AIFC",
    "SPF": "03_MODULES/SPF",
}

REQUIRED_CHECKS = ["04_CALIBRATION/cal_master.ics"]


@dataclass
class PromotionResult:
    promoted: List[str]
    conflicts: List[str]
    missing: List[str]


def parse_front_matter(path: str) -> Dict[str, str]:
    if not path.lower().endswith(".md"):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        lines = handle.readlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines) or lines[index].strip() != "<!--":
        return {}
    index += 1
    data: Dict[str, str] = {}
    while index < len(lines):
        line = lines[index].strip()
        if line == "-->":
            return data
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
        index += 1
    return data


def fallback_path(area: Optional[str], basename: str) -> str:
    if area and area in AREA_MAP:
        return os.path.join(AREA_MAP[area], basename)
    return os.path.join("07_AUDIT", "unmapped", basename)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def promote_file(src: str, dest: str, conflict_dir: str, results: PromotionResult) -> None:
    ensure_dir(os.path.dirname(dest))
    if os.path.exists(dest):
        same = filecmp.cmp(src, dest, shallow=False)
        if same:
            results.promoted.append(dest)
            return
        ensure_dir(conflict_dir)
        conflict_src = os.path.join(conflict_dir, f"source_{os.path.basename(src)}")
        conflict_dest = os.path.join(conflict_dir, f"dest_{os.path.basename(dest)}")
        shutil.copy2(src, conflict_src)
        shutil.copy2(dest, conflict_dest)
        results.conflicts.append(f"{src} -> {dest}")
        return
    shutil.copy2(src, dest)
    results.promoted.append(dest)


def check_required(root: str) -> List[str]:
    missing = []
    for path in REQUIRED_CHECKS:
        full_path = os.path.join(root, path)
        if not os.path.exists(full_path):
            missing.append(path)
    return missing


def write_report(root: str, date_str: str, results: PromotionResult) -> str:
    report_dir = os.path.join(root, "07_AUDIT", "promotion_reports")
    ensure_dir(report_dir)
    report_path = os.path.join(report_dir, f"promotion_report_{date_str}.md")
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write(f"# Promotion Report {date_str}\n\n")
        handle.write("## Promoted\n")
        if results.promoted:
            for item in results.promoted:
                handle.write(f"- {item}\n")
        else:
            handle.write("- none\n")
        handle.write("\n## Conflicts\n")
        if results.conflicts:
            for item in results.conflicts:
                handle.write(f"- {item}\n")
        else:
            handle.write("- none\n")
        handle.write("\n## Missing Required Artifacts\n")
        if results.missing:
            for item in results.missing:
                handle.write(f"- {item}\n")
        else:
            handle.write("- none\n")
    return report_path


def run_promotion(root: str, date_str: str) -> PromotionResult:
    inbox_dir = os.path.join(root, "INBOX", date_str)
    results = PromotionResult(promoted=[], conflicts=[], missing=check_required(root))
    if not os.path.isdir(inbox_dir):
        return results

    for term in sorted(os.listdir(inbox_dir)):
        term_dir = os.path.join(inbox_dir, term)
        if not os.path.isdir(term_dir):
            continue
        for entry in sorted(os.listdir(term_dir)):
            src = os.path.join(term_dir, entry)
            if not os.path.isfile(src):
                continue
            metadata = parse_front_matter(src)
            intended = metadata.get("intended_path")
            area = metadata.get("area")
            if intended:
                dest = os.path.join(root, intended)
            else:
                dest = os.path.join(root, fallback_path(area, os.path.basename(src)))
            conflict_dir = os.path.join(root, "07_AUDIT", "conflicts", date_str, term)
            promote_file(src, dest, conflict_dir, results)

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote INBOX drops into canonical folders.")
    parser.add_argument("--date", required=True, help="Date in YYYYMMDD format")
    parser.add_argument("--root", default=os.getcwd(), help="Repository root")
    args = parser.parse_args()

    results = run_promotion(args.root, args.date)
    write_report(args.root, args.date, results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
