# Control Tower Compatibility Matrix

This document traces the mapping definitions between legacy control engines, snapshots, DTOs, and the new canonical contracts.

## Mapping Table

| Existing Source | Canonical Target | Mapping Status | Missing Fields | Migration Risk | Deprecated Candidate |
|---|---|---|---|---|---|
| **ProductTwinSnapshot** | `ModuleDetailSnapshot` / `FeatureDetailSnapshot` | Fully Mapped | None | Low | Yes |
| **EmareBrainSnapshot** | `ControlTowerSnapshot` | Fully Mapped | None | Low | Yes |
| **PlatformIntelligenceSnapshot** | `ControlTowerSnapshot` | Fully Mapped | Analyzer lists | Low | Yes |
| **PlatformDecisionSnapshot** | `ActionRegistryItem` | Fully Mapped | None | Low | Yes |
| **ExecutionSnapshot** | `AgentDetailSnapshot` | Fully Mapped | None | Low | Yes |
| **PlatformMemory Contracts** | `ControlTowerSnapshot` | Fully Mapped | None | Low | Yes |
| **Workspace DTOs** | `WorkspaceRegistryItem` | Fully Mapped | None | Low | Yes |
