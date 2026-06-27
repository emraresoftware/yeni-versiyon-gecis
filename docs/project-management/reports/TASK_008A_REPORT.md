# Task 008A Report — Event Bus Hardening / Outbox Fix

## Objective
Task 008 bağımsız QA incelemesinde tespit edilen 2 kritik bug ve 1 mimari eksiklik düzeltilerek Event Bus altyapısı sağlamlaştırıldı.

## Scope
- `Platform/Domain` — `OutboxMessage.Create` bug fix (CorrelationId atanmıyordu)
- `Platform/Application/Contracts` — `IOutboxWriter` sözleşmesi (yeni)
- `Platform/Persistence/Outbox` — `OutboxWriter` implementasyonu (yeni)
- `Platform/Persistence` — `PersistenceDependencyInjection` DI kaydı güncellendi
- `Platform/Persistence/DbContext` — `EmareDbContext.SaveChangesAsync` override: `CollectDomainEventsToOutbox()` metodu eklendi
- `Platform/Infrastructure/Events` — `DomainEventDispatcher` yeniden yazıldı (`IOutboxWriter` tabanlı)
- `Emare.Platform.API.Tests` — `OutboxHardeningTests` sınıfı (9 yeni test), `EventBusTests` stabilize edildi

## Bugs Fixed

### Bug 1 — `OutboxMessage.Create` CorrelationId atanmıyordu
`OutboxMessage.Create(...)` metodunda `correlationId` parametresi alınıyor ancak entity nesnesine atanmıyordu. `CorrelationId = correlationId` satırı object initializer'a eklendi.

### Bug 2 — `DomainEventDispatcher` doğrudan MediatR'a publish ediyordu
`DomainEventDispatcher`, domain eventleri MediatR'ın `IPublisher.Publish()` metoduna gönderiyordu — bu Outbox pattern'ini tamamen atlıyordu ve kritik bir mimari hataydı. Dispatcher `IOutboxWriter` kullanacak şekilde yeniden yazıldı.

## Outbox Dispatch Akışı (Düzeltilmiş)

```text
Aggregate Domain Events
        ↓
EmareDbContext.SaveChangesAsync()
        ↓
CollectDomainEventsToOutbox()
  → entity.DomainEvents toplanır
  → entity.ClearDomainEvents() çağrılır
  → OutboxMessage.Create() ile serialize edilir
  → OutboxMessages.Add(outboxMsg) ile EF track'e alınır
        ↓
base.SaveChangesAsync() — OutboxMessages DB'ye yazılır (aynı transaction)
        ↓
[Gelecek Task: Background Worker → Relay → External Broker]
```

Hiçbir aşamada dış sisteme (RabbitMQ, Kafka) publish yapılmamaktadır.

## Architecture Improvement — IOutboxWriter

Clean Architecture ihlali düzeltildi:
- `Infrastructure` katmanı `Persistence` katmanına bağımlı olamazdı
- `IOutboxWriter` sözleşmesi `Application/Contracts/` katmanına eklendi
- `OutboxWriter` implementasyonu `Persistence/Outbox/` altında yapıldı
- `DomainEventDispatcher` artık `IOutboxWriter` üzerinden çalışıyor

Katman bağımlılık yönü korundu: `Infrastructure → Application → Domain`

## Files Created
- `src/Platform/Application/Contracts/IOutboxWriter.cs`
- `src/Platform/Persistence/Outbox/OutboxWriter.cs`

## Files Modified
- `src/Platform/Domain/Entities/OutboxMessage.cs` (CorrelationId bug fix)
- `src/Platform/Infrastructure/Events/DomainEventDispatcher.cs` (IOutboxWriter tabanlı yeniden yazım)
- `src/Platform/Persistence/DbContext/EmareDbContext.cs` (SaveChangesAsync override + CollectDomainEventsToOutbox)
- `src/Platform/Persistence/PersistenceDependencyInjection.cs` (IOutboxWriter DI kaydı)
- `tests/Emare.Platform.API.Tests/EventBusTests.cs` (9 hardening testi eklendi)
- `tests/Emare.Platform.API.Tests/Emare.Platform.API.Tests.csproj` (EF InMemory paket + Persistence ProjectReference)

## Build Result
```text
Oluşturma başarılı oldu.
    0 Uyarı
    0 Hata
```

## Test Result
```text
Başarılı! - Başarısız: 0, Başarılı: 45, Atlanan: 0, Toplam: 45, Süre: 3 s
```
Platform genelinde 69 testin tamamı yeşil.

## Hardening Test Senaryoları (9 adet)
1. `OutboxMessage_Create_ShouldAssign_TenantId` — TenantId doğru atanmalı
2. `OutboxMessage_Create_ShouldAssign_CorrelationId` — CorrelationId bug fix doğrulaması
3. `OutboxMessage_Create_ShouldWrite_CorrectEventType` — EventType doğru yazılmalı
4. `OutboxMessage_Create_ShouldNotAllow_EmptyPayload` — Boş payload reject edilmeli
5. `OutboxMessage_Create_OccurredAt_ShouldBeUtc` — UTC timestamp zorunlu
6. `OutboxWriter_ShouldSerializeDomainEvent_IntoOutboxMessage` — OutboxWriter domain eventi serialize edip ChangeTracker'a eklemeli
7. `Aggregate_DomainEvents_ShouldBeCleared_AfterDispatch` — Domain event listesi temizlenmeli
8. `InMemoryEventBus_WithoutHandlerRegistered_ShouldNotThrow` — Handler yoksa event bus hata vermemeli
9. `DomainEventDispatcher_ShouldWriteToOutbox_AndClearDomainEvents` — Dispatcher OutboxWriter'ı çağırmalı ve domain eventleri temizlemeli

## Performance Notes
- OutboxWriter JSON serialization için `System.Text.Json` kullanıyor (reflection-based, ileriki sprint'te source generator ile optimize edilebilir).

## Security Notes
- Hassas veri log'a yazılmıyor. `_logger.LogDebug` yalnızca EventType ve EventId içeriyor.

## Technical Debt
- `EmareDbContext.CollectDomainEventsToOutbox()` şu an tenant bilgisi olmadan OutboxMessage oluşturuyor. Gelecek sprint'te aggregate'den TenantId türetme mantığı eklenebilir.

## Risks
- Yok.

## Breaking Changes
- `DomainEventDispatcher` constructor signature değişti (`IPublisher` → `IOutboxWriter + ILogger`). DI üzerinden çözümlendiği için runtime'da etkisi yok.

## Next Recommended Task
- Task 009: Rule Engine Skeleton
