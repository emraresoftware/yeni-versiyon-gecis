# Task 008A Report — Event Bus Hardening / Outbox Fix (Hotfix)

## Objective
Task 008 bağımsız QA incelemesinde tespit edilen kritik bulgu: `OutboxMessage.Create` çağrılarında `tenantId` ve `correlationId` **parametre olarak geçirilmiyordu**. Bu hotfix ile her iki çağrı noktası da düzeltildi ve ek test senarileri eklendi.

## Scope
- `Platform/Persistence/Outbox` — `OutboxWriter`: `ITenantProvider` inject edildi, `tenantId` geçildi
- `Platform/Persistence/DbContext` — `EmareDbContext.CollectDomainEventsToOutbox()`: `_tenantProvider.TenantId` artık her `OutboxMessage.Create` çağrısına iletiliyor
- `Emare.Platform.API.Tests` — Test 6 constructor güncellendi, Test 10 ve Test 11 eklendi
- `Emare.Platform.Persistence.Tests` — Outbox stamp integration testi eklendi

## Bugs Fixed

### Bug 1 — `OutboxWriter.WriteAsync` tenantId geçmiyordu
`OutboxWriter`, `EmareDbContext` içindeki `_tenantProvider`'a erişimi olmadığından `OutboxMessage.Create(eventType, payload)` çağrısında `tenantId = null` bırakıyordu.

**Fix:** `ITenantProvider` constructor injection ile eklendi. `tenantId: _tenantProvider.TenantId == Guid.Empty ? null : _tenantProvider.TenantId` olarak geçildi.

### Bug 2 — `EmareDbContext.CollectDomainEventsToOutbox` tenantId geçmiyordu
`SaveChangesAsync` içinde çalışan outbox toplama metodunda `OutboxMessage.Create(eventType, payload)` çağrısı tenantId olmadan yapılıyordu. Her OutboxMessage `TenantId = null` ile kaydediliyordu.

**Fix:** `_tenantProvider.TenantId` (Guid.Empty ise null) her OutboxMessage.Create çağrısına geçildi.

### Bug 3 — Test 6 OutboxWriter constructor 1 argümanla çalışmıyordu
`OutboxWriter(dbContext)` çağrısı constructor değişikliğinden sonra derleme hatası veriyordu.

**Fix:** `OutboxWriter(dbContext, tenantProvider)` olarak güncellendi.

## Outbox TenantId Akışı (Düzeltilmiş)

```text
Aggregate Domain Event
        ↓
EmareDbContext.SaveChangesAsync()
        ↓
CollectDomainEventsToOutbox()
  → tenantId = _tenantProvider.TenantId (Guid.Empty → null)
  → OutboxMessage.Create(eventType, payload, tenantId)  ← BUG FIX
  → OutboxMessages.Add(msg) — EF tracked
        ↓
base.SaveChangesAsync() — OutboxMessage DB'ye tenantId ile yazılır

  ─ ─ ─ ─ veya ─ ─ ─ ─

OutboxWriter.WriteAsync(domainEvent)
  → tenantId = _tenantProvider.TenantId  ← BUG FIX (ITenantProvider injected)
  → OutboxMessage.Create(eventType, payload, tenantId)
  → OutboxMessages.Add(msg) — EF tracked
```

## Files Modified
- `src/Platform/Persistence/Outbox/OutboxWriter.cs` — ITenantProvider inject, tenantId geçildi
- `src/Platform/Persistence/DbContext/EmareDbContext.cs` — CollectDomainEventsToOutbox tenantId fix
- `tests/Emare.Platform.API.Tests/EventBusTests.cs` — Test 6 fix, Test 10 + Test 11 eklendi
- `tests/Emare.Platform.Persistence.Tests/PersistenceTests.cs` — Outbox stamp integration testi eklendi, Tenant_CanBeSaved assertion güncellendi

## Architecture Decisions
- `correlationId` şimdilik null geçilmektedir. `ICorrelationProvider` gelecek sprint'te eklenecek (Technical Debt olarak kayıt altına alındı).
- `Guid.Empty` kontrolü eklendi: tenant context yokken `TenantId = null` yazılır (fail-safe).

## Build Result
```
Oluşturma başarılı oldu.
    0 Uyarı
    0 Hata
```

## Test Result
```
Başarılı! - Başarısız: 0, Başarılı: 14, Atlanan: 0 — Emare.Platform.Persistence.Tests
Başarılı! - Başarısız: 0, Başarılı: 47, Atlanan: 0 — Emare.Platform.API.Tests
Toplam: 61 test — 0 başarısız
```

## New / Updated Test Scenarios

| Test | Konum | Doğrulama |
|------|-------|-----------|
| Test 6 (güncellendi) | OutboxHardeningTests | OutboxWriter 2-arg constructor artık çalışıyor |
| Test 10 (yeni) | OutboxHardeningTests | OutboxWriter → OutboxMessage.TenantId doğru atanıyor |
| Test 11 (yeni) | OutboxHardeningTests | SaveChangesAsync sonrası DB'de TenantId doğru |
| (yeni) | PersistenceTests | CollectDomainEventsToOutbox gerçek Tenant aggregate ile TenantId stamp testi |
| Tenant_CanBeSaved (güncellendi) | PersistenceTests | `Be(1)` → `BeGreaterThanOrEqualTo(1)` (OutboxMessage side-effect) |

## Performance Notes
- Null-check `Guid.Empty` eklendi — minimal overhead.

## Security Notes
- Herhangi bir hassas veri log'a yazılmıyor.

## Technical Debt
- `correlationId` ambient provider (`ICorrelationProvider`, HttpContext X-Correlation-ID tabanlı) gelecek sprint'te eklenmelidir. Şu an `null` geçiliyor.

## Risks
- Yok.

## Breaking Changes
- `OutboxWriter` constructor imzası değişti: `(EmareDbContext)` → `(EmareDbContext, ITenantProvider)`. DI üzerinden çözümlendiği için runtime'da etkisi yok.

## Next Recommended Task
- Task 009: Rule Engine Skeleton (önceki öneri) **veya** correlationId için `ICorrelationProvider` altyapısı (Technical Debt kapatma).
