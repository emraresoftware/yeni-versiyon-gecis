# TASK_MULTI_REPO_001A — Private Documentation Federation and Deterministic Sync Pilot

## MODE: IMPLEMENTATION_AND_VERIFICATION
## PRIORITY: P0

---

## 🎯 OBJECTIVE

Create the private `Emare-Multi-Repo` documentation federation and synchronize exactly 10 approved Project Intake pilot projects into it.

*   Do not publish anything publicly.
*   Do not create public repositories.
*   Do not modify source projects.
*   Do not push to source repositories.
*   Do not copy source code or build artifacts.
*   Do not trust the previous Project Intake completion report without verifying the actual ten project packages.

---

## 🔒 CANONICAL REPOSITORIES

1.  **`Emare-Knowledge` / `emare-docs`:**
    *   Active Emare platform Engineering Memory.
2.  **`Emare-Multi-Repo`:**
    *   Private project documentation federation.
    *   Project metadata, generated analysis, reports, and evidence.
3.  **`Emare-Project-Catalog`:**
    *   Not implemented in this task.
    *   Future public subset after explicit approvals.

---

## 🚦 PHASE 0 — VERIFY PROJECT INTAKE PILOT

Locate the 10 claimed pilot projects.
For every project, prove:
*   Stable `ProjectId`
*   Approved source root
*   Source repository or folder
*   Source HEAD commit where applicable
*   Read-only scan evidence
*   Documentation package exists
*   Required artifacts exist:
    *   `PROJECT_PROFILE.md`
    *   `CURRENT_STATUS.md`
    *   `ARCHITECTURE.md`
    *   `FEATURES.md`
    *   `MODULE_INVENTORY.md`
    *   `API_INVENTORY.md`
    *   `DATABASE_INVENTORY.md`
    *   `DEPENDENCY_MAP.md`
    *   `REUSE_CANDIDATES.md`
    *   `DUPLICATE_ANALYSIS.md`
    *   `SECURITY_PUBLICATION_REPORT.md`
    *   `LICENSE_IP_REPORT.md`
    *   `EVALUATION.md`
    *   `PROJECT_MANIFEST.json`
    *   `EVIDENCE.json`
*   Security report exists
*   License/IP report exists
*   Duplicate analysis exists
*   Source project was not modified
*   Re-scan was deterministic
*   No public publication occurred

*If fewer than 10 valid packages exist:*
*   Overall result must be `PARTIAL`.
*   Do not invent missing projects.
*   Synchronize only verified packages.
*   Report every missing item.

---

## 📁 PRIVATE REPOSITORY STRUCTURE

Create or validate the folder tree in `Emare-Multi-Repo`:

```text
Emare-Multi-Repo/
├── README.md
├── MASTER_INDEX.md
├── catalog.json
├── schemas/
├── projects/
├── duplicate-clusters/
├── reuse-candidates/
├── publication-review/
├── security-reports/
├── agents/
└── archive/
```

Per project directory:
```text
projects/{PROJECT_ID}/
├── project.yaml
├── SOURCE.json
├── SYNC_STATUS.json
├── docs/
├── generated/
├── reports/
└── evidence/
```

---

## ⚙️ DOCUMENTATION MODES

Support:
1.  `source-owned`
    *   Source repository `docs/` is authoritative.
    *   Multi-Repo contains a traceable mirror.
2.  `federation-owned`
    *   Intended for legacy/frozen/read-only projects.
    *   Multi-Repo documentation is canonical.
    *   Source code remains untouched.
    *   All claims reference source commit/fingerprint evidence.

*Record the mode in each project's project.yaml.*

---

## 📄 PROJECT MANIFEST SCHEMA

Create and validate `.emare/project.yaml` containing:
*   `schemaVersion`
*   `projectId` (deterministic and immutable)
*   `name`
*   `documentationMode` (`source-owned` | `federation-owned`)
*   `owner`
*   `confidentiality`
*   `lifecycle`
*   `sourceRoot`
*   `sourceRepository`
*   `docsRoot`
*   `syncEnabled`
*   `readOnly`
*   `publicDocsAllowed`
*   `sourcePublicationAllowed`
*   `excludePatterns`

---

## 🤖 MULTI-REPO SYNC AGENT

Implement `MultiRepoSyncAgent` with responsibilities:
*   Read approved manifest.
*   Validate approved source boundary.
*   Validate intake package.
*   Calculate source and document hashes.
*   Copy approved text documentation only.
*   Preserve relative document structure.
*   Record source repository, branch, and commit.
*   Write `SOURCE.json` and `SYNC_STATUS.json`.
*   Detect stale mirror.
*   Detect duplicate project ID.
*   Detect conflicting authoritative documents.
*   Sanitize paths exposed to clients.
*   Produce deterministic results.
*   Isolate one project failure from others.

*Forbidden Actions:*
*   Source code changes.
*   Git push to source.
*   Public publication.
*   Secret copying.
*   Customer/partner private data copying.
*   No binaries or generated builds (`node_modules`, `bin`, `obj`, `.next`, `dist`).
*   No absolute local path exposure.

---

## 🛡️ SECURITY GATE

Check all synchronized outputs for:
*   Tokens, API keys, passwords, private SSH keys.
*   Connection strings, internal IPs, URLs, local user paths.
*   PII / KVKK data (customer names, private data).
*   White-label partner configurations, commercial secrets.
*   License/IP uncertainty or third-party copyrighted source.

*States:*
`PRIVATE`, `SECURITY_BLOCKED`, `LEGAL_REVIEW`, `FOUNDER_REVIEW` (Never `PUBLISHED` in this task).

---

## 📋 PROVENANCE DATA

`SOURCE.json` must include:
*   `projectId`, `sourceRepository`, `sanitizedRemote`, `sourceBranch`, `sourceCommit`, `sourceFingerprint`, `documentationMode`, `sourceDocsPath`, `scannedAt`, `scannerVersion`.

`SYNC_STATUS.json` must include:
*   `schemaVersion`, `projectId`, `sourceCommit`, `syncedAt`, `documentCount`, `contentHash`, `syncStatus`, `securityStatus`, `publicationStatus`, `warnings`, `errors`.

---

## 🚦 TEST MATRIX

Validate:
1.  Manifest validation
2.  Stable ProjectId
3.  Approved-root enforcement
4.  Read-only source behavior
5.  Source commit provenance
6.  `source-owned` mode
7.  `federation-owned` mode
8.  Secret blocking
9.  PII blocking
10. Internal path sanitization
11. Generated folder exclusion
12. Duplicate ProjectId rejection
13. Duplicate authoritative document detection
14. Failed project isolation
15. Stale mirror detection
16. Deterministic second sync
17. Unchanged source produces no unintended diff
18. No public publication
19. No source mutation
20. Control Tower registry population

---

## 📦 DELIVERABLES

1.  `MULTI_REPO_ARCHITECTURE.md`
2.  `MULTI_REPO_PROJECT_SCHEMA.md`
3.  `MULTI_REPO_SYNC_POLICY.md`
4.  `MULTI_REPO_SECURITY_POLICY.md`
5.  `MULTI_REPO_PUBLICATION_POLICY.md`
6.  `MULTI_REPO_PILOT_VERIFICATION.md`
7.  `MULTI_REPO_SYNC_REPORT.md`
8.  Verified project list / missing pilot package list.
9.  Up to 10 synchronized private project mirrors with commit provenance & security reports.
10. Deterministic second-run evidence.
11. Control Tower registry update evidence.
