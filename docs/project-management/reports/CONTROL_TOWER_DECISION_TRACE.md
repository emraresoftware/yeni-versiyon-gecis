# Control Tower Decision Trace

This document defines the properties and rules for decision traces.

## Properties
- `TraceId`: Unique canonical ID (prefixed with `TRACE-`).
- `SnapshotId`: Snapshot GUID.
- `SnapshotSchemaVersion`: Schema version.
- `EvaluatedAt`: Date/time of evaluation.
- `RuleId` / `RuleVersion`: Originating rule metadata.
- `TriggeredConditions` / `RejectedConditions`: Condition execution traces.
- `EvidenceInputs` / `MetricInputs` / `StatusInputs`: Inputs evaluated.
- `DeterminismHash`: SHA/MD5 fingerprint of inputs and rules.

## Determinism
Traces exclude request-volatile timestamps and paths, ensuring that a run under a fixed clock and inputs produces a stable, deterministic hash.
