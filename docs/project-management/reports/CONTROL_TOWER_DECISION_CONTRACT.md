# Control Tower Decision Contract

This document defines the properties and validation rules for `DecisionContract`.

## Properties
- `DecisionId`: Unique canonical ID (prefixed with `DECISION-`).
- `RuleId`: Canonical ID of the rule that generated the decision.
- `Title` / `Description`: Text display values.
- `Category` / `Severity` / `Status`: Enums.
- `PriorityScore`: Score between 0 and 100.
- `Confidence`: Confidence value between 0 and 1.
- `Scope`: Scoping information (e.g. Workspace, Module).
- `AffectedSubjects`: Subject references.
- `Owners`: List of technical/business owners.
- `Evidence`: Supporting evidence list.
- `RecommendedActions`: Associated actions.
- `Trace`: Explanation trace mapping.

## Validation Rules
1. Title must not be empty.
2. PriorityScore must be in the range [0, 100].
3. Confidence must be in the range [0.0, 1.0].
4. Active decisions must have evidence unless explicitly marked "Unverified".
