# ADR-005 — Transactional Outbox Pattern

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Event Bus mimarisinde (ADR-004) integration event'lerin domain transaction ile atomik yayınlanması gerekir. Doğrudan broker publish ("dual write") senaryosunda DB commit başarılı olup event kaybolabilir veya tam tersi tutarsızlık oluşur. `EVENT_BUS.md` § Event Transaction Kuralı Outbox Pattern kullanımını önerir. Task 008A ile `OutboxMessage` entity, tenantId stamp ve `CollectDomainEventsToOutbox` hardening tamamlanmıştır.

---

## Decision

Integration event yayını **Transactional Outbox Pattern** ile gerçekleştirilir.

**Akış:**

```text
Business Command
      ↓
Domain Event (aggregate)
      ↓
Same DB Transaction:
  1. Entity persist
  2. OutboxMessage insert
      ↓
Commit
      ↓
Outbox Poller (background worker)
      ↓
Event Bus / Message Broker
      ↓
Subscribers
```

**OutboxMessage gereksinimleri:**

- `TenantId`, `CorrelationId`, `EventType`, `Payload`, `OccurredAt`, `ProcessedAt`, `RetryCount` alanları zorunlu.
- Index: `ProcessedAt`, `OccurredAt`, `TenantId`, `EventType`.
- Poller batch size: 100–500; PostgreSQL `FOR UPDATE SKIP LOCKED` ile paralel poller desteği.

**Kurallar:**

1. Integration event **doğrudan broker'a publish edilmez**; önce outbox'a yazılır.
2. Outbox insert ile business entity persist **aynı transaction** içinde olmalıdır.
3. Başarısız publish: retry → DLQ; hiçbir event sessizce kaybolmaz.
4. Outbox payload'da PII/secret maskeleme caller sorumluluğunda; platform redaction guideline uygulanır.

---

## Consequences

**Pozitif:**

- At-least-once delivery garantisi (idempotent consumer ile exactly-once semantiği).
- DB ve event tutarlılığı korunur.
- Retry/DLQ operasyonel görünürlük sağlar.

**Negatif:**

- Outbox tablosu büyür; arşivleme/temizleme job'ı gerekir.
- Eventual latency (poller interval).
- Background worker altyapısı zorunlu.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Direct Publish after Commit** | Race condition; commit sonrası crash'te event kaybı. |
| **Two-Phase Commit (2PC)** | Dağıtık sistemlerde operasyonel karmaşıklık ve performans cezası. |
| **Change Data Capture (CDC)** | Gelecek faz adayı; MVP için outbox yeterli ve kontrol edilebilir. |
| **In-Memory Event Bus only** | Reliable messaging garantisi yok; production uygun değil. |

---

## References

- [EVENT_BUS.md](../../../EVENT_BUS.md)
- [SECURITY_ARCHITECTURE.md](../../../SECURITY_ARCHITECTURE.md)
- [PERFORMANCE_GUIDE.md](../../project-management/performance/PERFORMANCE_GUIDE.md)
- [QA_TASK_008A_EVENT_BUS_HARDENING.md](../../project-management/qa/QA_TASK_008A_EVENT_BUS_HARDENING.md)
