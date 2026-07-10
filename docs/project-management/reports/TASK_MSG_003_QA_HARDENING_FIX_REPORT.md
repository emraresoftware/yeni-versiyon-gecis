# QA Hardening Fix Report — TASK_MSG_003

## Pre-flight Check
PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

---

## Hardening Objectives
Address the security, tenant spoofing, and safe URI parsing vulnerabilities raised by the QA agent (A2 Sentinel) in `QA_TASK_MSG_003.md`.

## Implemented Fixes

### Fix 1: Safe Attachment URL Resolution
* **Location:** [MessengerAdapter.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Adapters/MessengerAdapter.cs) & [WebWidgetAdapter.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Adapters/WebWidgetAdapter.cs)
* **Changes:** Replaced raw `new Uri(url)` parsing with `Uri.TryCreate(url, UriKind.Absolute, out var parsedUri)` validations.
* **Constraints Imposed:**
  * Only accepts `http` and `https` schemes.
  * Skips relative, malformed, or dangerous schemes (like `file://`, `javascript:`) without raising unhandled exceptions or failing the entire webhook processing.
  * Prevents raw URL strings from exposing PII/secrets in exception traces or logs.

### Fix 2: Tenant trust context & Anti-Spoofing
* **Location:** [MessagingGateway.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/MessagingGateway.cs)
* **Changes:** Integrated with `ICurrentUserService` to perform server-side authenticated session tenant checks.
* **Constraints Imposed:**
  * For the `WebWidget` channel, the session tenant ID MUST exist (fail-closed model).
  * If the payload provides a `tenantId`, it must match the session tenant ID. Any mismatch triggers a "Tenant ID spoofing detected" rejection.
  * For webhook-based channels, a tenant spoofing check ensures that if the normalized envelope payload contains a pre-populated `TenantId`, it matches the resolved tenant ID derived securely from account configuration lookups.

---

## Verifications
* Tested using unit tests:
  * Attachment URL check scenarios (valid HTTPS, relative, javascript, file schemes).
  * WebWidget authenticated session validation, missing context rejection, mismatch/spoofed tenant ID rejections.
* All 722 tests are green.
