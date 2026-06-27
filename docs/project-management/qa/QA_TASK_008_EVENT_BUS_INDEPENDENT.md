# QA Review — Task 008 Event Bus Skeleton — Independent Review

**Reviewer:** Agent 2 (Independent QA)  
**Date:** 2026-06-27  
**Scope:** Emare BOS — Event Bus abstractions, InMemoryEventBus, DomainEventDispatcher, OutboxMessage  
**Method:** `dotnet restore/build/test`, kaynak inceleme, Agent 1 `QA_TASK_008.md` ile çapraz doğrulama  
**Kısıt:** Kod değiştirilmedi. Private repo commit/push yapılmadı.

**Referanslar:** `TASK_008_REPORT.md`, `QA_TASK_008.md` (Agent 1 — bu inceleme bağımsızdır)

---

## Build Result

**PASS**

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | Başarılı |
| `dotnet build Emare.sln` | **0 hata**, 4 uyarı (CA1000 — BuildingBlocks generic static factory) |

---

## Test Result

**PASS**

| Proje | Geçen | Başarısız | Toplam |
|-------|-------|-----------|--------|
| `Emare.BuildingBlocks.Tests` | 8 | 0 | 8 |
| `Emare.Platform.Domain.Tests` | 10 | 0 | 10 |
| `Emare.Platform.Persistence.Tests` | 13 | 0 | 13 |
| `Emare.Platform.API.Tests` | 38 | 0 | 38 |
| **Toplam** | **69** | **0** | **69** |

Event Bus testleri: `EventBusTests.cs` — 9 senaryo (UTC, handler, no-handler, multi-handler, dispatcher clear, outbox create, outbox UTC, DbSet, EF index).

---

## Event Bus Findings

| Bileşen | Durum | Not |
|---------|--------|-----|
| `IEventBus` / `IEventHandler<T>` | ✅ | Integration event sözleşmesi BuildingBlocks'ta |
| `IIntegrationEvent` / `IntegrationEvent` | ✅ | `EventId`, `TenantId`, `OccurredAt`, `CorrelationId`, `Version` |
| `InMemoryEventBus` | ✅ | Subscribe/Unsubscribe, scoped handler resolve |
| DI (`AddEventBus`) | ✅ | Singleton bus, scoped dispatcher — Infrastructure DI |
| RabbitMQ / Kafka | ✅ Yok | Platform katmanında mesaj broker bağımlılığı yok |
| Background Worker (Outbox) | ✅ Yok | Task 008 skeleton kapsamı; Task Report'ta borç olarak not edilmiş |

**Handler yokken:** `PublishAsync` exception fırlatmaz, warning log + return — test ile doğrulandı.

**Multiple handler:** Aynı event'e iki handler subscribe — her ikisi de invoke edilir — test ile doğrulandı.

**Eksik:** Production'da handler'ların otomatik kaydı yok; `Subscribe<,>()` manuel çağrı bekliyor (skeleton).

---

## Domain Event Dispatch Findings

| Kontrol | Sonuç |
|---------|--------|
| Domain event doğrudan dış sisteme publish | ✅ Hayır — `DomainEventDispatcher` yalnızca MediatR `IPublisher` kullanır |
| Dispatch sonrası aggregate temizliği | ✅ `ClearDomainEvents()` dispatch öncesi kopya + clear — unit test (mock MediatR) |
| `OccurredAt` UTC | ✅ `DomainEvent` base → `DateTime.UtcNow` |
| UoW / SaveChanges entegrasyonu | ❌ `UnitOfWork.SaveChangesAsync` dispatcher çağırmıyor — domain event'ler otomatik dağıtılmıyor |
| MediatR handler gerçek entegrasyon testi | ⚠️ Yalnızca mock; end-to-end domain handler yok |

**Sonuç:** Dispatcher modülü doğru izole; **üretim akışına bağlanmamış** (beklenen skeleton sınırı, ancak Task 009+ gate).

---

## Outbox Findings

| Kontrol | Sonuç |
|---------|--------|
| `OutboxMessage` entity | ✅ AggregateRoot, factory `Create`, `MarkAsProcessed` / `MarkAsFailed` |
| `OutboxMessageConfiguration` | ✅ Tablo, index: `ProcessedAt`, `OccurredAt`, `TenantId`, `EventType` |
| `EmareDbContext.OutboxMessages` | ✅ DbSet kayıtlı |
| Outbox olmadan Integration Event publish | ⚠️ **Evet** — `InMemoryEventBus.PublishAsync` doğrudan handler çağırır; outbox tablosuna yazmaz |
| Outbox → EventBus köprüsü | ❌ Yok (worker/processor yok) |
| `OccurredAt` UTC | ✅ `DateTime.UtcNow` |
| **`TenantId` taşınması (Create)** | ❌ **Bug** — `Create(..., tenantId, ...)` parametresi entity'ye atanmıyor |
| **`CorrelationId` taşınması (Create)** | ❌ **Bug** — parametre entity'ye atanmıyor |
| Payload hassas veri | ⚠️ Serbest JSON string; redaction/encryption yok — bilinçli skeleton riski |
| Persistence test (outbox insert) | ❌ Yalnızca model/index testi; DB'ye yazım testi yok |

Agent 1 QA "CorrelationId ve TenantId verified" iddiası — **testler bu alanları assert etmiyor**; bağımsız kod incelemesi atama eksikliğini gösteriyor.

---

## Transaction Boundary Findings

| Kontrol | Sonuç |
|---------|--------|
| Transactional Outbox pattern | ❌ Uygulanmamış — DB commit + outbox insert atomik değil |
| Integration publish + DB aynı transaction | ❌ |
| Domain dispatch + SaveChanges sırası | ❌ Tanımlı değil |

Skeleton için kabul edilebilir; production event güvenilirliği için **bloklayıcı follow-up**.

---

## Security Findings

| Kontrol | Sonuç |
|---------|--------|
| `DateTime.Now` (Platform Event Bus) | ✅ Yok |
| `throw new Exception` | ✅ Yok — `OutboxMessage.Create` → `ArgumentException`; bus handler hataları loglanır |
| Hardcoded secret / connection string | ✅ Event Bus modülünde yok |
| Outbox payload PII/secrets | ⚠️ Caller sorumluluğunda; platform seviyesinde maskeleme yok |

---

## Performance Findings

| Kontrol | Sonuç |
|---------|--------|
| Outbox index'ler | ✅ Sorgu kolonları index'li |
| InMemoryEventBus reflection `Invoke` | ⚠️ Handler dispatch reflection ile — skeleton OK, yük altında optimize edilebilir |
| Handler loop sequential `await` | ⚠️ Çok handler'da sıralı; paralel değil |

---

## Test Coverage Gaps

Agent 1 raporu "tam kapsam" demiş; bağımsız inceleme eksikleri:

1. `OutboxMessage.Create` — `TenantId` / `CorrelationId` assert (bug yakalanmamış)
2. Outbox persist + reload (SQLite integration)
3. `DomainEventDispatcher` + gerçek MediatR handler (mock dışı)
4. `UnitOfWork` save sonrası dispatch davranışı
5. Transactional outbox (same-transaction write)
6. Integration event publish → outbox row oluşturma (gelecek task)
7. Handler exception propagation politikası (bus swallow vs fail)
8. `IntegrationEvent.CorrelationId` constructor ile taşıma testi

---

## Critical Issues

1. **C1 — `OutboxMessage.Create` metadata bug:** `tenantId` ve `correlationId` parametreleri nesneye set edilmiyor; trace/tenant izolasyonu outbox'ta kırık.
2. **C2 — Agent 1 QA ile gerçeklik farkı:** `QA_TASK_008.md` Critical/Suggestions "None" — bağımsız inceleme C1 ve entegrasyon boşluklarını tespit etti.
3. **C3 — Integration Event outbox bypass:** Publish doğrudan in-memory; reliable messaging garantisi yok (skeleton kapsamında bilinen, ancak yanlışlıkla prod'da kullanılırsa veri kaybı riski).

---

## Suggestions

1. Agent 1: `OutboxMessage.Create` içinde `TenantId = tenantId`, `CorrelationId = correlationId` ataması + test assert.
2. `UnitOfWork` veya EF interceptor: `SaveChanges` sonrası `IDomainEventDispatcher.DispatchAndClearAsync`.
3. Outbox writer abstraction: integration publish önce outbox'a yaz (Task 009+).
4. Handler auto-registration (assembly scan) veya explicit module bootstrap.
5. Outbox payload için hassas alan redaction guideline (SECURITY_ARCHITECTURE uyumu).
6. Agent 1 QA şablonunda "verified" ifadeleri için zorunlu assert listesi.

---

## Final Verdict

# CONDITIONAL PASS

**Gerekçe:** Event Bus skeleton (abstractions, InMemoryEventBus, DomainEventDispatcher, Outbox entity/EF) build/test gate'ini geçiyor; kritik skeleton davranışları (no-handler, multi-handler, UTC, aggregate clear) test edilmiş. Ancak bağımsız inceleme **`OutboxMessage.Create` TenantId/CorrelationId bug'ını** tespit etti; transactional outbox ve UoW dispatch entegrasyonu yok; Integration Event outbox'sız publish ediliyor. Agent 1 PASS raporu bu bulguları yansıtmıyor.

**Gate:** C1 düzeltilmeden Outbox production kullanımına geçilmemeli. Architect Review'da skeleton vs production-ready ayrımı netleştirilmeli.

---

*Agent 1 rapor:* `qa/QA_TASK_008.md` — Independent verdict farklı: **CONDITIONAL PASS** vs Agent 1 **PASS**
