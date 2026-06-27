# Task 008 Report

## Objective
Bu görevin amacı, Emare BOS Platformu için Event Bus iskeleti, Domain Event dispatch altyapısı ve Outbox message hazırlık yapısının Clean Architecture ve DDD kuralları çerçevesinde kurulmasıdır.

## Scope
- `BuildingBlocks/Common` katmanı (IIntegrationEvent, IntegrationEvent, IEventBus, IEventHandler, IDomainEventDispatcher)
- `Platform/Domain` katmanı (OutboxMessage entity)
- `Platform/Persistence` katmanı (EmareDbContext DbSet, OutboxMessageConfiguration ve index tanımları)
- `Platform/Infrastructure` katmanı (InMemoryEventBus, DomainEventDispatcher, DI registration)
- `Emare.Platform.API.Tests` (Event Bus ve dispatcher test senaryoları)

## Files Created
- [IIntegrationEvent.cs](file:///Users/emre/Elyafgroup/src/BuildingBlocks/Common/Events/IIntegrationEvent.cs)
- [IntegrationEvent.cs](file:///Users/emre/Elyafgroup/src/BuildingBlocks/Common/Events/IntegrationEvent.cs)
- [IEventBus.cs](file:///Users/emre/Elyafgroup/src/BuildingBlocks/Common/Events/IEventBus.cs)
- [IEventHandler.cs](file:///Users/emre/Elyafgroup/src/BuildingBlocks/Common/Events/IEventHandler.cs)
- [IDomainEventDispatcher.cs](file:///Users/emre/Elyafgroup/src/BuildingBlocks/Common/Events/IDomainEventDispatcher.cs)
- [OutboxMessage.cs](file:///Users/emre/Elyafgroup/src/Platform/Domain/Entities/OutboxMessage.cs)
- [OutboxMessageConfiguration.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/Configurations/OutboxMessageConfiguration.cs)
- [InMemoryEventBus.cs](file:///Users/emre/Elyafgroup/src/Platform/Infrastructure/Events/InMemoryEventBus.cs)
- [DomainEventDispatcher.cs](file:///Users/emre/Elyafgroup/src/Platform/Infrastructure/Events/DomainEventDispatcher.cs)
- [EventBusDependencyInjection.cs](file:///Users/emre/Elyafgroup/src/Platform/Infrastructure/Events/EventBusDependencyInjection.cs)
- [EventBusTests.cs](file:///Users/emre/Elyafgroup/tests/Emare.Platform.API.Tests/EventBusTests.cs)

## Files Modified
- [EmareDbContext.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/DbContext/EmareDbContext.cs) (OutboxMessages DbSet eklendi)
- [DependencyInjection.cs (Infrastructure)](file:///Users/emre/Elyafgroup/src/Platform/Infrastructure/DependencyInjection.cs) (Event Bus DI kaydı eklendi)
- [Emare.Platform.API.Tests.csproj](file:///Users/emre/Elyafgroup/tests/Emare.Platform.API.Tests/Emare.Platform.API.Tests.csproj) (NSubstitute paket bağımlılığı eklendi)

## Architecture Decisions
- **Outbox Message Tasarımı:** Outbox mesajları generic/sistem olaylarını desteklemek adına nullable `TenantId` barındırır. Payload, olay türünden bağımsız olarak JSON string biçiminde saklanır.
- **Sıfır Bağımlılıkla Outbox:** `OutboxMessage` entity'si `AggregateRoot` türevidir. Persistence katmanı ile sıkı sıkıya bağlı DbContext sorgulamaları yerine Generic Repository ve Specification desenleri kullanılarak altyapıda bağımsızlık korunmuştur.
- **Güvenli Otonom Olay Dağıtımı (No-op Fallback):** Event Bus üzerinde herhangi bir event için kayıtlı handler bulunmadığında sistem hata fırlatmaz, sessizce (no-op) başarıyla tamamlanır. Aynı olaya birden fazla handler'ın abone olması (multiple subscribers) desteklenmiştir.

## Dependencies Added
- `NSubstitute` v5.1.0 (Test projesinde mock işlemlerini kolaylaştırmak için)

## Build Result
```text
Oluşturma başarılı oldu.
    0 Uyarı
    * Not: generic tip uyarıları (CA1000) BuildingBlocks sonuç kütüphanesindedir.
    0 Hata
```

## Test Result
```text
Başarılı!  - Başarısız:     0, Başarılı:    38, Atlanan:     0, Toplam:    38, Süre: 2 s - Emare.Platform.API.Tests.dll (net8.0)
```
Platform genelindeki toplam 69 testin tamamı sıfır hata ve sıfır başarısızlıkla geçmiştir.

## Performance Notes
- `OutboxMessage` tablosunda `ProcessedAt`, `OccurredAt`, `TenantId` ve `EventType` alanlarına performans artırıcı indexler eklenmiştir.

## Security Notes
- `OutboxMessage` nesnesinin oluşum anı UTC olarak set edilir. Olaylar arasında correlation ve trace bütünlüğünü korumak adına correlationId ve tenantId taşınır.

## Technical Debt
- Outbox mesajlarının arka planda işlenmesi için (Background Worker) ilerleyen fazlarda Inbox/Outbox Worker altyapısı yazılmalıdır.

## Risks
- Yok.

## Known Limitations
- Yok.

## Breaking Changes
- Yok.

## Next Recommended Task
- Task 009: Rule Engine Skeleton
