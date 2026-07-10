# Backlog Item Plan — TASK_MSG_004_BATCH_WEBHOOK_NORMALIZATION

## Pre-flight Check
PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

---

## Technical Debt Description
High-throughput production webhook endpoints for Meta Messenger and WhatsApp Business Cloud API often bundle multiple incoming user messages, reactions, or status updates in a single HTTP request payload array (e.g. `entry` or `changes` JSON array properties).

Currently, normalizer adapters read only the first element (`[0]`) to process immediately. Any concurrent messages in the same payload are not processed, creating a risk of data loss under high-load scenarios.

## Scope of Backlog Task

### 1. Refactor Channel Adapter Signature
* Change the contract signature of `IChannelAdapter.NormalizeInboundAsync` to return a list of envelopes:
  ```csharp
  Task<List<InboundMessageEnvelope>> NormalizeInboundAsync(object rawPayload, CancellationToken ct);
  ```

### 2. Batch Normalization Processing
* **Messenger Adapter:** Loop through the entire `entry` and `messaging` array elements to build normalized envelopes for each messaging event.
* **WhatsApp Adapter:** Loop through all objects under `entry`, `changes`, and `value.messages` or `value.statuses`.

### 3. Messaging Gateway Batch Handling
* Update `ProcessWebhookAsync` to process the returned `List<InboundMessageEnvelope>` sequentially or concurrently:
  * Apply individual idempotency checking.
  * Implement partial failure policy (if message 1 fails, log and continue processing message 2).
  * Maintain database transaction boundaries or utilize individual transactions per envelope to prevent partial failures from rolling back successfully processed envelopes in the same batch.
  * Preserve correct order of processing.

### 4. Backlog Status
* **Estimated Effort:** 2 story points
* **Priority:** Medium
* **Target Release:** Sprint 4 / Architect approval required before integration.
