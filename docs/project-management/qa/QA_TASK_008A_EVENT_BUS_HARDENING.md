# QA Review — Task 008A Event Bus Hardening / Outbox

**Task:** 008A — Event Bus Hardening / Outbox Fix  
**Date:** 2026-06-28  
**Reviewer:** Agent 2 (Independent QA)  
**Scope:** Emare BOS Platform — Outbox pattern, domain event dispatch, `OutboxMessage`, `OutboxWriter`, `EmareDbContext.CollectDomainEventsToOutbox`, `DomainEventDispatcher`, `InMemoryEventBus`  
**Method:** Pre-flight docs + `dotnet restore/build/test` + kaynak inceleme + Agent 1 `TASK_008A_REPORT.md` çapraz doğrulama  
**Kısıt:** Kod değiştirilmedi. Private repo commit/push yapılmadı.

---

## Pre-Flight (Okunan Dokümanlar)

| Doküman | Uyum kontrolü |
|---------|----------------|
| `docs/project-management/AGENTS.md` | Dual-repo QA çıktısı public repoda — uygun |
| `ANAYASA.md` | `DateTime.UtcNow` kuralı — Platform outbox uyumlu |
| `EVENT_BUS.md` | Outbox pattern önerisi; integration event ayrımı — kısmen uyumlu (integration bypass devam) |
| `DOMAIN_MODEL.md` | `OutboxMessage` entity matrisi ile uyumlu |
| `TASK_008A_REPORT.md` | tenantId fix doğrulandı; correlationId runtime iddiası kısmen yanlış |

---

## Build

**PASS**

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | Başarılı |
| `dotnet build Emare.sln` | **0 hata**, 5 uyarı (CA1000 ×4, CA1069 CRM enum — Task 008A dışı) |

---

## Tests

**PASS**

| Proje | Geçen | Başarısız | Toplam |
|-------|-------|-----------|--------|
| `Emare.BuildingBlocks.Tests` | 8 | 0 | 8 |
| `Emare.Platform.Domain.Tests` | 24 | 0 | 24 |
| `Emare.Platform.Persistence.Tests` | 19 | 0 | 19 |
| `Emare.Platform.API.Tests` | 47 | 0 | 47 |
| **Toplam** | **98** | **0** | **98** |

---

## Özel Doğrulama Matrisi

| # | Kontrol | Sonuç | Kanıt |
|---|---------|--------|-------|
| 1 | `OutboxMessage.Create` → `tenantId` | ✅ | L38 `TenantId = tenantId`. Unit test + runtime call sites geçiriyor. |
| 2 | `OutboxMessage.Create` → `correlationId` | ⚠️ Kısmi | L39 parametre binding doğru (unit test). **Runtime call sites geçirmiyor** → DB'de null. |
| 3 | `OutboxWriter` doğru çalışıyor mu? | ✅ | Serialize + `OutboxMessages.Add`; tenantId stamp; test 6/10/11. |
| 4 | `ITenantProvider` empty/null güvenli mi? | ✅ | `Guid.Empty ? null : TenantId` — `OutboxWriter` + `CollectDomainEventsToOutbox`. |
| 5 | Domain Event → Outbox SaveChanges içinde mi? | ✅ | `SaveChangesAsync` → `CollectDomainEventsToOutbox()` → `OutboxMessages.Add` → `base.SaveChangesAsync`. |
| 6 | Transaction sınırı bozulmuş mu? | ✅ | Tek EF `SaveChangesAsync` transaction; outbox insert aynı batch'te. **Not:** sync `SaveChanges()` override yok. |
| 7 | Domain event dış publish yok mu? | ✅ | Outbox yolu broker/handler çağırmıyor. `DomainEventDispatcher` yalnızca `IOutboxWriter`. |
| 8 | Integration event outbox bypass? | ⚠️ **Evet** | `InMemoryEventBus.PublishAsync` doğrudan handler invoke — outbox tablosuna yazmaz (Task 008 skeleton borcu). |
| 9 | Save sonrası aggregate events temiz mi? | ✅ | `ClearDomainEvents()` — `CollectDomainEventsToOutbox` + `DomainEventDispatcher`. |
| 10 | `DateTime.Now` | ✅ | `src/Platform/**` — yok. `OutboxMessage` → `DateTime.UtcNow`. |
| 11 | `throw new Exception` | ✅ | `src/Platform/**` — yok. Factory `ArgumentException` kullanıyor. |
| 12 | RabbitMQ / Kafka / outbox worker | ✅ | Platform katmanında yok. |

---

## Akış Diyagramı (Doğrulanmış)

```text
Aggregate raises IDomainEvent
        ↓
EmareDbContext.SaveChangesAsync()
        ↓
CollectDomainEventsToOutbox()
  • tenantId = ITenantProvider (Empty → null)
  • correlationId = null (bilinçli erteleme)
  • JsonSerializer → payload
  • OutboxMessage.Create(eventType, payload, tenantId)
  • aggregate.ClearDomainEvents()
        ↓
base.SaveChangesAsync()  ← tek transaction
        ↓
OutboxMessages tablosu (ProcessedAt = null, relay bekler)

Alternatif yol:
DomainEventDispatcher → IOutboxWriter.WriteAsync → aynı DbContext (manuel çağrı)
```

---

## Test Kapsamı Matrisi

| Senaryo | Test var mı? | Test adı / konum |
|---------|--------------|------------------|
| **tenantId** — factory | ✅ | `OutboxMessage_Create_ShouldAssign_TenantId` |
| **tenantId** — OutboxWriter | ✅ | `OutboxWriter_ShouldAssign_TenantId_ToOutboxMessage` |
| **tenantId** — SaveChanges persist | ✅ | `DbContext_SaveChangesAsync_ShouldPersistOutboxMessage_WithTenantId` |
| **tenantId** — CollectDomainEvents | ✅ | `SaveChangesAsync_CollectDomainEventsToOutbox_ShouldStampTenantId` |
| **tenantId** — CRM domain event | ✅ | `SaveChangesAsync_CollectCrmDomainEvents_ShouldCreateOutboxMessages` |
| **correlationId** — factory | ✅ | `OutboxMessage_Create_ShouldAssign_CorrelationId` |
| **correlationId** — runtime stamp | ❌ | Eksik — `ICorrelationProvider` sonrası eklenmeli |
| **payload** — serialize / not empty | ✅ | Test 4, 6; CRM outbox payload assertion |
| **event type** — doğru ad | ✅ | Test 3, 6; CRM `CrmAccountCreatedDomainEvent` |
| **UTC** — OccurredAt | ✅ | Test 5, 11, `IntegrationEvent_OccurredAt_ShouldBeUtc` |
| **empty tenant** — null TenantId on outbox | ❌ | Eksik — `Guid.Empty` → outbox `TenantId` null testi yok |
| **multiple domain events** — tek save | ❌ | Eksik — aggregate başına 2+ event senaryosu yok |
| **no direct external publish** — domain | ✅ | `DomainEventDispatcher_ShouldWriteToOutbox_AndClearDomainEvents` (mock) |
| **integration bypass** — bilinçli | ⚠️ | Dokümante borç; negatif test yok |

---

## Clean Architecture & Anayasa

| Kural | Durum |
|-------|--------|
| Domain bağımsızlığı | ✅ `OutboxMessage` Domain'de |
| Persistence → Application sözleşmesi | ✅ `IOutboxWriter` Application.Contracts |
| Infrastructure dispatcher | ✅ `DomainEventDispatcher` → `IOutboxWriter` |
| ANAYASA DateTime UTC | ✅ |
| EVENT_BUS outbox önerisi | ⚠️ Domain path OK; integration path bypass |

---

## Persistence

| Kontrol | Durum |
|---------|--------|
| `OutboxMessages` DbSet | ✅ |
| Index: ProcessedAt, OccurredAt, TenantId, EventType | ✅ Test ile doğrulandı |
| Outbox global tenant filter | N/A — `OutboxMessage` tenant filter dışı (relay için doğru) |

---

## Critical Issues

1. **CorrelationId runtime null** — Factory düzeltildi; `OutboxWriter` / `CollectDomainEventsToOutbox` iletmiyor. Task 008A report bilinçli erteleme ile uyumlu. **Blocker değil.**

2. **Integration event outbox bypass** — `InMemoryEventBus.PublishAsync` skeleton davranışı; production öncesi EVENT_BUS.md ile hizalanmalı.

3. **Sync `SaveChanges()` override yok** — Yalnızca `SaveChangesAsync` outbox toplar; sync çağrı outbox atlar (düşük risk, UoW async kullanıyor).

---

## Agent 1 Report Cross-Check

| Agent 1 iddiası | Bağımsız sonuç |
|-----------------|----------------|
| tenantId bug fix (2 call site) | ✅ Doğrulandı |
| correlationId parametreleri geçiriliyordu ama atanmıyordu → fix | ✅ Factory fix doğru |
| correlationId runtime | ❌ Hâlâ null — report'ta erteleme notu var |
| 61 test | ⚠️ Güncel **98/98** |
| Build 0 uyarı | ⚠️ 5 uyarı (CRM enum — 008A dışı) |

---

## Suggestions

1. `ICorrelationProvider` + outbox correlationId runtime testi.
2. `CollectDomainEventsToOutbox_GuidEmptyTenant_ShouldWriteNullTenantId` testi.
3. `Aggregate_WithMultipleDomainEvents_ShouldCreateMultipleOutboxRows` testi.
4. Integration event → outbox veya transactional relay tasarım kararı (ADR).
5. `SaveChanges()` sync override veya yasaklama (analyzer/rule).
6. Outbox relay worker + `ProcessedAt`/`RetryCount` işletimi (gelecek task).

---

## Final Verdict

**CONDITIONAL PASS**

**Gerekçe:** Task 008A ana hedefi (**tenantId outbox stamp**) düzeltilmiş ve unit/integration testlerle kanıtlanmış. Domain event → outbox → aggregate clear → tek transaction akışı doğru. Platform'da broker/worker/`DateTime.Now`/`throw new Exception` ihlali yok.

**Koşullar (gate):**

- `correlationId` runtime stamp + test eksik
- Integration event outbox bypass devam ediyor
- Outbox relay worker henüz yok
- Test matrisinde empty-tenant-outbox ve multiple-event senaryoları eksik

**Sonraki adım:** Chief Architect Review — `ARCHITECT_REVIEW_TASK_008A.md` (yalnızca Chief Architect yazar).

---

*Kod içermez. Hassas veri içermez.*
