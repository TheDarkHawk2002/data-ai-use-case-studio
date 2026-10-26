"""Command-line interface for a transparent data and AI use-case screen."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .assessment import rank
from .outputs import write_outputs
from .schema import read_use_cases


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="usecase-studio",
        description="Screen a synthetic or stakeholder-provided use-case CSV and create a decision brief.",
    )
    parser.add_argument("--input", type=Path, required=True, help="Path to the use-case register CSV")
    parser.add_argument("--output-dir", type=Path, default=Path("output"), help="Directory for generated artifacts")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        cases = read_use_cases(args.input)
        assessments = rank(cases)
        write_outputs(assessments, args.output_dir)
    except (OSError, ValueError) as exc:
        print(f"usecase-studio: {exc}", file=sys.stderr)
        return 2
    print(f"Assessed {len(assessments)} use cases. Outputs written to {args.output_dir.resolve()}")
    return 0
