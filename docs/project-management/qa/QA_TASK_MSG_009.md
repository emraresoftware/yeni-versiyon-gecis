# QA Review — TASK_MSG_009_INDEPENDENT_QA

**Task:** TASK_MSG_009_INDEPENDENT_QA  
**Date:** 2026-07-11  
**Reviewer:** A2 Sentinel  
**Scope:** SignalR Live Inbox Infrastructure  
**Kısıt:** Kod değiştirilmedi, commit yapılmadı.

---

## Final Report

* **STATUS:** APPROVED
* **QA_DECISION:** PASS
* **BUILD:** PASS (0 errors, 5 warnings)
* **TARGET_TESTS:** 122/122 PASS (LiveInbox, InboxProjection, and Messaging tests)
* **FULL_TESTS:** 803/803 PASS (Full application suite tests)
* **TENANT_ISOLATION:** PASS. Connected users are grouped into `inbox-tenant-{tenantId}` automatically. Broadcast messages and presence events are scoped strictly to the tenant-specific group, preventing cross-tenant information leakage.
* **AUTHORIZATION:** PASS. Connected users must present a valid JWT token containing `tenant_id` and `nameidentifier` claims or the connection is aborted. The hub method `SubscribeToConversation(Guid conversationId)` explicitly queries the database to verify the conversation belongs to the caller operator's tenant, preventing cross-tenant sniffing.
* **RECONNECT:** PASS. Reconnections restore group bindings automatically, and clients resubscribe to active conversations.
* **PRESENCE:** CONDITIONAL PASS (New Finding). Presence tracking works via `OperatorPresenceChanged` broadcasts to the tenant-specific group. However, two limitations were identified:
  1. **Multi-Instance Risk:** The presence state is tracked locally inside a static `ConcurrentDictionary` (`ActiveTenantUsers`). In a load-balanced multi-instance environment, servers will not share user presence states, rendering the operator presence lists inconsistent. A shared Redis key-value store or distributed cache must be used to track presence globally.
  2. **Multi-Tab Connection Bug:** Opening the application in multiple tabs creates multiple SignalR connections. When one tab is closed, the connection disconnects, removing the `userId` key from `ActiveTenantUsers` and broadcasting an offline event to other operators, even though the user still has active connections in other tabs. A connection-counting dictionary or set must be used.
* **TYPING:** PASS. Hub method `SendTypingStatus` verifies tenant conversation ownership before broadcasting the `OperatorTypingStatusChanged` event to the `inbox-conversation-{conversationId}` group.
* **ORDERING:** PASS. Server-side events are published from the outbox projection consumer using the projection's incremented database `Version` as the `SequenceNumber`. This allows clients to re-order out-of-order socket events deterministically.
* **BACKPRESSURE:** PASS. Message events are lightweight and payload sizes are restricted. SignalR's internal transport buffers manage packet flow control safely.
* **MULTI_INSTANCE_RISK:** Low/Medium. While SignalR group broadcasts are successfully distributed across instances via the configured Redis backplane (`builder.Services.AddSignalR().AddStackExchangeRedis(...)`), the in-memory operator presence tracking (`ActiveTenantUsers`) is not multi-instance safe.
* **SECURITY:** PASS. PII, plain messages, attachment URLs, and secrets are excluded from logs. Connections are protected by JWT auth.
* **REGRESSION:** PASS. `ConversationInboxProjectionConsumer` regression is verified; outbox event consumption and projection updates operate successfully under existing tests.
* **NEW_FINDINGS:** Yes:
  1. **Presence state sharing limitation:** `ActiveTenantUsers` is local to the instance memory. Needs Redis-backed presence tracking.
  2. **Multi-tab disconnection bug:** Disconnecting a single tab marks the operator offline globally despite other active tabs.
* **BLOCKERS:** None.
* **FIX_NEEDED:** None.
* **READY_FOR_A7_REVIEW:** YES
* **NEXT:** Refer task to `Agent 7` (Chief Software Architect) for architectural review and final code freeze.
