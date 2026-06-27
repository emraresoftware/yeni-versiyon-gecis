# 📋 TASK 013A — Product Traceability Update Report (TASK_013A_PRODUCT_TRACEABILITY_UPDATE.md)

**Title:** CEO & Sales Dashboard Product Traceability Alignment (Post-Fix)  
**Version:** 1.1.0  
**Status:** Approved  
**Owner:** Security & Architecture Team / Agent 3  
**Last Updated:** 2026-06-28  
**Task Number:** TASK 013A  
**Dependencies:** FEATURE_TRACEABILITY_MATRIX.md, SECURITY_AUTHORIZATION.md, CRM_SECURITY_REVIEW_TASK_013A.md  
**Related Documents:** TASK_013_CRM_FOUNDATION_PLAN.md, STATUS.md  

---

## 1. Amaç (Objective)

Bu rapor, **Emare Ai Dashboard** platformunun CRM yetkilendirme ve güvenlik denetimi (Task 013A) sonrasında tespit edilen yetki boşluklarının kapatılması ve [FEATURE_TRACEABILITY_MATRIX.md](file:///Users/emre/yeni-versiyon-gecis/docs/product/FEATURE_TRACEABILITY_MATRIX.md) dökümanındaki tüm veri eşleme satırlarının güncel CRM yetki seti, müşteri segmentleri, NPS ve sağlık/risk skoru değişkenlerine göre hizalanmasını belgelemek amacıyla hazırlanmıştır.

Ayrıca, matristeki tüm tablo satırlarının kullanıcının talep ettiği **`Control Tower | Widget | API | Query/Command | Handler | Entity | Workflow | Event | Permission | Test`** şablonuna uygunluğu doğrulanmıştır.

---

## 2. Detaylı Eşleme & Entegrasyon Başlıkları

### 2.1. CRM Permissions (Yetki Boşluklarının Kapatılması)
`CRM_SECURITY_REVIEW_TASK_013A.md` denetim raporu doğrultusunda resmi matrise eklenen 4 yeni yetki ve bunların izlenebilirlik matrisindeki yerleşimi şöyledir:
-   **`CRM.Opportunity.Read`:** Opportunities Pipeline (Satır 160), Fırsat Sayısı & Değeri (Satır 148), Win Rate (Satır 149), Ortalama Kapanış Süresi (Satır 150) ve Kayıp Fırsat Değeri (Satır 154) sorgularında genel `CRM.Account.Read` yerine en dar yetki prensibiyle (Least Privilege) kullanılmaya başlanmıştır.
-   **`CRM.Opportunity.Write`:** Fırsat oluşturma aksiyon komutu (Satır 171) bu yetkiyle sınırlandırılmıştır.
-   **`CRM.Activity.Read`:** Customer Panel (Satır 137) ve Targets & Performance (Satır 164) üzerinde yer alan müşteri etkileşim geçmişi verileri için bu izin atanmıştır.
-   **`CRM.Activity.Write`:** Arama, mail ve not kaydetme komutları bu yetkiye tabidir.

### 2.2. `CrmProposalItem` (Teklif Kalemi)
Tekliflerin kalem bazlı (Proposal Line Items) izlenebilirliğini sağlamak için:
-   `GET /api/crm/proposals` (Proposals & Quotes) listesinde ve `POST /api/crm/proposals` (Teklif oluşturma) aksiyonunda `CrmProposal` ile birlikte **`CrmProposalItem`** entity'si matrise açıkça eklenmiştir.

### 2.3. Account Segment & NPS
-   **Account Segment (A, B, C, D):** `CrmAccount`'un bir parçası olarak CEO stakeholder paneli, Sales müşteri paneli ve Customer Accounts alt ekranlarında izlenmektedir.
-   **NPS (Net Promoter Score):** CEO KPI NPS kartı (`GetCeoKpiNpsQuery`) veri kaynağı olarak `CrmAccount` ile eşleştirilmiş ve cari güncellemelerinin yansıması için `CrmAccountUpdated` event'i ile ilişkilendirilmiştir.

### 2.4. Customer Risk Score & Customer Health Score
-   **CEO Dashboard:** Risk/Health Score widget'ı (`GetCeoHealthScoresQuery`) şirket genel skorunun yanında `CrmAccount` (Müşteri riskleri) verilerini de izleyecek şekilde güncellenmiştir.
-   **Sales Dashboard:** `Customer Risk Score & Customer Health Score` widget'ı (`GetSalesHealthScoresQuery`) müşteri risk derecesini ve fırsatların durumlarını `CrmAccount` ve `CrmOpportunity` üzerinden besleyecek şekilde kurgulanmıştır.

---

## 3. Güncellenen Matris Satırları (Format Uyumlu)

Aşağıdaki satırlar **`Control Tower | Widget | API | Query/Command | Handler | Entity | Workflow | Event | Permission | Test`** formatına göre düzenlenmiştir:

| Control Tower | Widget | API | Query/Command | Handler | Entity | Workflow | Event | Permission | Test |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **CEO** | Risk / Health Score (Company & Customer) | `GET /api/control-tower/ceo/health-scores` | `GetCeoHealthScoresQuery` | `GetCeoHealthScoresQueryHandler` | `CompanyHealthScore`, `DepartmentScorecard`, `CrmAccount` | — | `PerformanceKPIValueUpdated`, `CrmAccountUpdated` | `CEO.ControlTower.View` | `GetCeoHealthScoresQueryHandlerTests` |
| **CEO** | Customer Panel (segment, NPS, risk, health) | `GET /api/control-tower/ceo/stakeholders` | `GetCeoStakeholderPanelsQuery` | `GetCeoStakeholderPanelsQueryHandler` | `CrmAccount`, `DepartmentScorecard` | — | `CrmAccountCreated`, `CrmAccountUpdated` | `CRM.Account.Read`, `CEO.ControlTower.View` | `GetCeoStakeholderPanelsQueryHandlerTests` |
| **CEO** | KPI — Net Promoter Score (NPS) | `GET /api/control-tower/ceo/kpis/nps` | `GetCeoKpiNpsQuery` | `GetCeoKpiNpsQueryHandler` | `CrmAccount`, `KPIValue` | — | `PerformanceKPIValueUpdated`, `CrmAccountUpdated` | `CEO.ControlTower.View`, `CRM.Account.Read` | `GetCeoKpiNpsQueryHandlerTests` |
| **Sales** | Customer Risk Score & Customer Health Score | `GET /api/control-tower/sales/health-scores` | `GetSalesHealthScoresQuery` | `GetSalesHealthScoresQueryHandler` | `CrmAccount`, `CrmOpportunity` | — | `CrmOpportunityCreated`, `CrmAccountUpdated` | `Sales.ControlTower.View` | `GetSalesHealthScoresQueryHandlerTests` |
| **Sales** | Customer Panel (segment, status) | `GET /api/control-tower/sales/customers` | `GetSalesCustomerPanelQuery` | `GetSalesCustomerPanelQueryHandler` | `CrmAccount`, `CrmActivity` | — | `CrmAccountCreated`, `CrmAccountUpdated` | `CRM.Account.Read`, `CRM.Activity.Read` | `GetSalesCustomerPanelQueryHandlerTests` |
| **Sales** | Opportunities Pipeline | `GET /api/crm/opportunities` | `ListCrmOpportunitiesQuery` | `ListCrmOpportunitiesQueryHandler` | `CrmOpportunity`, `CrmAccount` | — | `CrmOpportunityCreated` | `CRM.Opportunity.Read` | `ListCrmOpportunitiesQueryHandlerTests` |
| **Sales** | Proposals & Quotes | `GET /api/crm/proposals` | `ListCrmProposalsQuery` | `ListCrmProposalsQueryHandler` | `CrmProposal`, `CrmProposalItem` | `CrmProposalApproval` | `CrmProposalCreated` | `CRM.Proposal.Read` | `ListCrmProposalsQueryHandlerTests` |
| **Sales** | Customer Accounts (segment, status) | `GET /api/crm/accounts` | `ListCrmAccountsQuery` | `ListCrmAccountsQueryHandler` | `CrmAccount`, `CrmContact` | — | `CrmAccountCreated`, `CrmAccountUpdated` | `CRM.Account.Read` | `ListCrmAccountsQueryHandlerTests` |
| **Sales** | Targets & Performance | `GET /api/sales/targets` | `ListSalesTargetsQuery` | `ListSalesTargetsQueryHandler` | `SalesTarget`, `CrmActivity` | — | `PerformanceKPIValueUpdated` | `Sales.ControlTower.View`, `CRM.Activity.Read` | `ListSalesTargetsQueryHandlerTests` |
| **Sales** | Fırsat oluşturma | `POST /api/crm/opportunities` | `CreateCrmOpportunityCommand` | `CreateCrmOpportunityCommandHandler` | `CrmOpportunity` | — | `CrmOpportunityCreated` | `CRM.Opportunity.Write` | `CreateCrmOpportunityCommandHandlerTests` |
| **Sales** | Teklif oluşturma | `POST /api/crm/proposals` | `CreateCrmProposalCommand` | `CreateCrmProposalCommandHandler` | `CrmProposal`, `CrmProposalItem` | — | `CrmProposalCreated` | `CRM.Proposal.Write` | `CreateCrmProposalCommandHandlerTests` |
| **Sales** | Teklif onayı | `POST /api/crm/proposals/{id}/approve` | `ApproveCrmProposalCommand` | `ApproveCrmProposalCommandHandler` | `CrmProposal` | `CrmProposalApproval` | `CrmProposalApproved` | `CRM.Proposal.Approve` | `ApproveCrmProposalCommandHandlerTests` |
