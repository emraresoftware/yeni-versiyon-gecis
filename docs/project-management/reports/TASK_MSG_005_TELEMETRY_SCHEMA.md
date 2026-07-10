# TASK_MSG_005 — Batch Result Model & Telemetry Telemetry Schema Report

This document details the telemetry format and structural guidelines implemented to ensure robust tracing of the Omnichannel Messaging Core webhooks while maintaining strict PII compliance.

## Telemetry Log Schema

Every batch execution produces a structured log entry under the `Information` severity level:

```
Webhook Batch Telemetry - BatchId: {BatchId}, Channel: {Channel}, TenantIdHash: {TenantIdHash}, Total: {Total}, Success: {Success}, Failed: {Failed}, Duplicate: {Duplicate}, Invalid: {Invalid}, Skipped: {Skipped}, DurationMs: {DurationMs}, OverallStatus: {OverallStatus}
```

### Parameter Explanations
* **BatchId**: Unique identifier (`Guid`) representing the correlation scope of the batch HTTP payload.
* **Channel**: Channel type enum string representation (e.g. `WhatsApp`, `WebWidget`, `Messenger`).
* **TenantIdHash**: Cryptographically secure hash of the resolved database Tenant ID. If no tenant could be resolved, it falls back to `"none"`.
* **Total**: Total number of events normalized from the incoming payload.
* **Success**: Count of items successfully saved and dispatched.
* **Failed**: Count of items that failed processing.
* **Duplicate**: Count of items skipped due to idempotency checks.
* **Invalid**: Count of items containing bad payload schemas or tenant mismatches.
* **Skipped**: Count of unsupported event payloads that were ignored.
* **DurationMs**: Complete duration of the batch run in milliseconds.
* **OverallStatus**: Combined batch outcome enum string representation (`SUCCESS`, `PARTIAL_SUCCESS`, `FAILED`, `DUPLICATE_ONLY`).

## PII Compliance Rules

The following variables are **STRICTLY FORBIDDEN** from being outputted into logs or client trace responses:
1. **Raw Payloads**: Webhook JSON bodies are never dumped in full to diagnostics.
2. **Message Texts**: Customer content is private and kept entirely within the secured database bounds.
3. **Contact Details**: Phone numbers, emails, and names are excluded from logs.
4. **Credential Secrets**: API tokens, verify tokens, session keys, and secrets are masked or skipped.
5. **Storage Links**: Attachment URLs and keys are not logged.
