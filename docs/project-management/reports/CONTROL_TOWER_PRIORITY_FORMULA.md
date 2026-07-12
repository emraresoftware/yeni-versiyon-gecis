# Control Tower Priority Formula Specification

This document defines the canonical, versioned priority formula used by the Control Tower Executive Decision Engine.

## Canonical Weights

The subtotal priority score is calculated using the following weights, summing to exactly 1.00:

| Factor ID | Name | Weight | Purpose |
| --- | --- | --- | --- |
| `BusinessImpact` | Business Impact | 0.20 | Proportional to severity of business logic degradation. |
| `RuntimeRisk` | Runtime Risk | 0.18 | Based on service or container execution health states. |
| `CustomerImpact` | Customer Impact | 0.14 | Elevates priority for direct tenant/customer impact keywords. |
| `SecurityImpact` | Security Impact | 0.12 | Resolves vulnerability/incident severity for Security rules. |
| `QualityImpact` | Quality Impact | 0.08 | Triggered by test failure or code quality degradation. |
| `DataQualityImpact` | Data Quality Impact | 0.05 | Flags incomplete snapshots or validation evidence data. |
| `GovernanceImpact` | Governance Impact | 0.04 | Applies to missing ownership or architecture review tasks. |
| `AgeImpact` | Age Impact | 0.06 | Linearly increments score relative to decision age. |
| `Urgency` | Urgency | 0.05 | Calculated from SLA thresholds and due date closeness. |
| `BlastRadius` | Blast Radius | 0.04 | Scales based on the count of affected registry subjects. |
| `DependencyImpact` | Dependency Impact | 0.04 | Proportional to subject placement in system topology. |

## Score Calculations

### 1. Weighted Subtotal
$$WeightedSubtotal = \frac{\sum (NormalizedValue_{AvailableFactor} \times Weight_{Factor})}{\sum Weight_{AvailableFactor}}$$

### 2. Mitigation Progress Reduction
$$AdjustedScore = WeightedSubtotal \times (1.0 - MitigationProgress)$$

### 3. Clamping and Rounding
- Clamp to $0 \le Score \le 100$.
- Round deterministically using `MidpointRounding.AwayFromZero`.
