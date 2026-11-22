"""Command-line interface for Klipper Log Doctor."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .analyzer import analyze_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="klipper-log-doctor",
        description="Analyze a Klipper log locally without changing printer files.",
    )
    parser.add_argument("logfile", type=Path, help="Path to klippy.log")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.logfile.is_file():
        print(f"Error: file not found: {args.logfile}", file=sys.stderr)
        return 2

    try:
        findings = analyze_file(args.logfile)
    except OSError as exc:
        print(f"Error reading log file: {exc}", file=sys.stderr)
        return 2

    if not findings:
        print("No known issues detected.")
        print("This does not guarantee that the printer is problem-free.")
        return 0

    print(f"Found {len(findings)} matching log message(s):\n")
    for finding in findings:
        print(f"[{finding.severity.upper()}] {finding.title} ({finding.rule_id})")
        print(f"Line {finding.line_number}: {finding.matched_text}")
        print(f"What it may mean: {finding.explanation}")
        print("Suggested checks:")
        for step in finding.next_steps:
            print(f"  - {step}")
        print()

    print("These are diagnostic hints, not a definitive diagnosis.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
