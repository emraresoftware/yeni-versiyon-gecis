# Control Tower Evidence Mapping

This document describes how raw observation metrics translate to verified state evidence logs.

## Observation Types Mappings

| Source Type | Evidence reference | Verification criteria | State output |
|---|---|---|---|
| **Local Git** | Commit SHA / Branch | Process exit code = 0 | Mapped to `RepositoryDetailSnapshot` |
| **Engineering Memory** | File relative paths | Payload MD5 hash | Mapped to `ControlTowerEvidenceRecord` |
| **Runtime health** | Endpoint url | Response status = 200 OK | Mapped to `RuntimeServiceDetailSnapshot` |
| **Registry persistence** | Concurrency token / ID | Entity loaded from DB context | Mapped to `ControlTowerSnapshot` |

## Missing Evidence Resolution
If no provider emissions exist, the target component resolves to `UNKNOWN`. No zero-value metrics or healthy flags are fabricated.
