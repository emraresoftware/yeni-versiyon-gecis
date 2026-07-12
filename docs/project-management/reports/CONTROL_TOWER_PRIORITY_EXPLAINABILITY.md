# Control Tower Priority Explainability

Every scored decision contains a detailed trace containing structured inputs, calculated weights, and override records to ensure absolute transparency.

## Explanation Layout

The engine generates a human-readable summary inside `PriorityBreakdownContract.Explanation` matching the following schema:

```text
Priority Score: [Final Score]
- Weighted Subtotal: [Subtotal value]
- Mitigation Progress: [Mitigation reduction]% reduction
- Applied Overrides: [Override policies triggered] (optional)
- Confidence: [Confidence score]
- Formula Version: [Formula ID and Version]
```

## Trace Fields
- `TriggeredConditions`: Specific rule predicates matched.
- `RejectedConditions`: Predicates bypassed.
- `EvidenceInputs`: Exact references backing the score.
- `DeterminismHash`: An MD5-based signature that verifies idempotency of the evaluation.
