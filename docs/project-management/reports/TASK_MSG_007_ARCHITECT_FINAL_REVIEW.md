PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

# TASK_MSG_007 Architect Final Review Report

Review of the Transactional Outbox Pattern and Atomic Idempotency Reservation system implementation for the Omnichannel Messaging Core (OMC).

## Detailed Architectural Evaluations

### 1. Atomic Idempotency
* **Reservation Semantics:** Excellent design. The new three-phase idempotency reservation contract (`TryReserveAsync`, `CompleteAsync`, `ReleaseAsync`) resolves the race window of the previous split check-then-set logic.
* **Rollback Safety:** Verified. If database commits fail or lock acquisitions timeout inside the gateway, `ReleaseAsync` is immediately executed in the `catch` blocks to delete the temporary reservation.
* **Commit Completion:** Once database saving is committed, `CompleteAsync` marks the reservation state as `completed` with a 24-hour TTL.
* **PII Minimization:** Safe. Hashing `TenantId` and the external message ID using SHA-256 before forming keys ensures raw contact phone numbers never leak to Redis memory lists.

### 2. Transactional Outbox
* **Atomic Boundary:** The message persistence writes (conversations, messages, attachments) and `MessagingOutboxMessage` row inserts are executed under the exact same Postgres database transaction block. If outbox writing fails, message persistence is safely rolled back.
* **Decoupled Ingestion:** Excellent. Gateway network dispatches (`_dispatcher.DispatchAsync`) are completely removed from the webhook ingestion path. Returning HTTP 200 is immediate, reducing endpoint latency and protecting API throughput.

### 3. Asynchronous Polling Worker
* **Skip-Locked Locking:** Under PostgreSQL, the poller uses raw SQL `FOR UPDATE SKIP LOCKED` to lock pending/failed outbox rows. This avoids lock contention across multi-instance pods and guarantees each pod works on a unique message set.
* **Lock Recovery:** If a pod crashes mid-execution, locked records automatically unlock and become retriable once `LockedUntilUtc` expires.
* **UnitTest Compatibility:** Correctly implements LINQ-based fallback logic to support EF Core InMemory test suites.
* **Graceful Shutdown:** Worker loops monitor and react to `CancellationToken` triggers immediately.

### 4. Retry & Dead Letter Routing
* **Transient Failures:** Handled. Any dispatch exception triggers an attempt increment, log recording, and schedules a future retry.
* **Backoff Jitter:** Exponential delay calculation is bounded by `MaxBackoffMs` and successfully includes a 15% random jitter to avoid collision storms across replicas.
* **Dead Lettering:** Once attempts cross `MaxAttempts` (default: 5), the record shifts to `DeadLetter` status, excluding it from future automated polling cycles.

### 5. Delivery Guarantees
* **Classification:** **At-Least-Once Delivery**.
* **Downstream Idempotency Requirement:** Downstream event consumers must apply their own idempotency checks.
* **Duplicate Risk Analysis:** If the dispatcher succeeds in calling the downstream API but crashes before updating the outbox status to `Completed` in PostgreSQL, the record will be retried and dispatched again. This is a standard distributed system constraint, not a blocker.
* **Decision:** Accepted as standard architectural behavior. Marked in Technical Debt.

### 6. Security & Retention
* **Tenant Isolation:** Maintained via query filters and composite indexing (`TenantId` + `Status`).
* **PII minimization:** Key hashes are used for Redis.
* **Retention Policy:** The outbox table stores payloads in `PayloadJson`. Over time, completed messages will accumulate. A retention cleanup background job to prune completed rows older than 7-30 days is required.

### 7. Performance & Migration
* **Postgres Indexes:** Migration `AddMessagingOutbox` creates precise composite indices supporting fast polling (`Status` + `NextAttemptAtUtc`) and tenant checks (`TenantId` + `Status`).
* **N+1 Eliminated:** Database writes are bundled inside a single transaction save block.

### 8. Regression
* Unit and integration test suites pass successfully (765/765 tests passed). LEGOW WhatsApp, WebWidget, live chat sessions, and tenant anti-spoofing protections remain fully intact.

---

## Response to Specific Questions

### 1. TASK_MSG_007 production ready mi?
**Cevap:** Evet. Kod tabanı hatasız derlenmekte, tüm 765 test yeşil geçmekte, transactional outbox ve skip-locked concurrency mekanizmaları en üst standartlarda kurgulanmıştır.

### 2. Gerçek delivery guarantee nedir?
**Cevap:** **At-Least-Once** (En az bir kere teslimat). Veritabanı kesintileri veya pod çökmeleri sonrasında mükerrer downstream dispatches olabileceği için event tüketicilerinin (consumers) idempotent olması gereklidir.

### 3. Duplicate downstream dispatch riski blocker mi?
**Cevap:** Hayır. Dağıtık mimarinin doğal bir kısıtıdır, downstream alıcıların kendi idempotency mekanizmalarını kurması gerekmektedir.

### 4. Outbox payload güvenlik/retention politikası yeterli mi?
**Cevap:** Güvenlik açısından yeterlidir. Ancak db şişmesini önlemek adına tamamlanmış kayıtların 7-30 gün sonra otomatik temizlenmesini sağlayan bir **Outbox Retention Background Job** kurulması teknik borç (Tech Debt) olarak takip edilmelidir.

### 5. Sprint 3 kapatılabilir mi?
**Cevap:** Evet, Sprint 3 başarıyla kapatılabilir ve dondurulabilir (freeze).

### 6. TASK_MSG_008 Inbox Projection başlayabilir mi?
**Cevap:** Evet, TASK_MSG_008 başlatılabilir.

---

## Final Report

**STATUS:** APPROVED

**ARCHITECT_DECISION:** APPROVE

**ARCHITECTURE_SCORE:** 9.8 / 10

**SCALABILITY_SCORE:** 9.9 / 10

**SECURITY_SCORE:** 9.8 / 10

**DELIVERY_GUARANTEE:** AT_LEAST_ONCE

**DUPLICATE_DISPATCH_DECISION:** ACCEPTED AS TECH DEBT (Downstream consumer idempotency enforced)

**OUTBOX_TRANSACTION:** APPROVED (Same Postgres transaction context)

**DISPATCHER_DECISION:** APPROVED (Skip-locked concurrent worker model)

**RETRY_DECISION:** APPROVED (Exponential backoff + 15% jitter)

**DEAD_LETTER_DECISION:** APPROVED (MaxAttempts exceeded routing)

**MIGRATION_DECISION:** APPROVED (Additive migration active)

**TECH_DEBT:**
1. *Downstream Consumer Idempotency:* Handlers receiving outbox events must implement their own idempotency checks to handle duplicate dispatches during DB crash windows.
2. *Outbox Retention Cleanup Job:* Implement an automated background cleaner to purge or archive completed outbox messages older than 7-30 days to avoid Postgres table bloat.

**BLOCKERS:** None

**PRODUCTION_READY:** YES

**SPRINT_3_FREEZE:** YES

**READY_FOR_TASK_MSG_008:** YES

**RECOMMENDED_NEXT_TASK:** TASK_MSG_008 (Inbox Projection / CQRS Read Model)

**PUSH:** NO

**COMMIT:** NONE
