"""Write reusable assessment artifacts as Markdown, JSON, and CSV."""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from .assessment import Assessment


def write_outputs(items: list[Assessment], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(items, output_dir / "assessment.json")
    _write_csv(items, output_dir / "assessment.csv")
    _write_markdown(items, output_dir / "decision-brief.md")


def _write_json(items: list[Assessment], path: Path) -> None:
    payload = {
        "method_version": "1.0",
        "disclaimer": "Screening estimates only; not a financial forecast, legal assessment, or deployment approval.",
        "use_cases": [item.as_dict() for item in items],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_csv(items: list[Assessment], path: Path) -> None:
    fields = [
        "rank", "use_case_id", "title", "domain", "priority_score", "recommendation",
        "review_level", "annual_hours_estimate", "impact_score", "data_readiness_score",
        "feasibility_score", "risk_score", "human_review", "dependencies",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for position, item in enumerate(items, start=1):
            row = item.as_dict()
            row["rank"] = position
            writer.writerow({key: row[key] for key in fields})


def _escape_cell(value: object) -> str:
    return html.escape(str(value).replace("\n", " "), quote=False).replace("|", "\\|")


def _write_markdown(items: list[Assessment], path: Path) -> None:
    lines = [
        "# Data and AI opportunity review",
        "",
        "This screening ranks candidate use cases for a structured discovery conversation. It does not approve implementation or establish a business case.",
        "",
        "## Ranked overview",
        "",
        "| Rank | Use case | Score | Indicative annual hours | Recommendation | Review signal |",
        "|---:|---|---:|---:|---|---|",
    ]
    for position, item in enumerate(items, start=1):
        row = item.use_case
        lines.append(
            f"| {position} | {_escape_cell(row.title)} | {item.priority_score:.1f}/100 | "
            f"{item.annual_hours_estimate:.1f} | {item.recommendation} | {item.review_level} |"
        )
    lines.extend([
        "",
        "## Assessment notes",
        "",
        "The annual-hours figure multiplies monthly volume, estimated minutes saved, an assumed automation share, and 12 months. It excludes adoption, exceptions, implementation cost, and changes in service quality.",
        "",
        "The priority score weights impact (30%), data readiness (25%), feasibility (25%), and inverse risk (20%). Ratings are stakeholder inputs on a 1–5 scale, not measured outcomes. Review signals are prompts for human discussion and are not legal or regulatory classifications.",
        "",
        "## Use-case details",
        "",
    ])
    for position, item in enumerate(items, start=1):
        row = item.use_case
        lines.extend([
            f"### {position}. {_escape_cell(row.title)} ({_escape_cell(row.use_case_id)})",
            "",
            f"**Domain:** {_escape_cell(row.domain)}  ",
            f"**Problem:** {_escape_cell(row.problem)}  ",
            f"**Target group:** {_escape_cell(row.target_group)}  ",
            f"**Dependencies to resolve:** {_escape_cell(row.dependencies)}  ",
            f"**Assessment:** {item.rationale}",
            "",
            "**Suggested next conversation:** confirm the baseline, inspect data quality and access, define a human-reviewed pilot, and agree on success and stop criteria.",
            "",
        ])
    lines.extend([
        "## Sample-data notice",
        "",
        "All included cases and values are synthetic examples. Replace them with stakeholder-validated assumptions before using this framework in a real decision.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
