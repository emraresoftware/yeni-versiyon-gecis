# Legacy Workflows — Discovery Catalog

**Version:** 2.0 · **Task:** 022 · **Agent:** 6  
**BOS hedef:** `WORKFLOW_ENGINE.md` Workflow Matrix

---

## Özet

| Metrik | Değer |
|--------|-------|
| Keşfedilen workflow | 25 |
| Onay tabanlı | 12 |
| State machine / Blueprint | 4 |
| Scheduler / queue / job | 9 |

---

## Workflow → BOS Eşlemesi

| ID | Legacy kaynak | Durum geçişleri | BOS Workflow | BOS Event | Epic |
|----|---------------|-----------------|--------------|-----------|------|
| WF-01 | emare-crm `OnayMotoru.php` | bekliyor → onaylandı / reddedildi | `ApprovalRequest` | `ApprovalRequestApproved` | EPIC-LEG-011 |
| WF-02 | emare-crm `BlueprintEngine.php` | state → transition → waiting_approval | `WorkflowBlueprint` | `BlueprintPausedForApproval` | EPIC-LEG-011 |
| WF-03 | Finance `ExpenseReportController` | draft → submitted → manager → finance → paid | `ExpenseReportApproval` | `ExpenseReportSubmitted` | EPIC-LEG-005 |
| WF-04 | Finance `LeaveController` | pending → approved/rejected/cancelled | `HrLeaveApproval` | `HrLeaveApproved` | EPIC-LEG-009 |
| WF-05 | Finance `StokTransferServisi` | pending → approved → completed | `LogisticsStockTransfer` | `StockTransferApproved` | EPIC-LEG-012 |
| WF-06 | Finance `PurchaseOrderController` | draft → approved → partial → received | `PurchaseOrderApproval` | `PurchaseOrderApproved` | EPIC-LEG-010 |
| WF-07 | Finance `GoodsReceiptController` | draft → posted | `GoodsReceiptPosting` | `GoodsReceiptPosted` | EPIC-LEG-010 |
| WF-08 | Finance `MrpController` | suggestion draft → PO draft | `MrpSuggestionConversion` | `MrpSuggestionConvertedToPurchaseOrder` | EPIC-LEG-013 |
| WF-09 | Finance `GunSonuServisi` | open → closed (day-end) | `CashDayEndClosure` | `CashDayEndClosed` | EPIC-LEG-008 |
| WF-10 | Finance `TicketSlaService` | SLA timer → breach → escalate | `TicketSlaEscalation` | `TicketSlaBreached` | EPIC-LEG-018 |
| WF-11 | emare-crm `TicketRoutingService` | unassigned → assigned (round-robin) | `TicketAutoAssignment` | `TicketAssigned` | EPIC-LEG-018 |
| WF-12 | Finance `RecruitmentController` | applied → screening → interview → offer → hired | `RecruitmentPipeline` | `CandidateHired` | EPIC-LEG-009 |
| WF-13 | Finance `ContractController` | draft → active → suspended → expired | `ContractLifecycle` | `ContractActivated` | EPIC-LEG-021 |
| WF-14 | Finance `EInvoiceController` | draft → sent → cancelled | `EInvoiceSubmission` | `EInvoiceSent` | EPIC-LEG-021 |
| WF-15 | emare-crm `SatinalmaService` | taslak → onay_bekliyor → onaylı | `PurchaseRequisitionApproval` | `PurchaseRequisitionSubmitted` | EPIC-LEG-010 |
| WF-16 | Saloon `StokTransferServisi` | pending → approved → completed | `StockTransfer` (retail) | `StockTransferCompleted` | EPIC-LEG-010 |
| WF-17 | Elyafgroup `WorkflowEngine.cs` | ticket stage → rule match → email | `WorkflowRule` (service desk) | `WorkflowRuleExecuted` | — (mevcut) |
| WF-18 | Elyafgroup `ChangeProposalStatusCommand` | status 1–6 + timestamps | `CrmProposalApproval` | `CrmProposalApproved` | EPIC-LEG-003 |
| WF-19 | emare-crm `DripCampaignService` | enroll → delay → next step | `MarketingDripWorkflow` | `ContactEnrolledInDrip` | EPIC-LEG-020 |
| WF-20 | emare-crm `ImportExportService` | bekliyor → isleniyor → tamamlandi | `DataImportBatch` | `DataImportCompleted` | EPIC-LEG-008 |
| WF-21 | Finance `ProcessSmsAutomations` | scheduled → queue → sent | `SmsAutomationScheduler` | `SmsAutomationSent` | EPIC-LEG-021 |
| WF-22 | Saloon `ProcessCampaignQueue` | pending → sent/failed (retry 3) | `CampaignSmsQueue` | `CampaignSmsSent` | EPIC-LEG-021 |
| WF-23 | Emare Pazar `sync_tasks.py` | Celery periodic marketplace sync | `MarketplaceSyncJob` | `MarketplaceSyncCompleted` | EPIC-LEG-021 |
| WF-24 | Finance `SyncTrendyolOperationJob` | async operation runner | `MarketplaceOperationJob` | `TrendyolSyncCompleted` | EPIC-LEG-021 |
| WF-25 | emare-crm `DeadLetterQueueService` | failed → retry / DLQ | `IntegrationDeadLetter` | `WebhookDeliveryFailed` | EPIC-LEG-021 |

---

## Ortak Workflow İlkeleri (legacy kanıt)

| İlke | Kaynak(lar) | BOS policy |
|------|-------------|------------|
| Segregation of duty | OnayMotoru, ExpenseReport | Requester ≠ approver |
| Sequential approval steps | OnayMotoru adım_no | Ordered approval chain |
| Reject skips remaining | OnayMotoru | Terminal reject state |
| Draft-only edit | PO, ExpenseReport, Satinalma | Edit guard on status |
| Idempotent side effects | Saloon SaleObserver | Outbox + dedup key |

---

## Needs Architect Review

- BlueprintEngine (50 step cap) vs BOS workflow limit — **Needs Architect Review**
- Ticket workflow vs ERP approval — ayrı engine mi unified mi? **Karar: ayrı** (bounded context)

---

## Conflicts

| ID | Konu | A | B |
|----|------|---|---|
| WC-01 | Onay motoru sayısı | emare-crm OnayMotoru | Finance ExpenseReport inline | → Tek `ApprovalWorkflow` engine |
