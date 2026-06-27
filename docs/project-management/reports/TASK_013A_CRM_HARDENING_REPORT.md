# TASK 013A — CRM Foundation Hardening Report

## Pre-flight Checklist
- [x] AGENTS.md okundu
- [x] ANAYASA.md okundu
- [x] DOMAIN_MODEL.md okundu
- [x] EVENT_BUS.md okundu
- [x] SECURITY_AUTHORIZATION.md okundu

## Yapılan Değişiklikler
1. **CrmProposalItem Eklendi:**
   - `CrmProposalId`, `Description`, `Quantity`, `UnitPrice`, `Currency`, `LineTotal` alanları eklendi.
   - `CrmProposal` altında child entity olarak ilişkilendirildi.
   - `CrmProposalItemConfiguration` içinde `TenantId` ve `CrmProposalId` alanları için ayrı indeksler tanımlandı.
2. **CrmAccount Plan Boşlukları Kapatıldı:**
   - Account segment alanı (`Segment` enum), NPS/müşteri memnuniyeti alanı (`NpsScore`), müşteri risk skoru (`RiskScore`) ve müşteri sağlık skoru (`HealthScore`) alanları eklendi.
   - NPS skoru (0-10), risk skoru (0-100) ve sağlık skoru (0-100) için aralık doğrulama kısıtlamaları uygulandı.
3. **CRM İzinleri Tamamlandı:**
   - `Permissions.cs` içinde `CRM.Account.Read/Write`, `CRM.Contact.Read/Write`, `CRM.Opportunity.Read/Write`, `CRM.Proposal.Read/Write/Approve`, `CRM.Activity.Read/Write` yetki sabitleri tanımlandı.

## Event Suffix Açıklaması
- Kod içi event ismi: `CrmAccountCreatedDomainEvent`
- EVENT_BUS karşılığı: `CrmAccountCreated`
- `DomainEvent` suffix'i yalnızca C# kod içi marker'ıdır (derleyici seviyesinde tip güvenliği için). Gerçek event bus ve outbox Payload üzerinde `CrmAccountCreated` olarak serileştirilir.

## DDD Aggregate / Child Entity Gerekçesi
- **Aggregate Root Sınırları:** `CrmAccount`, `CrmOpportunity` ve `CrmProposal` bağımsız iş döngülerine sahip oldukları için Aggregate Root'tur.
- **CrmProposalItem (Child Entity):** Teklif satır kalemleri (`CrmProposalItem`), teklifin (`CrmProposal`) gövdesi olmadan tek başına var olamaz. Bu nedenle `CrmProposal` aggregate'inin bir parçasıdır ve child entity olarak modellenmiştir.
- **CrmContact ve CrmActivity (Logical References):** Modüller arası gevşek bağımlılığı korumak amacıyla `CrmAccount` ile fiziksel navigasyon yerine `CrmAccountId` (Guid) logical reference üzerinden bağlanmışlardır.

## Build/Test Sonucu
- **Build Durumu:** Başarılı (`dotnet build Emare.sln` -> 0 Hata, 0 Uyarı)
- **Test Durumu:** Başarılı (`dotnet test Emare.sln` -> 104/104 Passed)
  - `CrmProposalItem` line total doğrulaması test edildi.
  - NPS (0-10), Risk (0-100) ve Health (0-100) aralık validasyonları sınır değerleriyle (boundary tests) test edildi.
  - CRM permission constants doğruluğu persistence testlerinde kontrol edildi.
