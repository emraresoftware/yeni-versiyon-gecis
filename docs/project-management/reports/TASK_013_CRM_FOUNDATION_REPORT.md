# Task 013 Report — CRM Foundation (Domain + Persistence)

## Objective
Emare BOS’un ilk iş alanı olan CRM modülü Domain ve Persistence katmanlarının DDD (Domain-Driven Design), Clean Architecture ve SOLID prensiplerine göre yapılandırılması.

## Scope
- CRM Domain entity'lerinin (`CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal`, `CrmActivity`, `CrmTag`) tasarımı ve geliştirilmesi.
- Entity validation kurallarının ve domain event'lerin kodlanması.
- EF Core konfigürasyonlarının, indekslerinin, query filter ilişkilerinin ve database model eşlemelerinin persistence katmanında yapılandırılması.
- Birim (Unit) ve entegrasyon (Integration) testlerinin yazılarak tenant izolasyonu, soft delete, otomatik denetim (audit) ve outbox entegrasyonlarının doğrulanması.

## Aggregate & Model Kararları (Gerekçeleriyle)

- **CrmAccount (Aggregate Root):** CRM modülünün merkezinde yer alır. Müşteri bilgileri, etiketleri ve bağlı işlemler hesap (Account) üzerinden yönetilir. Kendi bağımsız yaşam döngüsüne sahiptir.
- **CrmOpportunity (Aggregate Root):** Fırsatlar, kendi yaşam aşamalarını (Stage) ve olasılıklarını (Probability) yöneten, hesaplardan bağımsız kapanma ve kazanılma döngüleri bulunan, teklif süreçlerini koordine eden bağımsız iş süreçleri oldukları için Aggregate Root olarak modellenmiştir.
- **CrmProposal (Aggregate Root):** Teklifler, kendi onay/red durumlarını yöneten, geçerlilik süreleri, revizyon numaraları bulunan, bağımsız olarak basılıp müşteriye gönderilen bir iş belgesi olduğu için Aggregate Root olarak tasarlanmıştır.
- **CrmContact, CrmActivity, CrmTag (Logical Entities / Values):**
  - **CrmContact:** Bağımsız bir varlık olamaz. Her zaman bir `CrmAccount` ile ilişkilidir. Logical reference (`CrmAccountId`) ile bağlıdır.
  - **CrmActivity:** Bir hesap veya fırsat etkileşimidir. Kendi başına bir yaşam döngüsü yoktur.
  - **CrmTag:** Sadece diğer nesneleri kategorize etmek için kullanılan paylaşımlı bir niteliktir.

## Cross-Context ve Logical References
Mimari standartlar gereği, modüller arası veya modül içi sıkı bağımlılıkları önlemek için fiziksel Foreign Key navigasyonları (`public CrmAccount Account`) yerine **Logical Reference** (Guid `CrmAccountId`, `CrmOpportunityId`) tercih edilmiştir. Bu sayede modüller kolayca mikroservislere bölünebilir veya izole edilebilir.

---

## Entity Listesi

- `CrmAccount`
- `CrmContact`
- `CrmOpportunity`
- `CrmProposal`
- `CrmActivity`
- `CrmTag`

---

## Event Listesi

- `CrmAccountCreatedDomainEvent`
- `CrmAccountUpdatedDomainEvent`
- `CrmAccountDeletedDomainEvent`
- `CrmOpportunityCreatedDomainEvent`
- `CrmOpportunityStageChangedDomainEvent`
- `CrmProposalCreatedDomainEvent`
- `CrmProposalSentDomainEvent`
- `CrmProposalApprovedDomainEvent`
- `CrmActivityCreatedDomainEvent`

---

## EF Configuration Listesi

- `CrmAccountConfiguration`
- `CrmContactConfiguration`
- `CrmOpportunityConfiguration`
- `CrmProposalConfiguration`
- `CrmActivityConfiguration`
- `CrmTagConfiguration`

### Uygulanan Veritabanı İndeksleri:
- `TenantId + AccountCode` (Unique)
- `TenantId + Name` (Combined Index)
- `TenantId + TaxNumber` (Combined Index)
- `TenantId + Email` (Combined Index)
- `TenantId + Status` (Combined Index)
- `TenantId + CrmAccountId` (Combined Index)
- `TenantId + ProposalNumber` (Unique)

---

## Build Result
- **Command:** `dotnet build Emare.sln`
- **Result:** Başarılı (0 Hata, 0 Uyarı)

## Test Result
Bütün test projeleri başarıyla çalıştırılmış ve 94 testin hepsi yeşil dönmüştür.
- `Emare.Platform.Domain.Tests`: 20/20 passed
- `Emare.Platform.Persistence.Tests`: 19/19 passed
- `Emare.BuildingBlocks.Tests`: 8/8 passed
- `Emare.Platform.API.Tests`: 47/47 passed
- **Total Tests:** 94 / 94 Passed (0 Failed, 0 Skipped)

---

## Technical Debt
- Bulunmamaktadır.

## Sprint 2A Etkisi
Sprint 2A kapsamında geliştirilecek olan Control Tower CEO ve Sales Dashboard API'leri ile frontend ekranlarının ihtiyaç duyduğu temel veri modeli ve persistence altyapısı bu görevle tamamen hazır hale getirilmiştir.
