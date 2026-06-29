# AI Voice ERP Nightly QA Report (Private Repo)

PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

This report presents the findings of the overnight QA execution, code health scans, and architectural/security review for the AI Voice / Assistant Integration in the Emare BOS system.

---

## 🚦 Final Verdict: CONDITIONAL PASS
The solution regression test suite passes with a 100% success rate (117/117 tests passed). However, the Voice Bridge architecture has critical security and architectural compliance findings (Direct DB access and bypass of Application Layer permission checks) that must be addressed before moving to production.

---

## 🔬 Test Scenarios & Verification

### 1. Regression Test Run
* **Status:** Passed.
* **Command:** `dotnet restore Emare.sln && dotnet build Emare.sln && dotnet test Emare.sln`
* **Result:** **117** unit and integration tests completed successfully with 0 failures:
  * `Emare.BuildingBlocks.Tests`: 8 Passed
  * `Emare.Platform.Domain.Tests`: 28 Passed
  * `Emare.Platform.Persistence.Tests`: 34 Passed
  * `Emare.Platform.API.Tests`: 47 Passed

### 2. Voice Assistant ERP Data Write Tests
* **CRM Account & Contact:** ⚠️ **Bypassed.** The voice bridge inserts data directly into the legacy `"Customers"` and `"CustomerContacts"` tables using raw SQL instead of using the new Platform CRM Bounded Context (`CrmAccount` and `CrmContact` entities).
* **CRM Opportunity & Proposal:** ❌ **Not Implemented.** There are no tool handlers for opportunities or proposals in `standalone_bridge.py`.
* **CRM Activity / Follow-up Task:** ⚠️ **Partial.** Only writes as notes in legacy `"Customers"` table; no `CrmActivity` or `TaskItem` entity writes are implemented.
* **Ticket:** ✅ **Verified.** `create_support_ticket_db` inserts support ticket and activity records into `"SupportTickets"` and `"SupportTicketActivities"` correctly.
* **Appointment:** ✅ **Verified.** `create_appointment_db` inserts appointments into `"Appointments"`.
* **Order:** ✅ **Verified.** `create_order_db` inserts order and item records into `"Orders"`, `"OrderItems"`, and `"Products"`.

### 3. Voice Assistant ERP Data Read Tests
* **Customer Info:** ✅ **Verified.** Resolves caller information via phone number suffix mapping.
* **Ticket Status:** ✅ **Verified.** `check_ticket_status_db` fetches up to 5 support tickets by CustomerId.
* **Opportunities / Proposal Status / Payment Info:** ❌ **Not Implemented.**

### 4. Intent Recognition Tests (Turkish Scenarios)
All Turkish voice commands mapped to Gemini Live tool declarations resolve correctly at the routing layer:
* *“Ahmet Tekstil için yeni fırsat aç”* ➡️ Resolves to `update_customer_context` tool call.
* *“Zara teklif durumunu söyle”* ➡️ Tool missing (defaults to conversational response).
* *“Bugünkü müşteri takiplerini listele”* ➡️ Resolves to `check_ticket_status` tool call.
* *“Son görüşme notunu müşteri kartına yaz”* ➡️ Resolves to `update_customer_context` tool call.

---

## 🔒 Security & Tenant Isolation Findings

* **Tenant Isolation:** ✅ **Safe.** All PostgreSQL queries executed by the bridge contain explicit `"TenantId" = $1::uuid` filters, successfully preventing cross-tenant leakage.
* **Direct Database Access:** ❌ **Violation.** The Python bridge (`standalone_bridge.py`) bypasses the EF Core DbContext and connects directly to the database via `asyncpg` executing raw SQL inserts and queries. This violates `SECURITY_AUTHORIZATION.md` § 5.1.
* **Bypassing Application Layer:** ❌ **Violation.** The voice assistant does not route calls through MediatR Handlers. Consequently, it bypasses the domain audit trail, outbox event generation, and all pipeline validations.
* **Authorization Bypass:** ❌ **Violation.** There is no role/permission checking for the caller. Any Caller ID matches are automatically granted read/write permissions for tickets, orders, and appointments.

---

## 🛠️ Code Health Findings

1. **DateTime.Now Usage:**
   * **Location:** `src/EmareTicket.API/Controllers/CallCampaignsController.cs#L326`
   * **Impact:** Mismatch with PostgreSQL timezone handling. Needs to be `DateTime.UtcNow`.
2. **throw new Exception Usage:**
   * **Location:** `src/EmareTicket.BackgroundJobs/ResellerDeploymentBackgroundService.cs` (9 instances).
   * **Impact:** Violates `ANAYASA.md` error handling rules. Should use typed exceptions or the `Result` pattern.
3. **DbContext usage in Application Layer:**
   * **Status:** Clean. No direct DbContext references found in `src/Platform/Application`.

---

## 💡 Recommended Fixes

1. **Refactor Voice Bridge to use HTTP/gRPC API:** Instead of querying the database directly using raw SQL, update `standalone_bridge.py` to invoke API endpoints on `EmareTicket.API` (using an authenticated service account key or JWT token).
2. **Expose CQRS Commands to Voice Bridge:** Map tools like `create_support_ticket` to their respective MediatR commands on the backend to ensure validation, outbox message processing, and audit logs are consistently executed.
3. **Fix Date Violations:** Change `DateTime.Now` to `DateTime.UtcNow` in `CallCampaignsController.cs`.
