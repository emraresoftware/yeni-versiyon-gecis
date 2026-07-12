# Control Tower Executive Brief Contract

This document defines the properties and rules for executive briefs.

## Properties
- `BriefId`: Unique canonical ID (prefixed with `BRIEF-`).
- `Persona`: Visibility context.
- `Scope`: Scope parameters.
- `GeneratedAt`: Date/time of generation.
- `SnapshotId` / `SnapshotGeneratedAt`: Snapshot source details.
- `TopPriorities`: Collection of sorted high-priority decisions.
- `ContentHash`: MD5/SHA summary hash.

## Stable Tie-Breaking Rules
Top priorities are ordered deterministically using the following stable tie-breaking rules:
1. `PriorityScore` descending
2. `Severity` descending
3. `CreatedAt` ascending
4. `DecisionId` ascending
