# QA Review — Task 008A Event Bus Hardening

**Task:** 008A — Event Bus Hardening / Outbox Fix  
**Date:** 2026-06-27  
**Reviewer:** Agent 2 (Independent QA)  
**Scope:** Emare BOS — `OutboxMessage`, `OutboxWriter`, `EmareDbContext.CollectDomainEventsToOutbox`, `DomainEventDispatcher`, Event Bus testleri  
**Method:** `dotnet restore/build/test`, kaynak inceleme, Agent 1 `TASK_008A_REPORT.md` ile çapraz doğrulama  
**Kısıt:** Kod değiştirilmedi. Private repo commit/push yapılmadı.

**Referanslar:** `TASK_008A_REPORT.md`, `QA_TASK_008_EVENT_BUS_INDEPENDENT.md` (Task 008 bağımsız inceleme)

---

## Build

**PASS**

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | Başarılı |
| `dotnet build Emare.sln` | **0 hata**, **0 uyarı** |

---

## Tests

**PASS**

| Proje | Geçen | Başarısız | Toplam |
|-------|-------|-----------|--------|
| `Emare.BuildingBlocks.Tests` | 8 | 0 | 8 |
| `Emare.Platform.Domain.Tests` | 10 | 0 | 10 |
| `Emare.Platform.Persistence.Tests` | 14 | 0 | 14 |
| `Emare.Platform.API.Tests` | 47 | 0 | 47 |
| **Toplam** | **79** | **0** | **79** |

Task 008A ile eklenen/güncellenen testler:

| Test | Konum | Sonuç |
|------|-------|-------|
| `OutboxMessage_Create_ShouldAssign_TenantId` | `OutboxHardeningTests` | ✅ |
| `OutboxMessage_Create_ShouldAssign_CorrelationId` | `OutboxHardeningTests` | ✅ |
| `OutboxWriter_ShouldAssign_TenantId_ToOutboxMessage` | `OutboxHardeningTests` | ✅ |
| `DbContext_SaveChangesAsync_ShouldPersistOutboxMessage_WithTenantId` | `OutboxHardeningTests` | ✅ |
| `SaveChangesAsync_CollectDomainEventsToOutbox_ShouldStampTenantId` | `PersistenceTests` | ✅ |
| `DomainEventDispatcher_ShouldWriteToOutbox_AndClearDomainEvents` | `OutboxHardeningTests` | ✅ |

---

## Task 008A Checklist (Özel Kontroller)

| # | Kontrol | Sonuç | Kanıt |
|---|---------|--------|-------|
| 1 | `OutboxMessage.Create` tenantId atıyor mu? | ✅ **Evet** | `OutboxMessage.cs` L38: `TenantId = tenantId`. `OutboxWriter` ve `CollectDomainEventsToOutbox` tenantId geçiriyor. Test 1, 10, 11, PersistenceTests stamp testi geçti. |
| 2 | `OutboxMessage.Create` correlationId atıyor mu? | ⚠️ **Kısmi** | Factory parametre bağlama düzeltildi (`CorrelationId = correlationId`, L39). Unit test geçiyor. **Runtime çağrı noktaları correlationId geçmiyor** — `OutboxWriter` ve `CollectDomainEventsToOutbox` yalnızca 3 argümanlı overload kullanıyor; DB'de `CorrelationId` null kalıyor. |
| 3 | SaveChanges sonrası domain event OutboxMessage'a dönüşüyor mu? | ✅ **Evet** | `EmareDbContext.SaveChangesAsync` → `CollectDomainEventsToOutbox()` → serialize + `OutboxMessages.Add`. Integration test: `SaveChangesAsync_CollectDomainEventsToOutbox_ShouldStampTenantId`. |
| 4 | Aggregate domain event listesi temizleniyor mu? | ✅ **Evet** | `CollectDomainEventsToOutbox`: kopyala → `aggregate.ClearDomainEvents()`. `DomainEventDispatcher`: aynı kalıp. Test: `Aggregate_DomainEvents_ShouldBeCleared_AfterDispatch`, PersistenceTests empty assertion. |
| 5 | Dış publish yapılmıyor mu? (domain → outbox yolu) | ✅ **Evet** | SaveChanges/outbox yolu yalnızca EF `OutboxMessages` insert. Broker/handler invoke yok. `DomainEventDispatcher` yalnızca `IOutboxWriter.WriteAsync` çağırır. |
| 6 | RabbitMQ/Kafka eklenmemiş mi? | ✅ **Evet** | `src/Platform/**` içinde RabbitMQ/Kafka referansı yok. |
| 7 | Background worker eklenmemiş mi? (outbox relay) | ✅ **Evet** | Platform katmanında outbox relay `BackgroundService`/`IHostedService` yok. (Legacy `EmareTicket.BackgroundJobs` ayrı monolit modülü — Task 008A kapsamı dışı.) |
| 8 | `DateTime.Now` var mı? | ✅ **Yok** | `src/Platform/**` taraması: eşleşme yok. `OutboxMessage` → `DateTime.UtcNow`. |
| 9 | `throw new Exception` var mı? | ✅ **Yok** | `src/Platform/**` taraması: eşleşme yok. Validation için `ArgumentException` kullanılıyor. |

---

## Clean Architecture

* **Domain bağımsız mı?** ✅ `OutboxMessage` Domain'de; Infrastructure/Persistence bağımlılığı yok.
* **Infrastructure sızıntısı var mı?** ✅ Outbox yazımı Persistence (`OutboxWriter`, `EmareDbContext`); dispatcher Infrastructure'da `IOutboxWriter` sözleşmesine bağımlı.
* **Controller DbContext kullanıyor mu?** ✅ Event Bus değişikliği controller katmanına taşmamış.

---

## DDD Compliance

* **AggregateRoot / domain event:** ✅ `IHasDomainEvents`, `ClearDomainEvents()` kalıbı doğru.
* **Domain event → outbox:** ✅ SaveChanges pipeline'da toplanıyor (Task 008 independent review'daki UoW boşluğu kapatıldı).
* **Çift yol notu:** `CollectDomainEventsToOutbox` (DbContext) ve `DomainEventDispatcher` (manuel çağrı) paralel mevcut; UoW yalnızca DbContext yolunu kullanıyor — çakışma riski düşük, ancak gelecekte tek giriş noktası tercih edilmeli.

---

## Security

* **DateTime.Now:** ✅ Yok (Platform).
* **throw new Exception:** ✅ Yok (Platform).
* **Hardcoded Secret / Connection String / Tenant:** ✅ Yok.
* **TenantId stamp:** ✅ `ITenantProvider.TenantId`; `Guid.Empty` → null (fail-safe).

---

## Performance

* **SaveChanges içi outbox toplama:** ChangeTracker scan — aggregate sayısına bağlı, kabul edilebilir skeleton maliyeti.
* **Async:** `SaveChangesAsync` async; `OutboxWriter.WriteAsync` senkron add + `Task.CompletedTask` (iyileştirme önerisi, blocker değil).

---

## Persistence

* **Outbox indexleri:** ✅ `ProcessedAt`, `OccurredAt`, `TenantId`, `EventType` — test ile doğrulandı.
* **Tenant:** ✅ OutboxMessage'a tenantId yazılıyor; global filter davranışı test edildi.
* **UTC:** ✅ `OccurredAt` UTC.

---

## API

Task 008A API yüzeyi değiştirmedi — N/A.

---

## Test Coverage

**Yeterli (Task 008A hotfix kapsamı için).**

008A'nın hedeflediği tenantId bug'ı unit + integration test ile kapatılmış. Eksikler:

* End-to-end: gerçek HTTP request → aggregate save → outbox row assertion (API integration).
* `correlationId` runtime stamp testi (ICorrelationProvider gelince).
* Outbox relay worker testi (henüz implementasyon yok).

---

## Critical Issues

1. **CorrelationId runtime'da null** — `OutboxMessage.Create` factory düzgün; `OutboxWriter` ve `CollectDomainEventsToOutbox` correlationId iletmiyor. Task 008A report'ta bilinçli erteleme (`ICorrelationProvider` backlog). **Blocker değil; izlenebilirlik borcu.**

---

## Suggestions

1. `ICorrelationProvider` eklenince hem `OutboxWriter` hem `CollectDomainEventsToOutbox` correlationId geçirmeli.
2. Integration event'ler (`InMemoryEventBus.PublishAsync`) hâlâ outbox bypass — production öncesi integration event → outbox veya transactional outbox relay tasarımı netleştirilmeli (Task 008 inherited).
3. Outbox relay background worker gelecek task'ta eklenecek; `ProcessedAt` / retry mantığı henüz işletilmiyor.
4. `DomainEventDispatcher` ile `CollectDomainEventsToOutbox` tek stratejide birleştirilebilir (mimari sadeleştirme).

---

## Agent 1 Report Cross-Check

| Agent 1 iddiası | Bağımsız doğrulama |
|-----------------|-------------------|
| tenantId bug fix | ✅ Doğrulandı |
| correlationId factory fix | ✅ Doğrulandı (param binding) |
| correlationId runtime | ⚠️ Hâlâ null — report ile uyumlu |
| 61 test yeşil | ⚠️ Güncel toplam **79/79** (test sayısı artmış) |
| Build 0 hata | ✅ Doğrulandı |

---

## Final Verdict

**CONDITIONAL PASS**

**Gerekçe:** Task 008A'nın ana hedefi olan **tenantId outbox stamp** bug'ı düzeltilmiş ve testlerle kanıtlanmış. SaveChanges → outbox → aggregate clear akışı çalışıyor. Platform katmanında broker/worker/DateTime.Now/throw new Exception ihlali yok.

**Koşul:** `correlationId` production çağrı noktalarında hâlü null; `ICorrelationProvider` task'ı tamamlanana kadar izlenmeli. Integration event outbox bypass ve outbox relay worker Task 008 skeleton borcu olarak devam ediyor — Sprint 2+ gate maddesi.

**Sonraki adım:** Chief Architect Review (`ARCHITECT_REVIEW_TASK_008A.md` — yalnızca Chief Architect yazar).

---

*Kod içermez. Hassas veri içermez.*
