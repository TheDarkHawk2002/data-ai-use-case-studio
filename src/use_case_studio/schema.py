"""Input parsing and validation for the use-case register."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = {
    "use_case_id", "title", "domain", "problem", "target_group",
    "monthly_cases", "minutes_saved_per_case", "automation_share",
    "impact_score", "data_readiness_score", "feasibility_score", "risk_score",
    "human_review", "data_sensitivity", "dependencies",
}


@dataclass(frozen=True)
class UseCase:
    use_case_id: str
    title: str
    domain: str
    problem: str
    target_group: str
    monthly_cases: int
    minutes_saved_per_case: float
    automation_share: float
    impact_score: int
    data_readiness_score: int
    feasibility_score: int
    risk_score: int
    human_review: bool
    data_sensitivity: str
    dependencies: str
    source_row: int


def _integer(row: dict[str, str], key: str, row_number: int, minimum: int = 0) -> int:
    try:
        value = int(row[key])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"row {row_number}: '{key}' must be a whole number") from exc
    if value < minimum:
        raise ValueError(f"row {row_number}: '{key}' must be at least {minimum}")
    return value


def _score(row: dict[str, str], key: str, row_number: int) -> int:
    value = _integer(row, key, row_number, 1)
    if value > 5:
        raise ValueError(f"row {row_number}: '{key}' must be between 1 and 5")
    return value


def read_use_cases(path: Path) -> list[UseCase]:
    """Read validated rows; fail with an actionable message for bad input."""
    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise ValueError(f"cannot open input file '{path}': {exc}") from exc

    with handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))

        result: list[UseCase] = []
        seen: set[str] = set()
        for row_number, raw in enumerate(reader, start=2):
            row = {key: (value or "").strip() for key, value in raw.items() if key}
            empty = [key for key in REQUIRED_COLUMNS if not row.get(key)]
            if empty:
                raise ValueError(f"row {row_number}: empty required fields: {', '.join(sorted(empty))}")
            case_id = row["use_case_id"]
            if case_id in seen:
                raise ValueError(f"row {row_number}: duplicate use_case_id '{case_id}'")
            seen.add(case_id)

            try:
                minutes = float(row["minutes_saved_per_case"])
                share = float(row["automation_share"])
            except ValueError as exc:
                raise ValueError(f"row {row_number}: minutes and automation share must be numeric") from exc
            if not math.isfinite(minutes) or minutes < 0:
                raise ValueError(f"row {row_number}: minutes_saved_per_case must be finite and non-negative")
            if not math.isfinite(share) or not 0 <= share <= 1:
                raise ValueError(f"row {row_number}: automation_share must be between 0 and 1")

            sensitivity = row["data_sensitivity"].lower()
            if sensitivity not in {"low", "medium", "high"}:
                raise ValueError(f"row {row_number}: data_sensitivity must be low, medium, or high")
            review = row["human_review"].lower()
            if review not in {"yes", "no"}:
                raise ValueError(f"row {row_number}: human_review must be yes or no")

            result.append(UseCase(
                use_case_id=case_id,
                title=row["title"],
                domain=row["domain"],
                problem=row["problem"],
                target_group=row["target_group"],
                monthly_cases=_integer(row, "monthly_cases", row_number),
                minutes_saved_per_case=minutes,
                automation_share=share,
                impact_score=_score(row, "impact_score", row_number),
                data_readiness_score=_score(row, "data_readiness_score", row_number),
                feasibility_score=_score(row, "feasibility_score", row_number),
                risk_score=_score(row, "risk_score", row_number),
                human_review=(review == "yes"),
                data_sensitivity=sensitivity,
                dependencies=row["dependencies"],
                source_row=row_number,
            ))
    if not result:
        raise ValueError("input contains no use-case rows")
    return result
