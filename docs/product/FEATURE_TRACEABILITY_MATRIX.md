# Feature Traceability Matrix — Elyaf Control Towers

**Task:** 009 — Product Engineering  
**Versiyon:** 1.0.0  
**Durum:** Approved for Sprint 2 Gate  
**Sahip:** Agent 2 (Product Traceability)  
**Son Güncelleme:** 2026-06-27  
**Kapsam:** CEO · Sales · Finance Control Tower (Sprint 2A / 2B)

---

## Amaç

Müşteri Control Tower ekranlarını (`CONTROL_TOWER_FINAL_SCOPE.md`) teknik geliştirme planına bağlar.  
Her widget için **ekran → API → handler → entity → workflow → event → permission → test** izlenebilirliği sağlanır.

**Bu doküman kod değildir.** Uygulama sprint'lerinde doğrulanır.

---

## Referanslar

| Doküman | Kullanım |
|---------|----------|
| `docs/product/CONTROL_TOWER_FINAL_SCOPE.md` v1.1.0 | Widget, KPI, menü kapsamı |
| `docs/product/LOCALIZATION_I18N_STANDARDS.md` | UI/API mesaj i18n (`controlTower.{tower}.*`) |
| `DOMAIN_MODEL.md` | Entity / aggregate adları |
| `EVENT_BUS.md` | Domain event adlandırma (`{ModuleEntity}{Action}`) |
| `SECURITY_AUTHORIZATION.md` | `Module.Resource.Action` permission |
| `WORKFLOW_ENGINE.md` | Onay / SLA workflow tanımları |

---

## Adlandırma sözleşmesi

| Katman | Kalıp |
|--------|--------|
| API Endpoint | `GET/POST /api/...` |
| Query | `Get{Resource}Query`, `List{Resource}Query` |
| Command | `{Action}{Entity}Command` |
| Handler | `{QueryOrCommand}Handler` |
| Domain Event | `CrmProposalApproved`, `FinanceJournalEntryPosted` vb. |
| Test (unit) | `{Handler}Tests` |
| Test (API) | `{Tower}ControlTowerApiTests` |

---

## 1. CEO Control Tower

**Scope referansı:** `CONTROL_TOWER_FINAL_SCOPE.md` §1  
**Base permission:** `CEO.ControlTower.View`  
**Menü rotaları:** Executive Overview · Strategic Decisions · Company Health Score · Department Scorecards · Budget vs Actuals · Key Risk Indicators · Board Reports

### Shell & ortak kontroller

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| CEO | Sol dikey menü + kule geçişleri | `GET /api/control-tower/ceo/navigation` | `GetCeoNavigationQuery` | `GetCeoNavigationQueryHandler` | — (RBAC) | — | — | `CEO.ControlTower.View` | `GetCeoNavigationQueryHandlerTests` |
| CEO | Rol bazlı kullanıcı / profil alanı | `GET /api/control-tower/ceo/profile` | `GetCeoProfileContextQuery` | `GetCeoProfileContextQueryHandler` | `User`, `Role` | — | `UserLoggedIn` | `CEO.ControlTower.View` | `GetCeoProfileContextQueryHandlerTests` |
| CEO | Export / Filter / Date controls | `GET /api/control-tower/ceo/export` | `ExportCeoDashboardQuery` | `ExportCeoDashboardQueryHandler` | read models | — | — | `CEO.ControlTower.View` | `CeoControlTowerApiTests` |
| CEO | Legend / status açıklamaları | `GET /api/control-tower/ceo/status-legend` | `GetCeoStatusLegendQuery` | `GetCeoStatusLegendQueryHandler` | — (i18n) | — | — | `CEO.ControlTower.View` | `GetCeoStatusLegendQueryHandlerTests` |

### Standart dashboard widget'ları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| CEO | Executive Snapshot | `GET /api/control-tower/ceo/snapshot` | `GetCeoExecutiveSnapshotQuery` | `GetCeoExecutiveSnapshotQueryHandler` | `ExecutiveDashboardSnapshot`, `CompanyHealthScore` | — (read projection) | `PerformanceKPIValueUpdated` | `CEO.ControlTower.View` | `GetCeoExecutiveSnapshotQueryHandlerTests` |
| CEO | Today's Priorities | `GET /api/control-tower/ceo/priorities/today` | `GetCeoTodayPrioritiesQuery` | `GetCeoTodayPrioritiesQueryHandler` | `DecisionLog`, `FinanceInvoice`, `QcClaim` | — | `CeoDecisionLogCreated`, `FinanceInvoiceCreated`, `QcClaimCreated` | `CEO.DecisionLog.Read`, `Finance.Invoice.Read`, `QC.Claim.Read` | `GetCeoTodayPrioritiesQueryHandlerTests` |
| CEO | Critical Alerts | `GET /api/control-tower/ceo/alerts/critical` | `GetCeoCriticalAlertsQuery` | `GetCeoCriticalAlertsQueryHandler` | `CompanyHealthScore`, `ProductionWorkOrder`, `FinancePayment` | — | `ProductionWorkOrderCreated`, `FinancePaymentCompleted` | `CEO.ControlTower.View` | `GetCeoCriticalAlertsQueryHandlerTests` |
| CEO | Notifications | `GET /api/control-tower/ceo/notifications` | `GetCeoNotificationsQuery` | `GetCeoNotificationsQueryHandler` | `AuditLog` | — | `CeoDecisionLogApproved` | `CEO.ControlTower.View` | `GetCeoNotificationsQueryHandlerTests` |
| CEO | Risk / Health Score | `GET /api/control-tower/ceo/health-scores` | `GetCeoHealthScoresQuery` | `GetCeoHealthScoresQueryHandler` | `CompanyHealthScore`, `DepartmentScorecard` | — | `PerformanceKPIValueUpdated` | `CEO.ControlTower.View` | `GetCeoHealthScoresQueryHandlerTests` |
| CEO | Customer / Supplier / Department Panel | `GET /api/control-tower/ceo/stakeholders` | `GetCeoStakeholderPanelsQuery` | `GetCeoStakeholderPanelsQueryHandler` | `CrmAccount`, `DepartmentScorecard` | — | `CrmAccountCreated` | `CRM.Account.Read`, `CEO.ControlTower.View` | `GetCeoStakeholderPanelsQueryHandlerTests` |
| CEO | Message Drafts | `GET /api/control-tower/ceo/message-drafts` | `GetCeoMessageDraftsQuery` | `GetCeoMessageDraftsQueryHandler` | message draft projection | — | — | `CEO.DecisionLog.Write`, `AI.Copilot.Use` | `GetCeoMessageDraftsQueryHandlerTests` |
| CEO | Calendar & Key Events | `GET /api/control-tower/ceo/calendar` | `GetCeoCalendarEventsQuery` | `GetCeoCalendarEventsQueryHandler` | calendar projection | — | — | `CEO.ControlTower.View` | `GetCeoCalendarEventsQueryHandlerTests` |
| CEO | Next 7 Days Focus | `GET /api/control-tower/ceo/focus/next-7-days` | `GetCeoNext7DaysFocusQuery` | `GetCeoNext7DaysFocusQueryHandler` | `BudgetTarget`, `DecisionLog` | — | `CeoDecisionLogCreated` | `CEO.ControlTower.View` | `GetCeoNext7DaysFocusQueryHandlerTests` |
| CEO | Reports & Analytics | `GET /api/control-tower/ceo/reports` | `GetCeoReportsCatalogQuery` | `GetCeoReportsCatalogQueryHandler` | reporting metadata | — | — | `CEO.ControlTower.View`, `Finance.JournalEntry.Read` | `GetCeoReportsCatalogQueryHandlerTests` |

### KPI kartları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| CEO | KPI — Aylık Ciro (Gerçek vs Hedef) | `GET /api/control-tower/ceo/kpis/monthly-revenue` | `GetCeoKpiMonthlyRevenueQuery` | `GetCeoKpiMonthlyRevenueQueryHandler` | `SalesOrder`, `BudgetTarget`, `KPIValue` | — | `SalesOrderConfirmed`, `PerformanceKPIValueUpdated` | `CEO.ControlTower.View`, `Sales.Order.Read` | `GetCeoKpiMonthlyRevenueQueryHandlerTests` |
| CEO | KPI — EBITDA Marjı (%) | `GET /api/control-tower/ceo/kpis/ebitda-margin` | `GetCeoKpiEbitdaMarginQuery` | `GetCeoKpiEbitdaMarginQueryHandler` | `FinanceJournalEntry`, `KPIValue` | — | `FinanceJournalEntryPosted` | `CEO.ControlTower.View`, `Finance.JournalEntry.Read` | `GetCeoKpiEbitdaMarginQueryHandlerTests` |
| CEO | KPI — Aktif Müşteri Sayısı | `GET /api/control-tower/ceo/kpis/active-customers` | `GetCeoKpiActiveCustomersQuery` | `GetCeoKpiActiveCustomersQueryHandler` | `CrmAccount` | — | `CrmAccountCreated` | `CEO.ControlTower.View`, `CRM.Account.Read` | `GetCeoKpiActiveCustomersQueryHandlerTests` |
| CEO | KPI — Toplam Alacak / Borç | `GET /api/control-tower/ceo/kpis/receivables-payables` | `GetCeoKpiReceivablesPayablesQuery` | `GetCeoKpiReceivablesPayablesQueryHandler` | `FinanceInvoice`, `FinancePayment` | — | `FinanceInvoiceCreated`, `FinancePaymentCompleted` | `CEO.ControlTower.View`, `Finance.Invoice.Read` | `GetCeoKpiReceivablesPayablesQueryHandlerTests` |
| CEO | KPI — Sipariş Backlog Değeri | `GET /api/control-tower/ceo/kpis/order-backlog` | `GetCeoKpiOrderBacklogQuery` | `GetCeoKpiOrderBacklogQueryHandler` | `SalesOrder` | — | `SalesOrderCreated` | `CEO.ControlTower.View`, `Sales.Order.Read` | `GetCeoKpiOrderBacklogQueryHandlerTests` |
| CEO | KPI — Personel Sayısı | `GET /api/control-tower/ceo/kpis/headcount` | `GetCeoKpiHeadcountQuery` | `GetCeoKpiHeadcountQueryHandler` | `HrEmployee` | — | `HrEmployeeOnboarded` | `CEO.ControlTower.View`, `HR.Payroll.Read` | `GetCeoKpiHeadcountQueryHandlerTests` |
| CEO | KPI — Üretim Verimliliği (%) | `GET /api/control-tower/ceo/kpis/production-efficiency` | `GetCeoKpiProductionEfficiencyQuery` | `GetCeoKpiProductionEfficiencyQueryHandler` | `ProductionWorkOrder`, `KPIValue` | — | `ProductionWorkOrderCompleted` | `CEO.ControlTower.View`, `Production.WorkOrder.Read` | `GetCeoKpiProductionEfficiencyQueryHandlerTests` |
| CEO | KPI — Kalite Red Oranı (%) | `GET /api/control-tower/ceo/kpis/quality-reject-rate` | `GetCeoKpiQualityRejectRateQuery` | `GetCeoKpiQualityRejectRateQueryHandler` | `QcTestResult` | — | `QcTestResultCompleted` | `CEO.ControlTower.View`, `QC.Claim.Read` | `GetCeoKpiQualityRejectRateQueryHandlerTests` |
| CEO | KPI — Net Promoter Score (NPS) | `GET /api/control-tower/ceo/kpis/nps` | `GetCeoKpiNpsQuery` | `GetCeoKpiNpsQueryHandler` | `CrmAccount`, `KPIValue` | — | `PerformanceKPIValueUpdated` | `CEO.ControlTower.View`, `CRM.Account.Read` | `GetCeoKpiNpsQueryHandlerTests` |
| CEO | KPI — Nakit Pozisyonu | `GET /api/control-tower/ceo/kpis/cash-position` | `GetCeoKpiCashPositionQuery` | `GetCeoKpiCashPositionQueryHandler` | `BankAccount`, `CashVault` | — | `FinancePaymentCompleted` | `CEO.ControlTower.View`, `Finance.Payment.Read` | `GetCeoKpiCashPositionQueryHandlerTests` |

### Menü alt ekranları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| CEO | Strategic Decisions | `GET /api/ceo/decision-logs` | `ListCeoDecisionLogsQuery` | `ListCeoDecisionLogsQueryHandler` | `DecisionLog` | `DecisionLogApproval` | `CeoDecisionLogCreated` | `CEO.DecisionLog.Read` | `ListCeoDecisionLogsQueryHandlerTests` |
| CEO | Company Health Score (detay) | `GET /api/control-tower/ceo/health-scores/detail` | `GetCeoCompanyHealthScoreDetailQuery` | `GetCeoCompanyHealthScoreDetailQueryHandler` | `CompanyHealthScore` | — | `PerformanceKPIValueUpdated` | `CEO.ControlTower.View` | `GetCeoCompanyHealthScoreDetailQueryHandlerTests` |
| CEO | Department Scorecards | `GET /api/control-tower/ceo/department-scorecards` | `ListCeoDepartmentScorecardsQuery` | `ListCeoDepartmentScorecardsQueryHandler` | `DepartmentScorecard` | — | `PerformanceKPIValueUpdated` | `CEO.ControlTower.View` | `ListCeoDepartmentScorecardsQueryHandlerTests` |
| CEO | Budget vs Actuals | `GET /api/control-tower/ceo/budget-vs-actuals` | `GetCeoBudgetVsActualsQuery` | `GetCeoBudgetVsActualsQueryHandler` | `BudgetTarget`, `BudgetLine` | — | `FinanceJournalEntryPosted` | `CEO.ControlTower.View`, `Finance.JournalEntry.Read` | `GetCeoBudgetVsActualsQueryHandlerTests` |
| CEO | Key Risk Indicators | `GET /api/control-tower/ceo/risk-indicators` | `GetCeoKeyRiskIndicatorsQuery` | `GetCeoKeyRiskIndicatorsQueryHandler` | `CompanyHealthScore`, `ComplianceFinding` | — | `ComplianceFindingOpened` | `CEO.ControlTower.View` | `GetCeoKeyRiskIndicatorsQueryHandlerTests` |
| CEO | Board Reports | `GET /api/control-tower/ceo/board-reports` | `GetCeoBoardReportsQuery` | `GetCeoBoardReportsQueryHandler` | reporting metadata | — | — | `CEO.ControlTower.View` | `GetCeoBoardReportsQueryHandlerTests` |

### Aksiyon komutları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| CEO | Karar oluşturma | `POST /api/ceo/decision-logs` | `CreateCeoDecisionLogCommand` | `CreateCeoDecisionLogCommandHandler` | `DecisionLog` | `DecisionLogApproval` | `CeoDecisionLogCreated` | `CEO.DecisionLog.Write` | `CreateCeoDecisionLogCommandHandlerTests` |
| CEO | Karar onayı | `POST /api/ceo/decision-logs/{id}/approve` | `ApproveCeoDecisionLogCommand` | `ApproveCeoDecisionLogCommandHandler` | `DecisionLog` | `DecisionLogApproval` | `CeoDecisionLogApproved` | `CEO.DecisionLog.Approve` | `ApproveCeoDecisionLogCommandHandlerTests` |

---

## 2. Sales Control Tower

**Scope referansı:** `CONTROL_TOWER_FINAL_SCOPE.md` §2  
**Base permission:** `Sales.ControlTower.View`  
**Menü rotaları:** Sales Overview · Opportunities Pipeline · Proposals & Quotes · Sales Orders · Customer Accounts · Targets & Performance · Sales Reports

### Shell & ortak kontroller

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Sales | Sol dikey menü + kule geçişleri | `GET /api/control-tower/sales/navigation` | `GetSalesNavigationQuery` | `GetSalesNavigationQueryHandler` | — (RBAC) | — | — | `Sales.ControlTower.View` | `GetSalesNavigationQueryHandlerTests` |
| Sales | Rol bazlı kullanıcı / profil alanı | `GET /api/control-tower/sales/profile` | `GetSalesProfileContextQuery` | `GetSalesProfileContextQueryHandler` | `User`, `Role` | — | `UserLoggedIn` | `Sales.ControlTower.View` | `GetSalesProfileContextQueryHandlerTests` |
| Sales | Export / Filter / Date controls | `GET /api/control-tower/sales/export` | `ExportSalesDashboardQuery` | `ExportSalesDashboardQueryHandler` | read models | — | — | `Sales.ControlTower.View` | `SalesControlTowerApiTests` |
| Sales | Legend / status açıklamaları | `GET /api/control-tower/sales/status-legend` | `GetSalesStatusLegendQuery` | `GetSalesStatusLegendQueryHandler` | — (i18n) | — | — | `Sales.ControlTower.View` | `GetSalesStatusLegendQueryHandlerTests` |

### Standart dashboard widget'ları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Sales | Executive Snapshot | `GET /api/control-tower/sales/snapshot` | `GetSalesExecutiveSnapshotQuery` | `GetSalesExecutiveSnapshotQueryHandler` | `CrmOpportunity`, `CrmProposal`, `SalesOrder` | — | `CrmOpportunityCreated`, `SalesOrderConfirmed` | `Sales.ControlTower.View` | `GetSalesExecutiveSnapshotQueryHandlerTests` |
| Sales | Today's Priorities | `GET /api/control-tower/sales/priorities/today` | `GetSalesTodayPrioritiesQuery` | `GetSalesTodayPrioritiesQueryHandler` | `CrmOpportunity`, `CrmProposal`, `SalesOrder` | — | `CrmProposalCreated` | `CRM.Proposal.Read`, `Sales.Order.Read` | `GetSalesTodayPrioritiesQueryHandlerTests` |
| Sales | Critical Alerts | `GET /api/control-tower/sales/alerts/critical` | `GetSalesCriticalAlertsQuery` | `GetSalesCriticalAlertsQueryHandler` | `CrmProposal`, `SalesOrder`, `CrmAccount` | — | `CrmProposalCreated` | `Sales.ControlTower.View` | `GetSalesCriticalAlertsQueryHandlerTests` |
| Sales | Notifications | `GET /api/control-tower/sales/notifications` | `GetSalesNotificationsQuery` | `GetSalesNotificationsQueryHandler` | notification projection | — | `SalesOrderCreated`, `CrmProposalApproved` | `Sales.ControlTower.View` | `GetSalesNotificationsQueryHandlerTests` |
| Sales | Risk / Health Score | `GET /api/control-tower/sales/health-scores` | `GetSalesHealthScoresQuery` | `GetSalesHealthScoresQueryHandler` | `CrmOpportunity`, `CrmAccount` | — | `CrmOpportunityCreated` | `Sales.ControlTower.View` | `GetSalesHealthScoresQueryHandlerTests` |
| Sales | Customer / Department Panel | `GET /api/control-tower/sales/customers` | `GetSalesCustomerPanelQuery` | `GetSalesCustomerPanelQueryHandler` | `CrmAccount`, `CrmActivity` | — | `CrmAccountCreated` | `CRM.Account.Read` | `GetSalesCustomerPanelQueryHandlerTests` |
| Sales | Message Drafts | `GET /api/control-tower/sales/message-drafts` | `GetSalesMessageDraftsQuery` | `GetSalesMessageDraftsQueryHandler` | message draft projection | — | — | `CRM.Proposal.Write`, `AI.Copilot.Use` | `GetSalesMessageDraftsQueryHandlerTests` |
| Sales | Calendar & Key Events | `GET /api/control-tower/sales/calendar` | `GetSalesCalendarEventsQuery` | `GetSalesCalendarEventsQueryHandler` | calendar projection | — | — | `Sales.ControlTower.View` | `GetSalesCalendarEventsQueryHandlerTests` |
| Sales | Next 7 Days Focus | `GET /api/control-tower/sales/focus/next-7-days` | `GetSalesNext7DaysFocusQuery` | `GetSalesNext7DaysFocusQueryHandler` | `CrmOpportunity`, `CrmProposal` | — | `CrmOpportunityCreated` | `Sales.ControlTower.View` | `GetSalesNext7DaysFocusQueryHandlerTests` |
| Sales | Reports & Analytics | `GET /api/control-tower/sales/reports` | `GetSalesReportsCatalogQuery` | `GetSalesReportsCatalogQueryHandler` | reporting metadata | — | — | `Sales.ControlTower.View` | `GetSalesReportsCatalogQueryHandlerTests` |

### KPI kartları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Sales | KPI — Aylık Satış Cirosu | `GET /api/control-tower/sales/kpis/monthly-revenue` | `GetSalesKpiMonthlyRevenueQuery` | `GetSalesKpiMonthlyRevenueQueryHandler` | `SalesOrder`, `SalesTarget` | — | `SalesOrderConfirmed` | `Sales.ControlTower.View`, `Sales.Order.Read` | `GetSalesKpiMonthlyRevenueQueryHandlerTests` |
| Sales | KPI — Aktif Fırsat Sayısı ve Değeri | `GET /api/control-tower/sales/kpis/active-opportunities` | `GetSalesKpiActiveOpportunitiesQuery` | `GetSalesKpiActiveOpportunitiesQueryHandler` | `CrmOpportunity` | — | `CrmOpportunityCreated` | `Sales.ControlTower.View`, `CRM.Account.Read` | `GetSalesKpiActiveOpportunitiesQueryHandlerTests` |
| Sales | KPI — Win Rate (%) | `GET /api/control-tower/sales/kpis/win-rate` | `GetSalesKpiWinRateQuery` | `GetSalesKpiWinRateQueryHandler` | `CrmOpportunity`, `SalesOrder` | — | `SalesOrderConfirmed` | `Sales.ControlTower.View` | `GetSalesKpiWinRateQueryHandlerTests` |
| Sales | KPI — Ortalama Kapanış Süresi | `GET /api/control-tower/sales/kpis/avg-close-days` | `GetSalesKpiAvgCloseDaysQuery` | `GetSalesKpiAvgCloseDaysQueryHandler` | `CrmOpportunity` | — | `CrmOpportunityCreated` | `Sales.ControlTower.View` | `GetSalesKpiAvgCloseDaysQueryHandlerTests` |
| Sales | KPI — Teklife Dönüşüm Oranı | `GET /api/control-tower/sales/kpis/proposal-conversion` | `GetSalesKpiProposalConversionQuery` | `GetSalesKpiProposalConversionQueryHandler` | `CrmProposal`, `SalesOrder` | — | `CrmProposalApproved` | `Sales.ControlTower.View`, `CRM.Proposal.Read` | `GetSalesKpiProposalConversionQueryHandlerTests` |
| Sales | KPI — Aktif Sipariş Sayısı | `GET /api/control-tower/sales/kpis/active-orders` | `GetSalesKpiActiveOrdersQuery` | `GetSalesKpiActiveOrdersQueryHandler` | `SalesOrder` | — | `SalesOrderCreated` | `Sales.ControlTower.View`, `Sales.Order.Read` | `GetSalesKpiActiveOrdersQueryHandlerTests` |
| Sales | KPI — Yeni Müşteri Sayısı (Ay) | `GET /api/control-tower/sales/kpis/new-customers` | `GetSalesKpiNewCustomersQuery` | `GetSalesKpiNewCustomersQueryHandler` | `CrmAccount` | — | `CrmAccountCreated` | `Sales.ControlTower.View`, `CRM.Account.Read` | `GetSalesKpiNewCustomersQueryHandlerTests` |
| Sales | KPI — Kayıp Fırsat Değeri | `GET /api/control-tower/sales/kpis/lost-opportunity-value` | `GetSalesKpiLostOpportunityValueQuery` | `GetSalesKpiLostOpportunityValueQueryHandler` | `CrmOpportunity` | — | `CrmOpportunityCreated` | `Sales.ControlTower.View` | `GetSalesKpiLostOpportunityValueQueryHandlerTests` |

### Menü alt ekranları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Sales | Opportunities Pipeline | `GET /api/crm/opportunities` | `ListCrmOpportunitiesQuery` | `ListCrmOpportunitiesQueryHandler` | `CrmOpportunity`, `CrmAccount` | — | `CrmOpportunityCreated` | `CRM.Account.Read` | `ListCrmOpportunitiesQueryHandlerTests` |
| Sales | Proposals & Quotes | `GET /api/crm/proposals` | `ListCrmProposalsQuery` | `ListCrmProposalsQueryHandler` | `CrmProposal`, `CrmProposalItem` | `CrmProposalApproval` | `CrmProposalCreated` | `CRM.Proposal.Read` | `ListCrmProposalsQueryHandlerTests` |
| Sales | Sales Orders | `GET /api/sales/orders` | `ListSalesOrdersQuery` | `ListSalesOrdersQueryHandler` | `SalesOrder`, `SalesOrderItem` | — | `SalesOrderCreated` | `Sales.Order.Read` | `ListSalesOrdersQueryHandlerTests` |
| Sales | Customer Accounts | `GET /api/crm/accounts` | `ListCrmAccountsQuery` | `ListCrmAccountsQueryHandler` | `CrmAccount`, `CrmContact` | — | `CrmAccountCreated` | `CRM.Account.Read` | `ListCrmAccountsQueryHandlerTests` |
| Sales | Targets & Performance | `GET /api/sales/targets` | `ListSalesTargetsQuery` | `ListSalesTargetsQueryHandler` | `SalesTarget`, `CrmActivity` | — | `PerformanceKPIValueUpdated` | `Sales.ControlTower.View` | `ListSalesTargetsQueryHandlerTests` |
| Sales | Sales Reports (detay) | `GET /api/sales/reports` | `ListSalesReportsQuery` | `ListSalesReportsQueryHandler` | reporting metadata | — | — | `Sales.ControlTower.View` | `ListSalesReportsQueryHandlerTests` |

### Aksiyon komutları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Sales | Fırsat oluşturma | `POST /api/crm/opportunities` | `CreateCrmOpportunityCommand` | `CreateCrmOpportunityCommandHandler` | `CrmOpportunity` | — | `CrmOpportunityCreated` | `CRM.Account.Write` | `CreateCrmOpportunityCommandHandlerTests` |
| Sales | Teklif onayı | `POST /api/crm/proposals/{id}/approve` | `ApproveCrmProposalCommand` | `ApproveCrmProposalCommandHandler` | `CrmProposal` | `CrmProposalApproval` | `CrmProposalApproved` | `CRM.Proposal.Approve` | `ApproveCrmProposalCommandHandlerTests` |
| Sales | Sipariş oluşturma | `POST /api/sales/orders` | `CreateSalesOrderCommand` | `CreateSalesOrderCommandHandler` | `SalesOrder`, `SalesOrderItem` | — | `SalesOrderCreated`, `SalesOrderConfirmed` | `Sales.Order.Write` | `CreateSalesOrderCommandHandlerTests` |

---

## 3. Finance & Cash Control Tower

**Scope referansı:** `CONTROL_TOWER_FINAL_SCOPE.md` §3  
**Base permission:** `Finance.ControlTower.View`  
**Menü rotaları:** Finance Overview · Cash Position · Receivables & Payables · Journal Entries · Invoices · Bank & Vault · Budget Management · Tax & Compliance · Finance Reports

### Shell & ortak kontroller

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Finance | Sol dikey menü + kule geçişleri | `GET /api/control-tower/finance/navigation` | `GetFinanceNavigationQuery` | `GetFinanceNavigationQueryHandler` | — (RBAC) | — | — | `Finance.ControlTower.View` | `GetFinanceNavigationQueryHandlerTests` |
| Finance | Rol bazlı kullanıcı / profil alanı | `GET /api/control-tower/finance/profile` | `GetFinanceProfileContextQuery` | `GetFinanceProfileContextQueryHandler` | `User`, `Role` | — | `UserLoggedIn` | `Finance.ControlTower.View` | `GetFinanceProfileContextQueryHandlerTests` |
| Finance | Export / Filter / Date controls | `GET /api/control-tower/finance/export` | `ExportFinanceDashboardQuery` | `ExportFinanceDashboardQueryHandler` | read models | — | — | `Finance.ControlTower.View` | `FinanceControlTowerApiTests` |
| Finance | Legend / status açıklamaları | `GET /api/control-tower/finance/status-legend` | `GetFinanceStatusLegendQuery` | `GetFinanceStatusLegendQueryHandler` | — (i18n) | — | — | `Finance.ControlTower.View` | `GetFinanceStatusLegendQueryHandlerTests` |

### Standart dashboard widget'ları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Finance | Executive Snapshot | `GET /api/control-tower/finance/snapshot` | `GetFinanceExecutiveSnapshotQuery` | `GetFinanceExecutiveSnapshotQueryHandler` | `FinancePayment`, `BankAccount` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View` | `GetFinanceExecutiveSnapshotQueryHandlerTests` |
| Finance | Today's Priorities | `GET /api/control-tower/finance/priorities/today` | `GetFinanceTodayPrioritiesQuery` | `GetFinanceTodayPrioritiesQueryHandler` | `FinancePayment`, `FinanceJournalEntry`, `BankReconciliation` | — | `FinanceJournalEntryCreated` | `Finance.JournalEntry.Read`, `Finance.Payment.Write` | `GetFinanceTodayPrioritiesQueryHandlerTests` |
| Finance | Critical Alerts | `GET /api/control-tower/finance/alerts/critical` | `GetFinanceCriticalAlertsQuery` | `GetFinanceCriticalAlertsQueryHandler` | `FinanceInvoice`, `BudgetLine`, `TaxDeclaration` | — | `FinanceInvoiceCreated` | `Finance.ControlTower.View` | `GetFinanceCriticalAlertsQueryHandlerTests` |
| Finance | Notifications | `GET /api/control-tower/finance/notifications` | `GetFinanceNotificationsQuery` | `GetFinanceNotificationsQueryHandler` | notification projection | — | `FinancePaymentCompleted` | `Finance.ControlTower.View` | `GetFinanceNotificationsQueryHandlerTests` |
| Finance | Risk / Health Score | `GET /api/control-tower/finance/health-scores` | `GetFinanceHealthScoresQuery` | `GetFinanceHealthScoresQueryHandler` | `FinanceInvoice`, `FinancePayment` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View` | `GetFinanceHealthScoresQueryHandlerTests` |
| Finance | Customer / Supplier / Department Panel | `GET /api/control-tower/finance/aging` | `GetFinanceAgingPanelsQuery` | `GetFinanceAgingPanelsQueryHandler` | `FinanceInvoice`, `FinancePayment`, `CrmAccount`, `BudgetLine` | — | `FinanceInvoiceCreated` | `Finance.Invoice.Read`, `Finance.Payment.Read` | `GetFinanceAgingPanelsQueryHandlerTests` |
| Finance | Message Drafts | `GET /api/control-tower/finance/message-drafts` | `GetFinanceMessageDraftsQuery` | `GetFinanceMessageDraftsQueryHandler` | message draft projection | — | — | `Finance.Invoice.Read`, `AI.Copilot.Use` | `GetFinanceMessageDraftsQueryHandlerTests` |
| Finance | Calendar & Key Events | `GET /api/control-tower/finance/calendar` | `GetFinanceCalendarEventsQuery` | `GetFinanceCalendarEventsQueryHandler` | `TaxDeclaration`, `BudgetTarget` | — | — | `Finance.ControlTower.View` | `GetFinanceCalendarEventsQueryHandlerTests` |
| Finance | Next 7 Days Focus | `GET /api/control-tower/finance/focus/next-7-days` | `GetFinanceNext7DaysFocusQuery` | `GetFinanceNext7DaysFocusQueryHandler` | `FinancePayment`, `BankReconciliation` | — | `FinanceJournalEntryPosted` | `Finance.ControlTower.View` | `GetFinanceNext7DaysFocusQueryHandlerTests` |
| Finance | Reports & Analytics | `GET /api/control-tower/finance/reports` | `GetFinanceReportsCatalogQuery` | `GetFinanceReportsCatalogQueryHandler` | reporting metadata | — | — | `Finance.ControlTower.View` | `GetFinanceReportsCatalogQueryHandlerTests` |

### KPI kartları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Finance | KPI — Günlük Nakit Pozisyonu | `GET /api/control-tower/finance/kpis/daily-cash` | `GetFinanceKpiDailyCashQuery` | `GetFinanceKpiDailyCashQueryHandler` | `BankAccount`, `CashVault` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View`, `Finance.Payment.Read` | `GetFinanceKpiDailyCashQueryHandlerTests` |
| Finance | KPI — Toplam Alacak | `GET /api/control-tower/finance/kpis/receivables` | `GetFinanceKpiReceivablesQuery` | `GetFinanceKpiReceivablesQueryHandler` | `FinanceInvoice` | — | `FinanceInvoiceCreated` | `Finance.ControlTower.View`, `Finance.Invoice.Read` | `GetFinanceKpiReceivablesQueryHandlerTests` |
| Finance | KPI — Toplam Borç | `GET /api/control-tower/finance/kpis/payables` | `GetFinanceKpiPayablesQuery` | `GetFinanceKpiPayablesQueryHandler` | `FinanceInvoice`, `FinancePayment` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View`, `Finance.Payment.Read` | `GetFinanceKpiPayablesQueryHandlerTests` |
| Finance | KPI — DSO | `GET /api/control-tower/finance/kpis/dso` | `GetFinanceKpiDsoQuery` | `GetFinanceKpiDsoQueryHandler` | `FinanceInvoice`, `FinancePayment` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View` | `GetFinanceKpiDsoQueryHandlerTests` |
| Finance | KPI — DPO | `GET /api/control-tower/finance/kpis/dpo` | `GetFinanceKpiDpoQuery` | `GetFinanceKpiDpoQueryHandler` | `FinanceInvoice`, `FinancePayment` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View` | `GetFinanceKpiDpoQueryHandlerTests` |
| Finance | KPI — Aylık Gelir vs Gider | `GET /api/control-tower/finance/kpis/revenue-vs-expense` | `GetFinanceKpiRevenueVsExpenseQuery` | `GetFinanceKpiRevenueVsExpenseQueryHandler` | `FinanceJournalEntry` | — | `FinanceJournalEntryPosted` | `Finance.ControlTower.View`, `Finance.JournalEntry.Read` | `GetFinanceKpiRevenueVsExpenseQueryHandlerTests` |
| Finance | KPI — Vergi Borcu | `GET /api/control-tower/finance/kpis/tax-liability` | `GetFinanceKpiTaxLiabilityQuery` | `GetFinanceKpiTaxLiabilityQueryHandler` | `TaxDeclaration` | — | — | `Finance.ControlTower.View` | `GetFinanceKpiTaxLiabilityQueryHandlerTests` |
| Finance | KPI — Banka Bakiyeleri Özeti | `GET /api/control-tower/finance/kpis/bank-balances` | `GetFinanceKpiBankBalancesQuery` | `GetFinanceKpiBankBalancesQueryHandler` | `BankAccount`, `BankTransaction` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View`, `Finance.Payment.Read` | `GetFinanceKpiBankBalancesQueryHandlerTests` |

### Menü alt ekranları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Finance | Cash Position | `GET /api/finance/cash-position` | `GetFinanceCashPositionQuery` | `GetFinanceCashPositionQueryHandler` | `BankAccount`, `CashVault` | — | `FinancePaymentCompleted` | `Finance.ControlTower.View` | `GetFinanceCashPositionQueryHandlerTests` |
| Finance | Receivables & Payables | `GET /api/finance/receivables-payables` | `GetFinanceReceivablesPayablesQuery` | `GetFinanceReceivablesPayablesQueryHandler` | `FinanceInvoice`, `FinancePayment` | — | `FinanceInvoiceCreated` | `Finance.Invoice.Read` | `GetFinanceReceivablesPayablesQueryHandlerTests` |
| Finance | Journal Entries | `GET /api/finance/journal-entries` | `ListFinanceJournalEntriesQuery` | `ListFinanceJournalEntriesQueryHandler` | `FinanceJournalEntry`, `FinanceJournalEntryLine` | `FinanceJournalEntryPosting` | `FinanceJournalEntryCreated` | `Finance.JournalEntry.Read` | `ListFinanceJournalEntriesQueryHandlerTests` |
| Finance | Invoices | `GET /api/finance/invoices` | `ListFinanceInvoicesQuery` | `ListFinanceInvoicesQueryHandler` | `FinanceInvoice`, `FinanceInvoiceLine` | — | `FinanceInvoiceCreated` | `Finance.Invoice.Read` | `ListFinanceInvoicesQueryHandlerTests` |
| Finance | Bank & Vault | `GET /api/finance/bank-accounts` | `ListBankAccountsQuery` | `ListBankAccountsQueryHandler` | `BankAccount`, `BankTransaction`, `BankReconciliation` | — | `FinancePaymentCompleted` | `Finance.Payment.Read` | `ListBankAccountsQueryHandlerTests` |
| Finance | Budget Management | `GET /api/finance/budgets` | `ListBudgetTargetsQuery` | `ListBudgetTargetsQueryHandler` | `BudgetTarget`, `BudgetLine` | — | — | `Finance.ControlTower.View` | `ListBudgetTargetsQueryHandlerTests` |
| Finance | Tax & Compliance | `GET /api/finance/tax-declarations` | `ListTaxDeclarationsQuery` | `ListTaxDeclarationsQueryHandler` | `TaxDeclaration` | — | — | `Finance.ControlTower.View` | `ListTaxDeclarationsQueryHandlerTests` |
| Finance | Finance Reports (detay) | `GET /api/finance/reports` | `ListFinanceReportsQuery` | `ListFinanceReportsQueryHandler` | reporting metadata | — | — | `Finance.ControlTower.View` | `ListFinanceReportsQueryHandlerTests` |

### Aksiyon komutları

| Control Tower | Widget / Feature | API Endpoint | Query / Command | Handler | Entity | Workflow | Domain Event | Permission | Test |
| ------------- | ---------------- | ------------ | --------------- | ------- | ------ | -------- | ------------ | ---------- | ---- |
| Finance | Yevmiye fişi post | `POST /api/finance/journal-entries/{id}/post` | `PostFinanceJournalEntryCommand` | `PostFinanceJournalEntryCommandHandler` | `FinanceJournalEntry` | `FinanceJournalEntryPosting` | `FinanceJournalEntryPosted` | `Finance.JournalEntry.Post` | `PostFinanceJournalEntryCommandHandlerTests` |
| Finance | Fatura oluştur | `POST /api/finance/invoices` | `CreateFinanceInvoiceCommand` | `CreateFinanceInvoiceCommandHandler` | `FinanceInvoice`, `FinanceInvoiceLine` | — | `FinanceInvoiceCreated` | `Finance.Invoice.Write` | `CreateFinanceInvoiceCommandHandlerTests` |
| Finance | Ödeme / tahsilat kaydı | `POST /api/finance/payments` | `CreateFinancePaymentCommand` | `CreateFinancePaymentCommandHandler` | `FinancePayment` | — | `FinancePaymentCompleted` | `Finance.Payment.Write` | `CreateFinancePaymentCommandHandlerTests` |

---

## Cross-cutting gereksinimler

| Konu | Uygulama | Referans |
|------|----------|----------|
| i18n | Hardcoded string yasak; API `message` + UI key | `LOCALIZATION_I18N_STANDARDS.md` |
| Tenant | Tüm handler'larda `ITenantProvider` + global filter | `SECURITY_AUTHORIZATION.md` |
| Event publish | Domain event → Outbox → Integration | `EVENT_BUS.md` |
| Workflow | Onay akışları `WORKFLOW_ENGINE.md` Workflow Matrix ile hizalı | `DecisionLogApproval`, `CrmProposalApproval`, `FinanceJournalEntryPosting` |
| Permission gap | `CEO.ControlTower.View`, `Sales.ControlTower.View`, `Finance.ControlTower.View` — `SECURITY_AUTHORIZATION.md`'ye eklenecek | `CONTROL_TOWER_FINAL_SCOPE.md` § Standardization |

---

## Özet istatistik

| Control Tower | Widget satırı | Sprint |
|---------------|---------------|--------|
| CEO | 32 | 2A |
| Sales | 29 | 2A |
| Finance | 31 | 2B |
| **Toplam** | **92** | Sprint 2 gate |

**Phase 2:** Kule 4–16 (HR, Production, QC, Logistics, …) ayrı task ile genişletilecektir.

---

*Task 009 — Agent 2 Product Engineering. Kod veya hassas veri içermez.*
