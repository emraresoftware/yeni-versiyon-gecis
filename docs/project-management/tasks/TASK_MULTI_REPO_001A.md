# TASK_MULTI_REPO_001A
## Bootstrap, Secure and Populate the Private Multi-Repo Federation

TARGET REPOSITORY:
emraresoftware/multi-repo

MODE:
IMPLEMENTATION_AND_VERIFICATION

PRIORITY:
P0

IMPORTANT CURRENT REALITY

The target repository currently:
- is PRIVATE (Secured from public view),
- contains docs/, .gitignore, and docs/legacy/,
- does not yet contain the private federation structure,
- does not prove the claimed ten-project pilot packages.

Do not trust previous completion reports without repository evidence.

====================================================
PHASE 0 — SECURITY GATE
====================================================

1. Verify repository visibility.

Required outcome:
PRIVATE

If visibility is PUBLIC or cannot be changed:
- STOP before copying project documentation.
- Report BLOCKED_VISIBILITY.
- Do not synchronize any internal project.

2. Remove .DS_Store from tracking.

3. Add root .gitignore including:

.DS_Store
.env
.env.*
*.pem
*.key
*.p12
*.pfx
node_modules/
bin/
obj/
.next/
dist/
coverage/
.idea/
.vscode/
*.user
*.suo

4. Scan the full current Git history for:

- API keys
- tokens
- passwords
- private keys
- connection strings
- internal IPs and URLs
- local user paths
- customer/partner identifiers
- PII/KVKK content

5. If a secret is found:
- mark SECURITY_BLOCKED,
- do not merely delete it in a new commit,
- report required credential rotation and history cleanup.

====================================================
PHASE 1 — REPOSITORY FOUNDATION
====================================================

Create:

README.md
MASTER_INDEX.md
catalog.json

schemas/
projects/
duplicate-clusters/
reuse-candidates/
publication-review/
security-reports/
agents/assignments/
agents/run-reports/
agents/failed-jobs/
archive/

Do not copy source code or binaries.

README must define:

- This is a private documentation federation.
- Source project docs remain authoritative in source-owned mode.
- Legacy projects may use federation-owned mode.
- Public publication is forbidden without security, legal and Founder approval.
- Agents cannot write directly to main.

====================================================
PHASE 2 — SCHEMAS
====================================================

Create and validate:

schemas/project-manifest.schema.json
schemas/source-record.schema.json
schemas/sync-status.schema.json
schemas/publication-status.schema.json
schemas/evidence.schema.json

Per-project structure:

projects/{PROJECT_ID}/
├── project.yaml
├── SOURCE.json
├── SYNC_STATUS.json
├── docs/
├── generated/
├── reports/
└── evidence/

====================================================
PHASE 3 — VERIFY THE CLAIMED TEN-PROJECT PILOT
====================================================

Locate the exact ten claimed pilot projects.

For each, prove:

- ProjectId
- approved source root
- source repository/folder
- source commit or deterministic fingerprint
- required intake artifacts
- security report
- license/IP report
- duplicate analysis
- read-only scan evidence
- no source mutation
- deterministic second scan

Required artifacts:

PROJECT_PROFILE.md
CURRENT_STATUS.md
ARCHITECTURE.md
FEATURES.md
MODULE_INVENTORY.md
API_INVENTORY.md
DATABASE_INVENTORY.md
DEPENDENCY_MAP.md
REUSE_CANDIDATES.md
DUPLICATE_ANALYSIS.md
SECURITY_PUBLICATION_REPORT.md
LICENSE_IP_REPORT.md
EVALUATION.md
PROJECT_MANIFEST.json
EVIDENCE.json

If ten valid packages do not exist:

- return PARTIAL,
- do not invent projects,
- synchronize only verified packages,
- list missing packages and missing artifacts.

====================================================
PHASE 4 — MULTI-REPO SYNC AGENT
====================================================

Implement deterministic MultiRepoSyncAgent.

Rules:

- read approved project manifest,
- enforce source boundaries,
- copy approved text documentation only,
- preserve source provenance,
- calculate semantic content hash,
- sanitize client-visible paths,
- isolate project failures,
- reject duplicate ProjectId,
- detect stale mirror,
- detect authoritative document conflict,
- never modify or push to source project,
- never publish publicly.

Support:

documentationMode: source-owned
documentationMode: federation-owned

====================================================
PHASE 5 — CONTROL TOWER
====================================================

Register the verified synchronized projects in the existing canonical
Control Tower registry.

Expose:

- ProjectId
- Name
- DocumentationMode
- SyncStatus
- SecurityStatus
- PublicationStatus
- SourceCommit
- DocsFreshness
- DuplicateCluster
- ReuseCandidates
- Owner
- LastScan
- RecommendedDecision
- Evidence

Do not create a competing registry.

====================================================
PHASE 6 — DETERMINISM TEST
====================================================

Run synchronization twice without changing sources.

The second run must produce:
- zero duplicate projects,
- zero duplicate documents,
- same ProjectIds,
- same semantic hashes,
- stable ordering,
- no unintended Git diff.

====================================================
PUBLICATION RULE
====================================================

Allowed states during this task:

PRIVATE
SECURITY_BLOCKED
LEGAL_REVIEW
FOUNDER_REVIEW

Forbidden state:

PUBLISHED

Do not start TASK_PROJECT_INTAKE_002.
Do not create Emare-Project-Catalog.
Do not create public project repositories.

====================================================
DELIVERABLES
====================================================

MULTI_REPO_ARCHITECTURE.md
MULTI_REPO_PROJECT_SCHEMA.md
MULTI_REPO_SYNC_POLICY.md
MULTI_REPO_SECURITY_POLICY.md
MULTI_REPO_PUBLICATION_POLICY.md
MULTI_REPO_PILOT_VERIFICATION.md
MULTI_REPO_SYNC_REPORT.md

Also return:

- visibility verdict,
- history security scan,
- verified project package count,
- synchronized project count,
- missing/invalid package list,
- source provenance,
- deterministic second-run evidence,
- Control Tower registry evidence,
- final commit SHA.

====================================================
COMPLETION VERDICT
====================================================

Return exactly one:

COMPLETED_AND_VERIFIED
PARTIAL
CONFLICTED
SECURITY_BLOCKED
NOT_IMPLEMENTED

Recommended next task:

TASK_MULTI_REPO_001B — Control Tower Project Atlas and Founder Review Workflow
