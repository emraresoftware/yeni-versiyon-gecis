# ADR-004 — Event Bus (Event-Driven Architecture)

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS modülleri (CRM, Sales, Finance, HR, Logistics, QC vb.) birbirinin iş akışlarını tetikler ancak doğrudan servis çağrısı ile sıkı coupling oluşturmamalıdır. AI ajanlar, workflow engine, notification engine ve entegrasyon katmanının aynı olay akışına abone olabilmesi için merkezi bir event dağıtım mekanizması gereklidir. `EVENT_BUS.md` bu mimariyi tanımlar.

---

## Decision

Platform **Event-Driven Architecture** benimser. Modüller birbirini doğrudan çağırmaz; **Event Bus** üzerinden haberleşir.

**Event türleri:**

| Tür | Kaynak | Örnek |
|---|---|---|
| **Domain Event** | Aggregate iş kuralı sonucu | `HrLeaveApproved`, `QcTestResultCompleted` |
| **Integration Event** | Modüller arası / dış sistem | `FinanceInvoiceCreated`, `LogisticsShipmentDelivered` |
| **System Event** | Platform kernel | `UserLoggedIn`, `TenantCreated` |

**İsimlendirme standardı:** `EntityAction` formatı; modül prefix zorunlu (`CrmOpportunityCreated`, `FinanceJournalEntryPosted`).

**Event yapısı (minimum alanlar):** `eventId`, `eventType`, `aggregateId`, `aggregateType`, `tenantId`, `userId`, `occurredAt`, `version`, `payload`.

**Yaşam döngüsü kuralları:**

1. Event yalnızca **başarılı transaction commit** sonrasında yayınlanır.
2. Handler'lar **idempotent** olmalıdır (aynı event iki kez işlense aynı sonuç).
3. Başarısız işleme: Retry Queue → 3 deneme → **Dead Letter Queue (DLQ)**.
4. Event versioning desteklenir; eski consumer'lar kırılmadan evrilir.

**Dağıtım:**

- Domain event dispatch: Unit of Work / DbContext commit pipeline.
- Integration event publish: Outbox Pattern (ADR-005) üzerinden.

---

## Consequences

**Pozitif:**

- Gevşek coupling; modüller bağımsız deploy edilebilir.
- AI, workflow, notification aynı event'lere abone olabilir.
- Mikroservis geçişine uygun sınır.

**Negatif:**

- Eventual consistency; UI'da gecikmeli güncelleme yönetimi gerekir.
- Event şema evrimi ve versioning disiplini zorunlu.
- Debug/trace için CorrelationId zorunlu hale gelir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Direct Service Calls (sync)** | Modüller arası sıkı coupling; cascade failure riski. |
| **Shared Database Integration** | Anti-pattern; tenant izolasyonu ve modül sınırları ihlal edilir. |
| **Point-to-Point Messaging** | N modül × M subscriber kombinatorial karmaşıklık. |
| **Kafka-only (başlangıç)** | Operasyonel yük; Outbox + broker evrimi tercih edildi. |

---

## References

- [EVENT_BUS.md](../../../EVENT_BUS.md)
- [DOMAIN_MODEL.md](../../../DOMAIN_MODEL.md)
- [WORKFLOW_ENGINE.md](../../../WORKFLOW_ENGINE.md)
- [CONTROL_TOWER_FINAL_SCOPE.md](../../product/CONTROL_TOWER_FINAL_SCOPE.md)
- [NOTIFICATION_ENGINE.md](../../../NOTIFICATION_ENGINE.md)
