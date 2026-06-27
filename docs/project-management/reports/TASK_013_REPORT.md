# Task 013 Report — CRM Foundation

## Objective
Platformun ilk gerçek iş alanı olan CRM modülünün Domain ve Persistence katmanlarının DDD (Domain-Driven Design), Clean Architecture ve SOLID prensiplerine uygun olarak kurulması.

## Scope
- CRM Domain entity'lerinin (`CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal`, `CrmActivity`, `CrmTag`) tasarımı ve geliştirilmesi.
- Entity validation kurallarının ve domain event'lerin kodlanması.
- Entity Framework Core konfigürasyonlarının, indekslerinin, query filter ilişkilerinin ve database model eşlemelerinin persistence katmanında yapılandırılması.
- Birim (Unit) ve entegrasyon (Integration) testlerinin yazılarak tenant izolasyonu, soft delete, otomatik denetim (audit) ve outbox entegrasyonlarının doğrulanması.

## Files Created
- `src/Platform/Domain/Enums/CrmEnums.cs`
- `src/Platform/Domain/Events/CrmEvents.cs`
- `src/Platform/Domain/Entities/Crm/CrmTag.cs`
- `src/Platform/Domain/Entities/Crm/CrmAccount.cs`
- `src/Platform/Domain/Entities/Crm/CrmContact.cs`
- `src/Platform/Domain/Entities/Crm/CrmOpportunity.cs`
- `src/Platform/Domain/Entities/Crm/CrmProposal.cs`
- `src/Platform/Domain/Entities/Crm/CrmActivity.cs`
- `src/Platform/Persistence/Configurations/CrmTagConfiguration.cs`
- `src/Platform/Persistence/Configurations/CrmAccountConfiguration.cs`
- `src/Platform/Persistence/Configurations/CrmContactConfiguration.cs`
- `src/Platform/Persistence/Configurations/CrmOpportunityConfiguration.cs`
- `src/Platform/Persistence/Configurations/CrmProposalConfiguration.cs`
- `src/Platform/Persistence/Configurations/CrmActivityConfiguration.cs`
- `tests/Emare.Platform.Domain.Tests/Crm/CrmDomainTests.cs`
- `tests/Emare.Platform.Persistence.Tests/Crm/CrmPersistenceTests.cs`

## Files Modified
- `src/Platform/Persistence/DbContext/EmareDbContext.cs` (6 yeni DbSet eklendi)

## Architecture Decisions
- **Inheritance & Multi-Tenancy:** Tüm 6 CRM entity'si `BaseAuditableEntity` sınıfından türetilmiştir. Bu sayede `ISoftDelete`, `IHasTenant`, `IAuditable` ve `IConcurrencyTracked` davranışları otomatik olarak kazanılmıştır.
- **Tenant Context Isolation:** Core platform standardına (örn: `ApplicationUser`) uyularak, tüm entity'lerin factory metotlarında (`Create`) `Guid tenantId` parametresi zorunlu kılınmış ve `Guid.Empty` doğrulaması eklenmiştir.
- **Many-to-Many Tags:** `CrmAccount` ve `CrmTag` arasındaki many-to-many ilişkisi EF Core implicit join tablosu (`CrmAccountTags`) kullanılarak yapılandırılmıştır.
- **Financial Calculations:** `CrmProposal` net değeri (`NetValue`), `Value * (1 - DiscountRate/100)` formülüyle domain katmanında factory ve güncelleme metotları içinde tutarlı bir şekilde hesaplanmaktadır.
- **Database Index Optimization:** Tenant bazlı sorguların performansını artırmak amacıyla tenantId ile kombine edilmiş çoklu indeksler (`new { TenantId, AccountId }`, `new { TenantId, Email }` vb.) eklenmiştir.

## Dependencies Added
- Yok.

## Build Result
- **Command:** `dotnet build Emare.sln`
- **Result:** Başarılı (0 Hata, 0 Uyarı)

## Test Result
Bütün test projeleri ayrı ayrı ve tümüyle başarıyla geçmiştir.
- `Emare.Platform.Domain.Tests`: 24/24 passed (18 CRM domain test)
- `Emare.Platform.Persistence.Tests`: 19/19 passed (5 CRM persistence integration test)
- `Emare.BuildingBlocks.Tests`: 8/8 passed
- `Emare.Platform.API.Tests`: 47/47 passed
- **Total Tests:** 98 / 98 Passed (0 Failed, 0 Skipped)

## Performance Notes
- `CrmAccount` ve `CrmContact` üzerindeki Email ve LastName/FirstName alanlarına indexler tanımlanmıştır.
- `CrmOpportunity` ve `CrmProposal` tablolarındaki finansal kolonlar (`EstimatedValue`, `Value`, `NetValue`) SQL Server/Postgres veri hassasiyeti için `HasPrecision(18, 2)` olarak konfigüre edilmiştir.

## Security Notes
- Tüm sorgularda EF Core global query filter ile kiracı izolasyonu (`TenantId == currentTenantId`) aktiftir. Testlerde Tenant A kullanıcısının Tenant B verilerine erişemediği izole entegrasyon testleriyle doğrulanmıştır.
- Dokümantasyonda ve kodlarda hiçbir gizli bilgi, connection string, şifre bulunmamaktadır.

## Technical Debt
- Yok.

## Risks
- Yok.

## Known Limitations
- Modül veri tabanı şeması ve testleri için SQLite In-Memory sağlayıcısı kullanılmıştır. PostgreSQL migrations adımları deployment öncesinde persistence startup-project'inde çalıştırılmalıdır.

## Breaking Changes
- Yok.

## Next Recommended Task
- Sprint 2A CRM API handlers ve Query/Command CQRS yapılandırması (Task 014 veya CRM Application Services).
