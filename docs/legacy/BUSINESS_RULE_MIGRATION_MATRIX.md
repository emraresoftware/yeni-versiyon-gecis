# Business Rule Migration Matrix

**Version:** 2.0 · **Task:** 022 · **Agent:** 6

---

## Kolon Sözlüğü

| Kolon | Açıklama |
|-------|----------|
| ID | BR-XXX |
| Kaynak | Proje + dosya (READ ONLY tarama) |
| Açıklama | İş kuralı (kod kopyası değil) |
| Doğrulama | 2. kaynak varsa |
| BOS Aggregate | DOMAIN_MODEL |
| Workflow | WORKFLOW_ENGINE |
| Permission | Module.Resource.Action |
| Event | EVENT_BUS |
| Epic | EPIC-LEG-XXX |
| Sprint | Öneri |
| Öncelik | P0–P3 |
| Durum | Spec ready / Needs Architect Review |

---

## P0 — Kritik İş Kuralları (25)

| ID | Kaynak | Açıklama | 2. kaynak | BOS Aggregate | Workflow | Permission | Event | Epic | Sprint | Öncelik |
|----|--------|----------|-----------|---------------|----------|------------|-------|------|--------|---------|
| BR-001 | Finance MrpController | MRP min/max/safety/lead/reorder multiple zorunlu | Finance MrpRule model | MrpRule | — | Production.Mrp.Write | MrpRuleUpserted | EPIC-LEG-013 | N+6 | P0 |
| BR-002 | Finance MrpController | Target stock + reorder rounding | BR-001 | MrpPlanningService | MrpConversion | Production.Mrp.Read | MrpSuggestionDraftCreated | EPIC-LEG-013 | N+6 | P0 |
| BR-006 | Finance SaleController | Yetersiz stokta satış engeli | Saloon stok check | InventoryItem | — | Sales.Order.Write | SaleRejectedInsufficientStock | EPIC-LEG-010 | N+5 | P0 |
| BR-007 | Finance SaleController | Satışta stok düş + movement | Saloon observer | StockMovement | — | Inventory.Movement.Write | StockDecrementedOnSale | EPIC-LEG-010 | N+5 | P0 |
| BR-009 | Finance ProcurementLogisticsService | Mal kabul draft→posted stok artır | PO controller | GoodsReceipt | GoodsReceiptPosting | Purchasing.Receipt.Post | GoodsReceiptPosted | EPIC-LEG-010 | N+5 | P0 |
| BR-011 | Finance PurchaseOrderController | PO yalnız draft'tan approve | emare-crm PO pattern | PurchaseOrder | PurchaseOrderApproval | Purchasing.Order.Approve | PurchaseOrderApproved | EPIC-LEG-010 | N+5 | P0 |
| BR-005 | Finance Bom.php | BOM maliyet + fire oranı | LEGACY_BUSINESS_RULES §4 | BillOfMaterials | — | Production.Bom.Read | BomCostRecalculated | EPIC-LEG-013 | N+6 | P0 |
| BR-017 | Finance ExpenseReportController | SoD: sahip kendi raporunu onaylayamaz | emare-crm OnayMotoru | ApprovalWorkflow | ExpenseReportApproval | Finance.Expense.Approve | ApprovalSegregationViolation | EPIC-LEG-011 | N+1 | P0 |
| BR-022 | emare-crm OnayMotoru | Modül+koşul eşleşmeli onay akışı | Blueprint approval | ApprovalRequest | ApprovalChain | *.Approve | ApprovalRequestCreated | EPIC-LEG-011 | N+1 | P0 |
| BR-023 | emare-crm OnayMotoru | Talep eden ≠ onaylayan | Finance ExpenseReport | ApprovalRequest | ApprovalChain | *.Approve | ApprovalSegregationViolation | EPIC-LEG-011 | N+1 | P0 |
| BR-036 | Saloon SaleObserver | Tamamlanan satış → muhasebe+kasa | Finance AccountingService | Sale | SaleSideEffects | Sales.Sale.Complete | SaleCompletedSideEffectsTriggered | EPIC-LEG-008 | N+4 | P0 |
| BR-041 | Saloon KasaServisi | Kasa hareketi atomik bakiye | Finance cash | CashAccount | — | Finance.Cash.Write | CashBalanceAdjusted | EPIC-LEG-008 | N+4 | P0 |
| BR-044 | Saloon StokTransferServisi | Transfer pending→approved→completed + stok | Finance StokTransfer | StockTransfer | StockTransferApproval | Inventory.Transfer.Approve | StockTransferCompleted | EPIC-LEG-012 | N+5 | P0 |
| BR-029 | emare-crm DestekTalebiService | SLA hedef priority'ye göre | Finance TicketSla | SupportTicket | TicketSla | Ticket.Sla.Read | TicketSlaTargetsAssigned | EPIC-LEG-018 | — | P0 |
| — | DOMAIN_MODEL | Yevmiye borç=alacak post öncesi | Finance JournalEntry test | FinanceJournalEntry | JournalPosting | Finance.Journal.Post | FinanceJournalEntryPosted | EPIC-LEG-005 | N+3 | P0 |
| — | DOMAIN_MODEL | Generic Order yasak | ANAYASA | SalesOrder | OrderConfirmation | Sales.Order.Write | SalesOrderConfirmed | EPIC-LEG-004 | N+2 | P0 |
| — | Elyafgroup CrmProposal | Draft→Sent→Approved/Declined | emare-crm Teklif | CrmProposal | CrmProposalApproval | CRM.Proposal.Approve | CrmProposalApproved | EPIC-LEG-003 | N+1 | P0 |
| — | Elyafgroup NumberSequence | CR-/PR- tenant scoped | Finance DocumentSeries | NumberSequence | — | CRM.Number.Read | DocumentNumberIssued | EPIC-LEG-022 | N+1 | P0 |
| — | DOMAIN_MODEL | Yetersiz stokta transfer engeli | Finance transfer | LogisticsStockTransfer | TransferApproval | Logistics.Transfer.Write | StockTransferRejected | EPIC-LEG-012 | N+5 | P0 |
| — | ANAYASA | DateTime UTC PostgreSQL | — | All aggregates | — | — | — | EPIC-LEG-001 | N | P0 |
| BR-004 | Finance MrpController | MRP suggestion→draft PO | Satinalma flow | PurchaseOrder | MrpConversion | Purchasing.Order.Write | MrpSuggestionConvertedToPurchaseOrder | EPIC-LEG-013 | N+6 | P0 |
| BR-013 | Finance Product.php | Landed unit cost formülü | ReportController profit | ProductCosting | — | Inventory.Product.Read | ProductUnitCostComputed | EPIC-LEG-013 | N+6 | P0 |
| BR-008 | Finance SaleController | İade/iptal stok geri | — | StockMovement | SaleReversal | Sales.Order.Cancel | StockRestoredOnSaleReversal | EPIC-LEG-010 | N+5 | P0 |
| BR-039 | Saloon SatisOdemeServisi | Bölünmüş ödeme toplam=grand_total | emarepos pattern | SalePayment | — | Sales.Payment.Write | SplitPaymentValidated | EPIC-LEG-008 | N+4 | P0 |
| BR-003 | Finance MrpController | Projected demand rolling average | Procurement reorder | DemandForecast | — | Production.Mrp.Read | DemandForecastCalculated | EPIC-LEG-013 | N+6 | P0 |

---

## P1 — Yüksek (seçilmiş 15)

| ID | Açıklama | BOS Aggregate | Epic |
|----|----------|---------------|------|
| BR-010 | PO satır toplamları VAT | PurchaseOrder | EPIC-LEG-010 |
| BR-012 | Duplicate invoice per PO engeli | PurchaseInvoice | EPIC-LEG-010 |
| BR-015 | Expense report 2-stage approval | ExpenseReport | EPIC-LEG-005 |
| BR-024 | Onay red → kalan adımlar skip | ApprovalRequest | EPIC-LEG-011 |
| BR-026 | Blueprint max 50 step | WorkflowBlueprint | EPIC-LEG-011 |
| BR-030 | İlk yanıt SLA timestamp | SupportTicket | EPIC-LEG-018 |
| BR-034 | Satınalma talebi onay tetik | PurchaseRequisition | EPIC-LEG-010 |
| BR-037 | Veresiye 3 taksit otomatik | InstallmentPlan | EPIC-LEG-008 |
| BR-046 | Stok sayım fark movement | StockCount | EPIC-LEG-010 |
| BR-047 | Ticket stage→email workflow | WorkflowRule | — |
| BR-048 | Proposal status timestamp | CrmProposal | EPIC-LEG-003 |
| ALG-07 | FIFO lot allocation | StockLot | EPIC-LEG-010 |
| ALG-16 | Satıştan otomatik yevmiye | FinanceJournalEntry | EPIC-LEG-005 |
| BR-019 | SLA breach escalate | SupportTicket | EPIC-LEG-018 |
| BR-020 | DocumentSeries reset | DocumentSeries | EPIC-LEG-022 |

---

## P2/P3 (özet)

P2: BR-018, BR-021, BR-033, BR-040, BR-043, BR-045, marketing drip, booking states — `LEGACY_BUSINESS_RULES.md` tam liste.

P3: Kampanya, bayi hiyerarşisi, restoran POS — ayrı ürün / v2.

---

## Toplam

| Öncelik | Sayı |
|---------|------|
| P0 | 25 (kritik liste) |
| P1 | 24 |
| P2 | 8 |
| P3 | 6 |
| **Toplam catalogued** | **63+** |

---

## Conflicts

| ID | Kural | Conflict | Status |
|----|-------|----------|--------|
| BC-01 | Stok yöntemi | FIFO lot vs movement-only | Needs Architect Review |
| BC-02 | Numara serisi | NumberSequence vs DocumentSeries | EPIC-LEG-022 |

---

## Needs Architect Review (kurallar)

- EBITDA marjı hesaplama formülü (CEO KPI) — legacy gross profit farklı
- Textile AQL pass/fail — mock only, kural yok
- Production efficiency % — formül tanımsız
