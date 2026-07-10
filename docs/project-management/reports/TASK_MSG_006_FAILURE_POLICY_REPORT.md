# TASK_MSG_006 — Redis Idempotency & Distributed Lock Failure Policy Report

## Failure Policies for Redis Unavailability

This document defines the system behaviors and strategies when the Redis instance becomes unavailable or throws connection exceptions.

### 1. Message Idempotency Checker
- **Mode `FailClosed` (Production Default)**:
  - If Redis is down, `RedisMessageIdempotencyChecker` throws the original connection exception to the caller.
  - The webhook handler catches the exception and returns an HTTP error code (e.g. 500), forcing the message sender (such as WhatsApp/Meta webhook servers) to retry delivery later.
  - This ensures that under no circumstances can double-processing or state corruption occur.
- **Mode `FailOpen` (Development / Test Fallback)**:
  - Configured by setting `Messaging:Redis:FailureMode` to `FailOpen` in appsettings.
  - If Redis is down, the checker logs a warning and returns `false` (assuming the message has not been processed).
  - This allows developers or CI pipelines to run code successfully without needing a local Redis instance.

### 2. Distributed Locking Manager
- **Strategy**: Always **`FailClosed`** for all database writing operations.
- **Behavior**:
  - When Redis is down, `RedisDistributedLockManager` catches the exception and wraps it in a fatal `InvalidOperationException`.
  - The active webhook transaction immediately aborts and rolls back.
  - This is necessary because if a lock cannot be verified, processing the request could lead to concurrent conversation duplicates, split-brain messaging states, or multiple threads creating duplicate participant entities.
  - To prevent state corruption, we reject the request (Fail-Closed) and await retry.
