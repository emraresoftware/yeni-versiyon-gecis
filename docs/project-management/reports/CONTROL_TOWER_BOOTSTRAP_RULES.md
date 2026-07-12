# Control Tower Bootstrap Rules

This document specifies the validation and idempotency rules applied during platform registry bootstrapping.

## Idempotency Rules
1. Identifiers are resolved deterministically (e.g. static platform and workspace mapping GUIDs).
2. Second run without changes creates no writes or duplication rows.
3. DryRun remains default and never writes to database.

## Classification Rules
- Domain objects map to `ControlTowerDomain`.
- Module objects map to `ControlTowerModule`.
- Status fields parse safely; fallback to `UNKNOWN` or `Idea` if invalid.
