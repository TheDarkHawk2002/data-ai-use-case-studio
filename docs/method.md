# Assessment method

This prototype helps a team structure early discovery. It does not make an investment, employment, legal, or deployment decision.

## Inputs

Each record describes a problem, target group, estimated monthly volume, estimated minutes saved, assumed automation share, four 1–5 ratings, data sensitivity, a human-review choice, and dependencies. The ratings are explicit assumptions supplied by the team. They are not inferred from a model.

## Prioritization

The score is a weighted mean of normalized 1–5 ratings, rescaled to 0–100:

- Expected impact: 30%
- Data readiness: 25%
- Feasibility: 25%
- Inverse risk rating: 20%

The labels (prioritize discovery, validate, explore, defer) suggest what conversation to have next. They do not mean “build” or “do not build.”

## Indicative time estimate

`monthly volume × minutes saved × automation share × 12 ÷ 60`

This value excludes exceptions, adoption, training, costs, and changes in quality. It should be replaced or supplemented by measured evidence before a business case is made.

## Review signals

High sensitivity or a high input risk rating raises a review signal. The signal is a prompt to check data access, user impact, oversight, and applicable internal policies with the appropriate people. It is not a statutory risk classification or a substitute for specialist review.

## Discovery checklist

1. Confirm the problem and current baseline with affected users.
2. Identify the data owner, data provenance, access constraints, and known quality gaps.
3. State what the proposed system may and may not decide.
4. Define human oversight, escalation, and a non-automated fallback.
5. Agree on measurable success criteria and stop conditions before a pilot.
6. Record assumptions, unresolved questions, and an accountable decision owner.
