# 📋 TASK 013 — CRM Foundation Planning (TASK_013_CRM_FOUNDATION_PLAN.md)

**Title:** Sprint 2A — CRM Foundation & Control Tower Planning  
**Version:** 1.0.0  
**Status:** Approved  
**Owner:** Security & Architecture Team / Agent 3  
**Last Updated:** 2026-06-28  
**Dependencies:** CONTROL_TOWER_FINAL_SCOPE.md, FEATURE_TRACEABILITY_MATRIX.md  
**Related Documents:** DOMAIN_MODEL.md, SECURITY_AUTHORIZATION.md, EVENT_BUS.md  

---

## 1. Sprint 2A Amacı

Sprint 2A'nın temel amacı; **Emare Ai Dashboard** platformunun CRM modülü çekirdek yapısını (CRM Foundation) kurmak ve bu altyapıyı `CONTROL_TOWER_FINAL_SCOPE.md` ve `FEATURE_TRACEABILITY_MATRIX.md` standartlarında tanımlanan **CEO Control Tower** ve **Sales Control Tower** ekranlarındaki ilgili KPI, snapshot ve veri paneli bileşenlerine bağlamaktır. 

Bu süreçte:
- Çok kiracılı (multi-tenant) izolasyon kurallarına,
- CQRS (Command Query Responsibility Segregation) desenine,
- `Module.Resource.Action` standardındaki rol/yetkilendirme şemasına,
- Outbox destekli Event-Driven mimari standartlarına tam uyum sağlanacaktır.

---

## 2. CRM Foundation Kapsamı

CRM Foundation, platformun müşteri ilişkileri ve satış boru hattı (sales pipeline) yönetiminin temelini oluşturur. Kapsam aşağıdaki bileşenleri içerir:

*   **Müşteri ve Cari Yönetimi (CrmAccount):** Kiracıya (Tenant) bağlı kurumsal müşterilerin segmentasyonu, finansal ve demografik kartlarının yönetimi.
*   **İletişim Noktaları (CrmContact):** Cari hesaplara bağlı yetkili kişiler ve iletişim matrisi.
*   **Satış Fırsatı Takibi (CrmOpportunity):** Satış boru hattındaki fırsatların aşamalı (stage-by-stage) olarak izlenmesi, beklenen ciro değerlerinin analizi.
*   **Teklif ve Fiyatlandırma Yönetimi (CrmProposal & CrmProposalItem):** Fırsatlardan veya doğrudan müşteriye özel hazırlanan, onay akışlarına tabi tekliflerin oluşturulması ve takibi.
*   **Aktivite ve İletişim Logları (CrmActivity):** Müşteriler ve fırsatlarla ilgili yapılan telefon görüşmesi, e-posta, toplantı ve notların tarihsel olarak kayıt altına alınması.

*Teknik Alt Yapı Kapsamı:*
- Tüm veri tabanı kalıcı modellerinde `Guid TenantId` ve `bool IsDeleted` (Soft Delete) kolonlarının bulunması.
- EF Core `HasQueryFilter` seviyesinde otomatik kiracı izolasyonu.
- Kritik nesnelerde optimistic concurrency (`RowVersion` token) kullanımı.
- Kayıt oluşturma/düzenlemede otomatik `Audit` interceptorlarının çalışması.

---

## 3. CEO Control Tower ile Bağlantılar

CEO Control Tower ekranının CRM modülünden besleneceği noktalar şunlardır:

| CEO Widget | Bağlantılı CRM Bileşeni | Gerekli Veri / Aggregation | İlgili API & Query |
|---|---|---|---|
| **KPI — Aktif Müşteri Sayısı** | `CrmAccount` | Aktif kiracıya ait toplam `CrmAccount` sayısı | `GET /api/control-tower/ceo/kpis/active-customers` <br> `GetCeoKpiActiveCustomersQuery` |
| **KPI — Net Promoter Score (NPS)** | `CrmAccount` | Cari kartlarda güncellenen NPS skorlarının tenant bazlı ağırlıklı ortalaması | `GET /api/control-tower/ceo/kpis/nps` <br> `GetCeoKpiNpsQuery` |
| **Customer / Supplier Panel** | `CrmAccount` | Top 10 müşteri listesi (ciro ve segment bazlı listeleme) | `GET /api/control-tower/ceo/stakeholders` <br> `GetCeoStakeholderPanelsQuery` |
| **Today's Priorities & Alerts** | `CrmAccount` / `QcClaim` | Çözülmemiş kritik müşteri eskalasyonları veya geciken büyük cari riskler | `GET /api/control-tower/ceo/priorities/today` <br> `GetCeoTodayPrioritiesQuery` |

---

## 4. Sales Control Tower ile Bağlantılar

Sales Control Tower, CRM modülünün birincil operasyonel ve analitik izleme merkezidir. Bağlantı matrisi şu şekildedir:

| Sales Widget / Ekran | Bağlantılı CRM Bileşeni | Beklenen Veri / İş Mantığı | İlgili API, Query & Command |
|---|---|---|---|
| **KPI — Aktif Fırsat Sayısı & Değeri** | `CrmOpportunity` | `Stage` değeri `Won` veya `Lost` dışındaki fırsatların toplam sayısı ve tahmini bütçe değerleri (`EstimatedValue`) | `GET /api/control-tower/sales/kpis/active-opportunities` <br> `GetSalesKpiActiveOpportunitiesQuery` |
| **KPI — Win Rate (%)** | `CrmOpportunity` | Belirli periyotta `Won` statüsüne geçen fırsatların toplam kapalı fırsatlara oranı | `GET /api/control-tower/sales/kpis/win-rate` <br> `GetSalesKpiWinRateQuery` |
| **KPI — Ortalama Kapanış Süresi** | `CrmOpportunity` | Fırsat oluşturulma tarihi ile `Won`/`Lost` olma tarihi arasındaki gün farkı ortalaması | `GET /api/control-tower/sales/kpis/avg-close-days` <br> `GetSalesKpiAvgCloseDaysQuery` |
| **KPI — Teklife Dönüşüm Oranı** | `CrmProposal` / `CrmOpportunity` | Teklife dönüştürülen fırsat adetlerinin toplam fırsat adetlerine oranı | `GET /api/control-tower/sales/kpis/proposal-conversion` <br> `GetSalesKpiProposalConversionQuery` |
| **KPI — Kayıp Fırsat Değeri** | `CrmOpportunity` | `Stage` değeri `Lost` olan fırsatların toplam `EstimatedValue` değeri | `GET /api/control-tower/sales/kpis/lost-opportunity-value` <br> `GetSalesKpiLostOpportunityValueQuery` |
| **Opportunities Pipeline** | `CrmOpportunity` | Satış hunisi (funnel) görseli için aşamalara (`New`, `Qualification`, `Proposal`, `Negotiation`) göre gruplanmış fırsatlar | `GET /api/crm/opportunities` <br> `ListCrmOpportunitiesQuery` |
| **Proposals & Quotes** | `CrmProposal` | Kiracı genelindeki tekliflerin durumları (`Draft`, `Sent`, `Approved`, `Rejected`) ile listesi | `GET /api/crm/proposals` <br> `ListCrmProposalsQuery` |
| **Customer Accounts** | `CrmAccount` | Cari hesapların listelenmesi, yeni eklenmesi ve detaylarının izlenmesi | `GET /api/crm/accounts` <br> `ListCrmAccountsQuery` |

---

## 5. Gerekli Entity Adayları

Tüm entity adayları `Guid TenantId` ve `bool IsDeleted` alanlarını içerecektir. Modül sınırlarını korumak için referanslar GUID bazlı logical key'ler ile kurulacaktır.

### 5.1. `CrmAccount` (Aggregate Root)
*   **Id:** `Guid`
*   **TenantId:** `Guid`
*   **CompanyName:** `string` (max: 200)
*   **TaxOffice:** `string` (max: 100)
*   **TaxNumber:** `string` (max: 11)
*   **Email:** `string` (max: 150)
*   **Phone:** `string` (max: 20)
*   **Address:** `string` (max: 500)
*   **Segment:** `CrmSegment` (Enum: `A`, `B`, `C`, `D`)
*   **Status:** `CrmAccountStatus` (Enum: `Active`, `Inactive`, `Lead`)
*   **NpsScore:** `decimal` (0 - 10 aralığında)
*   **Contacts:** `ICollection<CrmContact>`
*   **Opportunities:** `ICollection<CrmOpportunity>`
*   **RowVersion:** `byte[]` (Optimistic Concurrency)

### 5.2. `CrmContact` (Entity)
*   **Id:** `Guid`
*   **TenantId:** `Guid`
*   **CrmAccountId:** `Guid` (Logical FK to CrmAccount)
*   **FirstName:** `string` (max: 50)
*   **LastName:** `string` (max: 50)
*   **Title:** `string` (max: 100)
*   **Email:** `string` (max: 150)
*   **Phone:** `string` (max: 20)
*   **IsPrimaryContact:** `bool`

### 5.3. `CrmOpportunity` (Entity)
*   **Id:** `Guid`
*   **TenantId:** `Guid`
*   **CrmAccountId:** `Guid` (Logical FK to CrmAccount)
*   **Title:** `string` (max: 150)
*   **Description:** `string` (max: 1000)
*   **EstimatedValue:** `decimal` (tahmini satış cirosu)
*   **Stage:** `CrmOpportunityStage` (Enum: `New`, `Qualification`, `Proposal`, `Negotiation`, `Won`, `Lost`)
*   **CloseDate:** `DateTime?`
*   **AssignedOwnerId:** `Guid?` (İlgili satış temsilcisi User ID'si)

### 5.4. `CrmProposal` (Aggregate Root)
*   **Id:** `Guid`
*   **TenantId:** `Guid`
*   **CrmAccountId:** `Guid` (Logical FK to CrmAccount)
*   **CrmOpportunityId:** `Guid?` (Logical FK to CrmOpportunity)
*   **ProposalNumber:** `string` (Sistem tarafından otomatik üretilen format: teklif-YYYYMM-XXXX, benzersiz)
*   **ValidUntil:** `DateTime` (Teklif geçerlilik son tarihi)
*   **TotalAmount:** `decimal`
*   **Status:** `CrmProposalStatus` (Enum: `Draft`, `Sent`, `Approved`, `Rejected`, `Expired`)
*   **Items:** `ICollection<CrmProposalItem>`
*   **RowVersion:** `byte[]`

### 5.5. `CrmProposalItem` (Entity)
*   **Id:** `Guid`
*   **TenantId:** `Guid`
*   **CrmProposalId:** `Guid` (Logical FK to CrmProposal)
*   **ProductCode:** `string` (max: 50)
*   **ProductName:** `string` (max: 250)
*   **Quantity:** `decimal`
*   **UnitPrice:** `decimal`
*   **DiscountRate:** `decimal` (yüzde cinsinden)
*   **TaxRate:** `decimal` (örn: 20.0)
*   **LineTotal:** `decimal` (hesaplanan değer: (Qty * Price * (1 - Discount)) * (1 + Tax))

### 5.6. `CrmActivity` (Aggregate Root / Entity)
*   **Id:** `Guid`
*   **TenantId:** `Guid`
*   **CrmAccountId:** `Guid` (Logical FK to CrmAccount)
*   **CrmContactId:** `Guid?` (Logical FK to CrmContact)
*   **Type:** `CrmActivityType` (Enum: `Call`, `Email`, `Meeting`, `Task`, `Note`)
*   **Subject:** `string` (max: 200)
*   **Description:** `string` (max: 2000)
*   **ActivityDate:** `DateTime`

---

## 6. Gerekli API Adayları

API'ler Clean Architecture doğrultusunda Controller katmanında `ApiResponse<T>` sarmalıyla dönecektir.

*   `GET /api/crm/accounts` (Sayfalanmış, filtrelenmiş cari listesi)
*   `POST /api/crm/accounts` (Yeni cari hesap oluşturma)
*   `GET /api/crm/accounts/{id}` (Cari hesap detayı, altındaki contacts ve activities listesiyle birlikte)
*   `PUT /api/crm/accounts/{id}` (Cari hesap güncelleme)
*   `DELETE /api/crm/accounts/{id}` (Cari hesap soft delete)
*   `POST /api/crm/accounts/{id}/contacts` (Cari hesaba yeni iletişim kişisi ekleme)
*   `GET /api/crm/opportunities` (Pipeline aşamalarına göre fırsat listesi)
*   `POST /api/crm/opportunities` (Yeni fırsat oluşturma)
*   `PUT /api/crm/opportunities/{id}/stage` (Fırsat satış hunisi aşamasını güncelleme)
*   `GET /api/crm/proposals` (Sayfalanmış teklif listesi)
*   `POST /api/crm/proposals` (Yeni teklif ve satırlarını oluşturma)
*   `POST /api/crm/proposals/{id}/approve` (Teklif durumu 'Approved' yapılması ve onay akışı)
*   `POST /api/crm/proposals/{id}/reject` (Teklif durumu 'Rejected' yapılması)
*   `POST /api/crm/activities` (Yeni müşteri aktivitesi kaydetme)

---

## 7. Gerekli Query/Command Adayları (CQRS)

CQRS mimarisi gereği her Handler tek sorumluluğa sahip olacaktır. Okuma verileri DTO (Data Transfer Object) üzerinden dönecektir.

### 7.1. Queries (Sorgular)
*   `ListCrmAccountsQuery` -> `Result<PagedList<CrmAccountDto>>`
*   `GetCrmAccountDetailQuery` -> `Result<CrmAccountDetailDto>`
*   `ListCrmOpportunitiesQuery` -> `Result<List<CrmOpportunityDto>>`
*   `ListCrmProposalsQuery` -> `Result<PagedList<CrmProposalDto>>`
*   `ListCrmActivitiesQuery` -> `Result<List<CrmActivityDto>>`
*   `GetCeoKpiActiveCustomersQuery` -> `Result<int>`
*   `GetCeoKpiNpsQuery` -> `Result<decimal>`
*   `GetSalesKpiActiveOpportunitiesQuery` -> `Result<SalesOpportunityKpiDto>`
*   `GetSalesKpiWinRateQuery` -> `Result<decimal>`
*   `GetSalesKpiAvgCloseDaysQuery` -> `Result<decimal>`
*   `GetSalesKpiProposalConversionQuery` -> `Result<decimal>`
*   `GetSalesKpiLostOpportunityValueQuery` -> `Result<decimal>`

### 7.2. Commands (Komutlar)
*   `CreateCrmAccountCommand` -> `Result<Guid>`
*   `UpdateCrmAccountCommand` -> `Result<bool>`
*   `DeleteCrmAccountCommand` -> `Result<bool>`
*   `CreateCrmContactCommand` -> `Result<Guid>`
*   `CreateCrmOpportunityCommand` -> `Result<Guid>`
*   `UpdateCrmOpportunityStageCommand` -> `Result<bool>`
*   `CreateCrmProposalCommand` -> `Result<Guid>`
*   `ApproveCrmProposalCommand` -> `Result<bool>`
*   `RejectCrmProposalCommand` -> `Result<bool>`
*   `CreateCrmActivityCommand` -> `Result<Guid>`

---

## 8. Gerekli Permission Adayları

İzin yapıları `SECURITY_AUTHORIZATION.md` standartlarında deklaratif `[Authorize(Permissions.xxx)]` yapısıyla korunacaktır.

*   `CRM.Account.Read` (Cari hesap listeleme ve detay görüntüleme)
*   `CRM.Account.Write` (Cari hesap oluşturma, düzenleme, silme)
*   `CRM.Contact.Read` (İletişim kişilerini listeleme)
*   `CRM.Contact.Write` (İletişim kişisi ekleme/düzenleme)
*   `CRM.Opportunity.Read` (Fırsat hunisi ve fırsat detaylarını görüntüleme)
*   `CRM.Opportunity.Write` (Fırsat ekleme, aşama güncelleme)
*   `CRM.Proposal.Read` (Teklifleri okuma)
*   `CRM.Proposal.Write` (Teklif oluşturma/düzenleme)
*   `CRM.Proposal.Approve` (Teklif onaylama yetkisi - SalesManager, TenantAdmin, CEO)
*   `CRM.Activity.Read` (Müşteri etkinlik günlüklerini okuma)
*   `CRM.Activity.Write` (Telefon/mail günlük girişi yapma)

---

## 9. Gerekli Domain Event Adayları

Olaylar `{ModuleEntity}{Action}` formatında tanımlanarak DbContext SaveInterceptor'ı üzerinden Outbox tablosuna yazılacak ve asenkron yayınlanacaktır.

*   `CrmAccountCreated` (Yeni müşteri cari kaydı eklendiğinde)
*   `CrmAccountUpdated` (Cari kart bilgiisi veya NPS skoru değiştiğinde)
*   `CrmContactCreated` (İletişim kişisi atandığında)
*   `CrmOpportunityCreated` (Yeni satış fırsatı girildiğinde)
*   `CrmOpportunityStageChanged` (Fırsat aşaması Won/Lost vb. güncellendiğinde)
*   `CrmProposalCreated` (Yeni teklif taslağı hazırlandığında)
*   `CrmProposalApproved` (Teklif onaylandığında -> Outbox ile Sipariş/Fatura modüllerini tetikler)
*   `CrmProposalRejected` (Teklif reddedildiğinde)
*   `CrmActivityCreated` (Yeni müşteri faaliyeti sisteme loglandığında)

---

## 10. Test Senaryoları (Tests)

xUnit + FluentAssertions + NSubstitute mimari test standartlarında yazılacak negatif ve pozitif test blokları şunlardır:

### 10.1. Tenant Isolation Tests (Kiracı İzolasyon Testleri)
*   `ListCrmAccounts_ShouldOnlyReturnAccountsForActiveTenant`
    *   *Senaryo:* Sistemde Tenant A ve Tenant B verileri mevcutken, Tenant A kullanıcısı cari listesini istediğinde sadece Tenant A verileri dönmelidir.
*   `GetCrmAccount_WithIdFromAnotherTenant_ShouldReturnNotFoundError`
    *   *Senaryo:* Tenant A kullanıcısı, HTTP isteği ile Tenant B'ye ait bir `CrmAccountId` sorguladığında 404 Not Found veya 403 Forbidden dönmelidir.
*   `CreateCrmAccount_ShouldForceActiveTenantIdFromContext`
    *   *Senaryo:* Client'tan gelen istek parametrelerinde farklı bir tenant_id yazsa dahi, Command Handler veriyi kaydederken HTTP Context claim'indeki aktif `TenantId` değerini zorla atamalıdır.

### 10.2. Business Logic Tests (İş Mantığı Testleri)
*   `CreateCrmOpportunity_WithNegativeEstimatedValue_ShouldReturnValidationError`
    *   *Senaryo:* Fırsat oluşturulurken tahmini değer sıfırdan küçük girildiğinde FluentValidation pipeline'da hata vermeli ve DB'ye yazılmamalıdır.
*   `ApproveCrmProposal_WithStatusDraft_ShouldSuccessfullyApprove`
    *   *Senaryo:* Taslak ('Draft') durumundaki geçerli bir teklif onaylandığında durumu 'Approved' olmalıdır.
*   `ApproveCrmProposal_AlreadyApprovedProposal_ShouldReturnValidationError`
    *   *Senaryo:* Durumu zaten 'Approved' olan bir teklif tekrar onaylanmaya çalışıldığında iş kuralları gereği hata fırlatmalı, transaction durdurulmalıdır.
*   `CreateCrmProposal_ValidUntilDateInPast_ShouldReturnValidationError`
    *   *Senaryo:* Geçerlilik tarihi geçmişe ait (past date) olan bir teklif oluşturulmak istendiğinde validasyon engeline takılmalıdır.

### 10.3. Transactional Outbox Tests (Event ve Outbox Testleri)
*   `CreateCrmAccount_ShouldPublishCrmAccountCreatedEventToOutbox`
    *   *Senaryo:* Cari hesap oluşturma transaction'ı bittiğinde, `CrmAccountCreated` domain event'i aynı transaction sınırları içerisinde `OutboxMessages` tablosuna yazılmış olmalıdır.
*   `ApproveCrmProposal_ShouldPublishCrmProposalApprovedEventWithinSameTransaction`
    *   *Senaryo:* Teklif onaylandığında oluşacak `CrmProposalApproved` olayı, teklif tablosundaki update işlemiyle aynı ACID transaction'da outbox'a kaydedilmelidir.

---

## 11. Acceptance Criteria (Kabul Kriterleri)

Bir CRM Foundation kod/özellik tesliminin (Definition of DoD) kabul edilmesi için aşağıdaki kriterleri tam sağlaması gerekir:

1.  **Strict Tenant Isolation:** Tüm veri okuma (Query) ve veri yazma (Command) süreçlerinde `ITenantProvider` aracılığıyla çözümlenen `TenantId` filtresi zorunlu kullanılacaktır. API dış parametresinden `TenantId` alınmayacaktır.
2.  **API Authorization:** Hazırlanan tüm Controller endpoint'lerinde ilgili permission attribute kontrolü (`[Authorize(Permissions.CRM.xxx)]`) bulunacaktır.
3.  **FluentValidation Pipeline:** Eksik veya geçersiz DTO istekleri handler'a girmeden pipeline seviyesinde (FluentValidation ile) kesilip standart `ProblemDetails` olarak dönecektir.
4.  **Audit Integrity:** Cari hesap, fırsat ve teklif aggregate'lerinde CRUD işlemlerinin tamamı EF Core Interceptor seviyesinde `CreatedBy`, `CreatedAt`, `UpdatedBy` ve `UpdatedAt` alanlarını dolduracaktır.
5.  **Optimistic Concurrency:** `CrmAccount` ve `CrmProposal` tablolarında eşzamanlı güncellemeleri önlemek için `RowVersion` kontrolü çalışır durumda olacaktır.
6.  **Outbox Integration:** Kritik domain event'ler veritabanına yazılırken kesinlikle doğrudan dış mesaj kuyruğuna publish edilmeyecek; db save transaction'ında Outbox tablosuna yazılacaktır.
7.  **Clean Architecture Directory:** Tüm CRM sınıfları mimari katman bağımlılıklarına uyacaktır (`Domain` -> `Application` -> `Persistence` / `Infrastructure` -> `API`).
