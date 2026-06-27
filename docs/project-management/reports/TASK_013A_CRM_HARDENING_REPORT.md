# Task 013A Report — CRM Foundation Hardening

## Pre-flight Checklist Verification
Before writing any code, the following mandatory standard documents were read and verified:
*   [x] `AGENTS.md` (Checked commands, topologies, and sync flow)
*   [x] `ANAYASA.md` (Enforced Article 1, 2, and 3 constraints)
*   [x] `DOMAIN_MODEL.md` (Checked CRM entity design and context separation)
*   [x] `EVENT_BUS.md` (Aligned domain event names with standard naming rules)
*   [x] `SECURITY_AUTHORIZATION.md` (Identified permissions structure and constants)

---

## Amaç
CRM Domain + Persistence katmanlarındaki mimari ve fonksiyonel eksikleri tamamlayarak QA raporu doğrultusunda modülü **PASS** seviyesine ulaştırmak.

---

## 🏗️ DDD Aggregate Sınırları & Gerekçeleri

-   **`CrmProposalItem` (Child Entity):** Bağımsız bir iş belgesi olan `CrmProposal` Aggregate Root'unun bir parçasıdır. Teklif satırları teklif olmadan anlamsızdır ve teklifin toplam tutarını belirler. Bu nedenle `CrmProposal` aggregate sınırları içinde bir *Child Entity* olarak modellenmiştir.
-   **`CrmContact` ve `CrmActivity` (Logical References / Context Boundaries):**
    -   `CrmContact` ve `CrmActivity` nesneleri kendi başlarına bir Aggregate Root başlatmazlar. `CrmAccount` nesnesi ile logical reference (`CrmAccountId` Guid) üzerinden ilişkilendirilmişlerdir.
    -   Navigasyon property'leri yerine logical references (Guid) tercih edilmiştir. Bu sayede modüller gevşek bağlı (loose coupling) kalmakta, veritabanı kısıtlamaları ve cross-context kilitlenmelerin önüne geçilmektedir.

---

## ⚡ Event İsimlendirme ve Suffix Standardı
`EVENT_BUS.md` ve genel platform standartlarına uyum sağlamak amacıyla:
-   Serileştirme ve mesajlaşma seviyesindeki event tipleri `CrmAccountCreated`, `CrmOpportunityStageChanged`, `CrmProposalSent` şeklinde suffix olmadan eşleşmektedir.
-   C# kodundaki `DomainEvent` suffix'i sadece derleyici seviyesinde tip güvenliğini sağlamak için kullanılan bir **marker (kod içi işaretleyici)**'dir.

---

## 🔒 CRM İzin Seti (Permissions)
Aşağıdaki yetki sabitleri `Emare.Platform.Application.Authorization.Permissions` sınıfına eklenmiştir:
-   `CRM.Account.Read`
-   `CRM.Account.Write`
-   `CRM.Contact.Read`
-   `CRM.Contact.Write`
-   `CRM.Opportunity.Read`
-   `CRM.Opportunity.Write`
-   `CRM.Proposal.Read`
-   `CRM.Proposal.Write`
-   `CRM.Proposal.Approve`
-   `CRM.Activity.Read`
-   `CRM.Activity.Write`

---

## 🛠️ Eklenen Fonksiyonlar ve Alanlar
-   **`CrmAccount` plan boşlukları kapatıldı:**
    -   `Segment` (enum `CrmAccountSegment`: A, B, C, D)
    -   `NpsScore` (0-10 arası kısıtlı tamsayı)
    -   `RiskScore` (0-100 arası kısıtlı tamsayı)
    -   `HealthScore` (0-100 arası kısıtlı tamsayı)
-   **`CrmProposalItem` entity'si eklendi:**
    -   `CrmProposalId` logical reference
    -   `Quantity`, `UnitPrice`, `Currency` alanları eklendi.
    -   `LineTotal` (`Quantity * UnitPrice`) otomatik hesaplanmaktadır.
    -   `CrmProposal` içindeki `Amount` alanı, eklenen satır kalemlerinin toplam `LineTotal` değerine göre otomatik olarak güncellenmektedir.

---

## Build Result
-   **Command:** `dotnet build Emare.sln`
-   **Result:** Başarılı (0 Hata, 0 Uyarı)

## Test Result
Bütün test projeleri başarıyla geçmiştir.
-   `Emare.Platform.Domain.Tests`: 28/28 passed (Yeni segment, NPS/Risk/Health aralık testleri, ProposalItem hesaplama testleri dahil).
-   `Emare.Platform.Persistence.Tests`: 21/21 passed (ProposalItem entegrasyon testleri, permission sabitleri kontrol testleri dahil).
-   `Emare.BuildingBlocks.Tests`: 8/8 passed
-   `Emare.Platform.API.Tests`: 47/47 passed
-   **Total Tests:** 104 / 104 Passed (0 Failed, 0 Skipped)
