# Control Tower Priority Test Matrix

This document maps the 50 priority engine test cases defined inside `PriorityEngineTests.cs` to confirm full specification compliance.

| Test Case | Method Name | Verification | Status |
| --- | --- | --- | --- |
| 1 | `Test_1_FormulaWeightsTotalValidation` | Verifies weights summing to 1.00 pass validator. | ✅ PASS |
| 2 | `Test_2_InvalidNegativeWeightRejection` | Confirms negative weights trigger exception. | ✅ PASS |
| 3 | `Test_3_DuplicateFactorRejection` | Dictionary constraints reject duplicate key insertions. | ✅ PASS |
| 4 | `Test_4_CompleteEvidenceScoring` | Ensures scorable decisions produce scored results. | ✅ PASS |
| 5 | `Test_5_MissingRequiredFactorReturnsUnknown` | Missing required factor marks decision unscorable. | ✅ PASS |
| 6 | `Test_6_OptionalMissingFactorProducesPartialScore` | Bypasses optional factor weight and rescales properly. | ✅ PASS |
| 7 | `Test_7_MissingValuesAreNotCoercedToZero` | Ensures missing values resolve to null (Unknown). | ✅ PASS |
| 8 | `Test_8_FreshVerifiedEvidenceConfidence` | Verified evidence increases confidence score. | ✅ PASS |
| 9 | `Test_9_StaleEvidenceConfidenceReduction` | Out-of-date evidence reduces confidence by 0.20. | ✅ PASS |
| 10 | `Test_10_ConflictedEvidenceConfidenceReduction` | Conflicted evidence reduces confidence by 0.30. | ✅ PASS |
| 11 | `Test_11_BusinessImpactContribution` | Maps severity levels to impact scores. | ✅ PASS |
| 12 | `Test_12_RuntimeRiskContribution` | Maps subject health state to runtime risk. | ✅ PASS |
| 13 | `Test_13_CustomerImpactContribution` | Keywords scale customer impact score. | ✅ PASS |
| 14 | `Test_14_SecurityImpactContribution` | Security category resolutions. | ✅ PASS |
| 15 | `Test_15_QualityImpactContribution` | Quality rule ID contributions. | ✅ PASS |
| 16 | `Test_16_DataQualityImpactContribution` | Data quality rules mapping. | ✅ PASS |
| 17 | `Test_17_GovernanceImpactContribution` | Governance categories mapping. | ✅ PASS |
| 18 | `Test_18_AgeImpactWithFixedClock` | Compares AsOf with creation date. | ✅ PASS |
| 19 | `Test_19_UrgencyWithDueDate` | Distance to due date scales urgency score. | ✅ PASS |
| 20 | `Test_20_NoDueDateReturnsUnknownUrgency` | Bypasses urgency factor when due date is absent. | ✅ PASS |
| 21 | `Test_21_BlastRadiusScoring` | Scales based on affected subject count. | ✅ PASS |
| 22 | `Test_22_DependencyImpactScoring` | Maps scope hierarchy positions. | ✅ PASS |
| 23 | `Test_23_MitigationReduction` | Mitigation progress reduces score. | ✅ PASS |
| 24 | `Test_24_RecommendationAloneIsNotMitigation` | Rejects recommendation as a mitigation input. | ✅ PASS |
| 25 | `Test_25_RuntimeCriticalOverride` | Verified Critical Runtime Outages receive minimum 90. | ✅ PASS |
| 26 | `Test_26_SecurityCriticalOverride` | Verified Critical Security incidents receive minimum 95. | ✅ PASS |
| 27 | `Test_27_FailedDeploymentOverride` | Failed build decisions receive minimum 85. | ✅ PASS |
| 28 | `Test_28_OverrideRequiresEvidence` | Unverified outages skip override minimums. | ✅ PASS |
| 29 | `Test_29_ScoreClamped` | Final score is bound between 0 and 100. | ✅ PASS |
| 30 | `Test_30_DeterministicRounding` | AwayFromZero rounding policy checks. | ✅ PASS |
| 31 | `Test_31_StableRanking` | Validates list enrichment and ordering. | ✅ PASS |
| 32 | `Test_32_StableTieBreaking` | Breaks ties using DecisionId ascending. | ✅ PASS |
| 33 | `Test_33_ResolvedDecisionsExcluded` | Filters out Resolved status decisions. | ✅ PASS |
| 34 | `Test_34_SuppressedDecisionsExcluded` | Filters out Suppressed decisions. | ✅ PASS |
| 35 | `Test_35_ExpiredDecisionsExcluded` | Filters out Expired decisions. | ✅ PASS |
| 36 | `Test_36_UnknownDecisionsRetainedAfterScoredDecisions` | Retains unscorable findings after active priorities. | ✅ PASS |
| 37 | `Test_37_DecisionEnrichmentPreservesEvidence` | Verification of metadata cloning rules. | ✅ PASS |
| 38 | `Test_38_DecisionEnrichmentPreservesRecommendedActions` | Cloning rules verify actions preservation. | ✅ PASS |
| 39 | `Test_39_TraceReceivesPriorityBreakdown` | Trace contract receives the scored breakdown. | ✅ PASS |
| 40 | `Test_40_SameInputProducesIdenticalSemanticScoreOutput` | Verifies score calculations are pure functions. | ✅ PASS |
| 41 | `Test_41_GeneratedDurationDoesNotChangeDeterminismHash` | Ignores execution latency from MD5 hash. | ✅ PASS |
| 42 | `Test_42_FormulaVersionChangesSemanticHash` | Formula changes force new trace hash. | ✅ PASS |
| 43 | `Test_43_CorvisTreatedAsOrdinaryOrganization` | No custom exceptions applied. | ✅ PASS |
| 44 | `Test_44_NoHardCodedCorvisBranch` | Reflective check guarantees code logic isolation. | ✅ PASS |
| 45 | `Test_45_PriorityEnginePerformsNoProviderAccess` | Verifies absence of external system dependencies. | ✅ PASS |
| 46 | `Test_46_PriorityEnginePerformsNoDbContextAccess` | Verifies database context is not referenced. | ✅ PASS |
| 47 | `Test_47_PriorityEnginePerformsNoActionExecution` | Verifies engine does not trigger recommended workflows. | ✅ PASS |
| 48 | `Test_48_CancellationPropagation` | Propagates CancellationToken in loops. | ✅ PASS |
| 49 | `Test_49_BulkScoringIsolatesOneInvalidDecision` | Exceptions in bulk evaluation are isolated safely. | ✅ PASS |
| 50 | `Test_50_FullRuleEnginePriorityEngineIntegration` | Integration test pipeline matches correctly. | ✅ PASS |
