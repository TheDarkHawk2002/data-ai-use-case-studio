"""Explainable prioritization calculations and review signals."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .schema import UseCase


@dataclass(frozen=True)
class Assessment:
    use_case: UseCase
    annual_hours_estimate: float
    priority_score: float
    recommendation: str
    review_level: str
    rationale: str

    def as_dict(self) -> dict[str, object]:
        data = asdict(self.use_case)
        data.update({
            "annual_hours_estimate": self.annual_hours_estimate,
            "priority_score": self.priority_score,
            "recommendation": self.recommendation,
            "review_level": self.review_level,
            "rationale": self.rationale,
        })
        return data


def assess(use_case: UseCase) -> Assessment:
    """Calculate a screening score; this is not an ROI or compliance decision."""
    score = 20 * (
        0.30 * use_case.impact_score
        + 0.25 * use_case.data_readiness_score
        + 0.25 * use_case.feasibility_score
        + 0.20 * (6 - use_case.risk_score)
    )
    annual_hours = (
        use_case.monthly_cases
        * use_case.minutes_saved_per_case
        * use_case.automation_share
        * 12
        / 60
    )
    if score >= 80:
        recommendation = "Prioritize discovery"
    elif score >= 65:
        recommendation = "Validate with a small pilot"
    elif score >= 50:
        recommendation = "Explore after key dependencies"
    else:
        recommendation = "Defer and revisit"

    if use_case.data_sensitivity == "high" or use_case.risk_score >= 4:
        review_level = "High review need"
    elif use_case.data_sensitivity == "medium" or use_case.risk_score == 3:
        review_level = "Review safeguards"
    else:
        review_level = "Initial review"

    rationale = (
        f"Impact {use_case.impact_score}/5; data readiness {use_case.data_readiness_score}/5; "
        f"feasibility {use_case.feasibility_score}/5; risk {use_case.risk_score}/5. "
        f"Human review {'is' if use_case.human_review else 'is not'} included in the proposal."
    )
    return Assessment(use_case, round(annual_hours, 1), round(score, 1), recommendation, review_level, rationale)


def rank(use_cases: list[UseCase]) -> list[Assessment]:
    return sorted((assess(item) for item in use_cases), key=lambda item: (-item.priority_score, item.use_case.use_case_id))
