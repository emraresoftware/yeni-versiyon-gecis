# Control Tower Priority Factors

This document catalogs the 13 canonical priority factor resolvers configured inside the Decision Engine.

## Canonical Factor Resolvers

1. **`BusinessImpact`**: Resolves baseline severity to 10 (Info), 30 (Low), 50 (Medium), 70 (High), or 90 (Critical).
2. **`RuntimeRisk`**: Inspects subject health states (Healthy: 10, Warning: 50, Offline: 90, Critical: 95).
3. **`CustomerImpact`**: Checks title/description for "Customer" or "incident" keyword matches (matches: 80, quality: 40, else: 20).
4. **`SecurityImpact`**: Set to 95/75 for decisions categorized under Security; otherwise baseline 10.
5. **`QualityImpact`**: Set to 90 for test failures, 50 for missing evidence, and 20 for baseline.
6. **`DataQualityImpact`**: Resolves to 80 for DataQuality rules; otherwise baseline 10.
7. **`GovernanceImpact`**: Resolves to 80 for missing ownership and 70 for governance category.
8. **`AgeImpact`**: Calculated relative to decision creation date. Linearly scales at 2 points per hour up to 100.
9. **`Urgency`**: Compares `DueDate` metadata value against the evaluation clock (Overdue: 100, <=1 day: 90, <=3 days: 70, else: 30).
10. **`BlastRadius`**: Scales from 30 (1 subject), 60 (2-5 subjects) to 95 (>5 subjects).
11. **`DependencyImpact`**: Set to 70 for Workspace/Domain scope, 40 for Module, and 20 for Feature/Capability.
12. **`MitigationProgress`**: Extracted from active remediation flags: 50% for completed rollback/deployed fixes, 40% for in-progress tasks, 10% for assigned owners, and 0% for proposed recommendations.
13. **`EvidenceConfidence`**: Calculates base confidence from average evidence weights, applying penalties of -0.2 for stale evidence, -0.3 for conflicted evidence, and +0.1 for verified evidence.
