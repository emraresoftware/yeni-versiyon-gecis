# TASK_MSG_002 Final Freeze Report

## Objective
Finalize architecture check and freeze the database persistence and repository store layers for the Omnichannel Messaging Core (OMC). This report verifies all safety, performance, and transactional bounds before frozen code status is declared.

## QA Blocker Fixes Applied

### Fix 1 — Monotonic Message Status
* Added status transition validation via `CanTransitionStatus` inside `ConversationStore.cs`.
* Enforced progressive sequence: `Draft → Pending → Sent → Delivered → Read`.
* Out-of-order webhook statuses (e.g. late-arriving `Delivered` when status is already `Read`) are safely skipped.
* Added corresponding unit test `UpdateDeliveryReadStatus_ShouldIgnoreOutOfOrderWebhooks` to verify correctness.

### Fix 2 — Soft Delete Unique Index
* Configured partial index filter inside EF Core mapping `MessagingConfigurations.cs`:
  `"ExternalMessageId" IS NOT NULL AND "IsDeleted" = false`
* Generated new EF Core database migration: `FixOmnichannelMessagingStoreUniqueIndex`.

### Fix 3 — Tenant Filter for Status Update
* Extended `UpdateDeliveryReadStatusAsync` to accept `Guid tenantId`, ensuring message status updates are constrained strictly to the correct tenant context even when global query filters are bypassed.

### Fix 4 — Transaction Boundary
* Wrapped the entire message persistence sequence (thread creation, channel links, participant creation, message appending, and attachment mapping) in `MessagingGateway.cs` under a single database transaction boundary.
* Added a provider check `_db.Database.ProviderName == "Microsoft.EntityFrameworkCore.InMemory"` to safely bypass EF transactions during in-memory unit tests.

---

## Checkpoints Verified

### 1. Tenant Isolation
* All relational models implement `ITenantEntity` and are isolated via query filters. Incoming webhooks bind requests using `_db.SetCurrentTenant(envelope.TenantId)`.

### 2. Performance
* Addressed N+1 risks via eager loading (`.Include()`) on conversations and message timelines.

### 3. Gateway-Store Boundaries
* Gateway processes transport and validation, delegating persistence strictly to the `IConversationStore` boundary.

---

## Verdict

* **STATUS:** APPROVED
* **TASK_MSG_002_DECISION:** FREEZE
* **BLOCKERS:** None.
* **TECH_DEBT:**
  1. *InMemory Idempotency Cache:* Needs a Redis-backed persistent provider before horizontal scale-out of pods.
  2. *Distributed Locking:* Needs Redlock synchronization on channel initialization queries to prevent race conditions during first-message concurrent creation.
* **READY_FOR_TASK_MSG_003:** YES
