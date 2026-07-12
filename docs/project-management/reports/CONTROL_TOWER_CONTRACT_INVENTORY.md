# Control Tower Contract Inventory

This document lists all active contract declarations created under the `EmareTicket.Contracts/ControlTower/` directory for the recovery scope.

## 1. Identity Contracts
- **`CanonicalId`**: Immutable value representation validating canonical structure for:
  - `PLAT-`, `ORG-`, `WS-`, `DOM-`, `MOD-`, `FEAT-`, `CAP-`, `WF-`, `ACT-`, `REPO-`, `BUILD-`, `REL-`, `DEP-`, `AGENT-`, `TASK-`, `RISK-`, `INCIDENT-`, `METRIC-`.

## 2. Status Contracts
- **`BusinessLifecycleStatus`**: Idea, Planned, Analysis, Design, Implementation, Review, Qa, Staging, Production, Monitoring, Deprecated, Archived.
- **`RuntimeHealthStatus`**: Unknown, Healthy, Warning, Degraded, Critical, Offline, Maintenance.
- **`EngineeringWorkStatus`**: Backlog, Ready, InProgress, Blocked, Review, Qa, Done, Cancelled, Duplicate.
- **`DeploymentStatus`**: NotDeployed, Queued, Building, Deploying, Verifying, Succeeded, Failed, RolledBack.
- **`DocumentationStatus`**: Missing, Draft, Stale, Current, Verified, Conflicted.
- **`AgentOperationalStatus`**: Offline, Idle, Planning, Executing, WaitingApproval, Blocked, Verifying, Completed, Failed.

## 3. Base Value Contracts
- **`OwnershipContract`**: Business owner, tech owner, agent owner references.
- **`ScopeContract`**: Scoped mapping references.
- **`EvidenceContract`**: Verified observation record with confidence scores.
- **`FreshnessContract`**: Stale observation limits.

## 4. Registry Contracts
- **`PlatformRegistryItem`**
- **`OrganizationRegistryItem`**
- **`WorkspaceRegistryItem`**
- **`DomainRegistryItem`**
- **`ModuleRegistryItem`**
- **`FeatureRegistryItem`**
- **`CapabilityRegistryItem`**
- **`WorkflowRegistryItem`**
- **`ActionRegistryItem`**
- **`ControlTowerModuleAssetContract`** (supporting API, DB, UI, Docs, Test, Prompt, Event, SignalR Hub, background workers).

## 5. Snapshot Contracts
- **`ControlTowerSnapshot`**
- **`OrganizationDetailSnapshot`**
- **`WorkspaceDetailSnapshot`**
- **`DomainDetailSnapshot`**
- **`ModuleDetailSnapshot`**
- **`FeatureDetailSnapshot`**
- **`AgentDetailSnapshot`**
- **`RepositoryDetailSnapshot`**
- **`RuntimeServiceDetailSnapshot`**
- **`ControlTowerDataQualitySnapshot`**
