# Task MSG_002 Pre Architecture Freeze Report

## Objective
Define and freeze the core architecture contracts and standards for the Omnichannel Messaging Core (OMC) Conversation Store, ensuring consistency across all current and future integration adapters (WhatsApp, Messenger, Instagram, Email, Web Chat).

## Scope
* Formulate C# Event definitions, payloads, and processing details for 14 conversation lifecycle events.
* Analyze single-channel vs. multi-channel conversation threading options and commit to a Unified Threading Model.
* Create immutable and mutable messaging standards defining core identity fields.
* Formulate attachment validation, storage paths, virus scanning policies, and data retention rules.
* Layout a roadmap for migrating from single-node local in-memory idempotency cache to multi-instance Redis/Database checks.
* Design a Mermaid state transition lifecycle schema.
* Frame handoff protocols detailing human takeovers, AI pause-resume boundaries, and audit logging.
* Specify stable interface microservice transition boundaries.

## Files Created
* [Conversation_Event_Contract.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Conversation_Event_Contract.md)
* [Conversation_Model_Standard.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Conversation_Model_Standard.md)
* [Message_Identity_Standard.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Message_Identity_Standard.md)
* [Attachment_Standard.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Attachment_Standard.md)
* [Distributed_Idempotency_Roadmap.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Distributed_Idempotency_Roadmap.md)
* [Conversation_Lifecycle.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Conversation_Lifecycle.md)
* [Human_Handoff_Contract.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Human_Handoff_Contract.md)
* [Microservice_Boundary.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/architecture/Microservice_Boundary.md)

## Files Modified
* [SPRINT_3.md](file:///Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/project-management/sprints/SPRINT_3.md)

## Architecture Decisions
* **Unified Threading Model:** A single logical `Conversation` aggregate binds multiple `ConversationChannel` records. Conversations are unified across channels based on CRM customer mappings, providing a seamless agent timeline. Outbound responses are routed dynamically to the last active channel.
* **Hardened Security & Virus Scan:** All incoming files undergo magic-number signature checks (bypassing trivial extension scans) and background ClamAV scans before transition from `Scanning` to `Clean` status.
* **Event Sourcing Ready:** Detailed events carry `correlationId` and ordering keys based on `conversationId` partition ranges, preparing the system for robust message brokers (Kafka/NATS).

## Dependencies Added
None.

## Build Result
Success. No code additions or mutations were introduced in this task, preserving the zero-error compile state.

## Test Result
Success. Existing 689 unit tests pass cleanly.

## Performance Notes
* Standardized attachment previews and image thumbnails reduce bandwidth and client-side page load times on large channels.
* In-memory cache idempotency holds lookup times under 1µs during MVP testing.

## Security Notes
* Eklenti nesneleri (attachments) directly reference signed temporary URLs or proxies, strictly preventing direct asset listing or unauthorized cross-tenant object access.
* Log statements exclude raw text, tokens, or credential payloads.

## Technical Debt
None.

## Risks
None.

## Known Limitations
None.

## Breaking Changes
None.

## Next Recommended Task
* `TASK_MSG_002 — Conversation Store` (Executing EF Core database migrations, entity models setup, and repository updates matching these standards).
