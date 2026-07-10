# TASK_MSG_006 — Redis Idempotency & Distributed Lock Implementation Report

## Architecture Details

We migrated the Omnichannel Messaging Core (OMC) to a multi-instance production topology by establishing Redis-backed distributed synchronization structures.

### 1. Redis Idempotency Checker
- **Class**: `RedisMessageIdempotencyChecker` (implementing `IMessageIdempotencyChecker`).
- **Namespace**: `EmareTicket.Infrastructure.Services.Messaging`.
- **Key Pattern**: `msg:idempotency:{tenantHash}:{channel}:{messageHash}`.
- **PII Protection**: Hashes are computed using SHA-256 to ensure raw sender details (such as phone numbers or plain-text values) never leak into Redis keys.
- **Expiry**: Default TTL is configurable via `Messaging:Redis:IdempotencyTtlSeconds` (default: 24 hours).

### 2. Redis Distributed Lock Manager
- **Class**: `RedisDistributedLockManager` (implementing `IDistributedLockManager`).
- **Namespace**: `EmareTicket.Infrastructure.Services.Messaging`.
- **Key Pattern**: `msg:lock:{tenantHash}:{channel}:{externalConversationHash}`.
- **Behavior**: Uses atomic Redis `SET NX PX` to acquire locks, retries with random jitter to prevent lock acquisition storms, and runs an atomic Lua release script to ensure locks are only deleted by their owners.

### 3. InMemory Fallbacks
- **Class**: `InMemoryDistributedLockManager`.
- **Purpose**: Acts as a local thread-safe memory fallback when Redis integration is disabled in configuration.

### 4. Dependency Injection & Configuration
- Connections are managed using a singleton `IConnectionMultiplexer` in `Program.cs`.
- Service registration dynamically swaps between `Redis` and `InMemory` providers based on `Messaging:Redis:Enabled` configuration.
