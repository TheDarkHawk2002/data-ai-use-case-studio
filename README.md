# Data & AI Use Case Studio

Data & AI Use Case Studio is a small, explainable decision-support tool for organizing early conversations about data and AI opportunities. It turns a structured register into a ranked overview and a reusable decision brief. The included cases and all numeric inputs are synthetic.

The prototype demonstrates practical Python, data validation, transparent scoring, risk and safeguard prompts, CSV/JSON/Markdown output, and communication of assumptions. It is deliberately domain-neutral so the same approach can support discovery work across public services, operations, and customer-facing teams.

## What it does

- Validates required fields, duplicate IDs, rating ranges, numeric assumptions, sensitivity labels, and human-review choices.
- Ranks use cases with an explicit weighted score: impact 30%, data readiness 25%, feasibility 25%, and inverse risk 20%.
- Calculates an indicative annual time-saving estimate from volume, minutes saved, and an assumed automation share.
- Emits a CSV for further analysis, JSON for integration, and a Markdown brief for stakeholder discussion.
- Flags higher review needs when the supplied sensitivity or risk rating warrants a conversation.
- Uses Python's standard library only; no private data or external AI API is required.

## Run it

Python 3.11 or later is required.

```powershell
python -m pip install -e .
usecase-studio --input data/sample_use_cases.csv --output-dir output
```

Or run the module without installing the console command:

```powershell
$env:PYTHONPATH = "src"
python -m use_case_studio --input data/sample_use_cases.csv --output-dir output
```

The output directory contains `decision-brief.md`, `assessment.csv`, and `assessment.json`. Generated output is excluded from version control.

The `examples/` folder contains a committed run of the included synthetic sample, so reviewers can inspect the decision brief and structured outputs without installing the package.

## Input contract

The CSV must include the columns in `data/sample_use_cases.csv`. Rating inputs use a 1–5 scale. `automation_share` is a decimal from 0 to 1. `human_review` accepts `yes` or `no`, and `data_sensitivity` accepts `low`, `medium`, or `high`. The CLI stops with a row-specific message if required values or ranges are invalid.

## How to read the results

The score is a prioritization aid for discovery, not a prediction of project success. Annual hours are an illustrative calculation, not a financial or staffing forecast. The prototype does not account for implementation cost, adoption, edge cases, service quality, or uncertainty ranges. Risk and sensitivity signals are prompts for a qualified human review; they are not legal classifications or deployment approval.

## Project structure

```text
data/                 synthetic input register
docs/                 method and case-study notes
examples/             generated sample artifacts
src/use_case_studio/  validation, assessment, reporting, CLI
```

## Next improvements

1. Add scenario ranges and confidence notes for uncertain assumptions.
2. Add stakeholder sign-off and versioned assessment history.
3. Add a simple dashboard once a real user need and data boundary are defined.
4. Add automated tests for input boundaries, ranking ties, and report escaping.

## License

MIT. See `LICENSE`.

