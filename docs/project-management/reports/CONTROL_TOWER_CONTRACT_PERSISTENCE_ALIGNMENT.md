# Control Tower Contract Persistence Alignment

This document details the schema reconciliation analysis between the canonical contracts and the database persistence models.

## Alignment Verification

1. **Entity Field Mapping**
   - Persistence entity properties (`BusinessLifecycleStatus`, `RuntimeHealthStatus`, etc.) map to Enum names as standard text fields. This guarantees compatibility and clean upgrades.
   - Concurrency tokens and tenancy filters align with Clean Architecture specifications.

2. **Status Models Representation**
   - The status strings saved in database columns map directly to the defined `StatusModels.cs` enums, preventing duplicates.

3. **Identity Validation Rules**
   - Database unique index constraints on `CanonicalId` map directly to the string representations of `CanonicalId` values, enforcing the same validation limits.

4. **Evidence & Freshness Alignments**
   - Freshness checks utilize UTC timestamp comparisons matching `FreshnessContract` definitions. No default zero-values are generated.

5. **Tenancy Hierarchy Mapping**
   - The organizational trees map exactly: `Platform -> Organization -> Workspace -> Domain -> Module -> Feature -> Capability`.
   - Corvis acts as a normal Organization type, requiring no custom bypass/special-case coding.
