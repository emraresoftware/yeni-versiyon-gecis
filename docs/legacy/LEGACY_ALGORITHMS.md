# Legacy Algorithms — Discovery Catalog

**Version:** 2.0 · **Task:** 022 · **Agent:** 6

---

## Özet

| Kategori | Keşif sayısı |
|----------|--------------|
| MRP / Planning | 4 |
| BOM / Costing | 3 |
| Stok (FIFO, transfer, sayım) | 5 |
| Fiyat / indirim / vergi | 4 |
| Döviz | 2 |
| Tahsilat / kasa | 4 |
| Tedarikçi skor | 3 |
| SLA / routing | 2 |
| Marketplace | 2 |
| **Toplam** | **29** |

---

## Algoritma Matrisi

| ID | Algoritma | Legacy kaynak | Business meaning | BOS aggregate / service | Epic |
|----|-----------|---------------|------------------|-------------------------|------|
| ALG-01 | MRP projected demand | Finance `MrpController` | (satış qty / gün) × lead_time | `MrpPlanningService` | EPIC-LEG-013 |
| ALG-02 | MRP target stock | Finance `MrpController` | max(min, safety + demand); reorder multiple | `MrpRule` | EPIC-LEG-013 |
| ALG-03 | MRP → draft PO | Finance `MrpController` | unit price, VAT, delivery date | `PurchaseOrder` | EPIC-LEG-013 |
| ALG-04 | BOM unit cost | Finance `Bom.php` | Σ(qty × price × (1+scrap%)) / batch | `BillOfMaterials` | EPIC-LEG-013 |
| ALG-05 | Landed unit cost | Finance `Product.php` | purchase + fees − rebate + marketplace | `ProductCosting` | EPIC-LEG-013 |
| ALG-06 | Channel gross profit | Finance `ReportController` | revenue − landed − commission JSON | `SalesAnalytics` | EPIC-LEG-008 |
| ALG-07 | FIFO cost allocation | raporlama-app `DataImportService` | consume oldest StockLot | `StockLot`, `CostAllocation` | EPIC-LEG-010 |
| ALG-08 | Sale stock decrement | Finance `SaleController` | qty check + outbound movement | `StockMovement` | EPIC-LEG-010 |
| ALG-09 | Sale reversal restore | Finance `SaleController` | inverse movements | `StockMovement` | EPIC-LEG-010 |
| ALG-10 | Goods receipt post | Finance `ProcurementLogisticsService` | stock + purchase_in movement | `GoodsReceipt` | EPIC-LEG-010 |
| ALG-11 | PO line totals | Finance `ProcurementLogisticsService` | qty × price + VAT% | `PurchaseOrder` | EPIC-LEG-010 |
| ALG-12 | Split payment validation | Saloon `SatisOdemeServisi` | sum = grand_total ±0.02 | `SalePayment` | EPIC-LEG-008 |
| ALG-13 | Cash balance atomic | Saloon `KasaServisi` | in/out delta | `CashAccount` | EPIC-LEG-008 |
| ALG-14 | Shift close variance | Saloon `KasaServisi` | expected vs actual | `CashShift` | EPIC-LEG-008 |
| ALG-15 | Stock count variance | Saloon `StokSayimServisi` | counted − system → movement | `StockCount` | EPIC-LEG-010 |
| ALG-16 | Auto journal from sale | Finance `AccountingService` | cash/card debit, revenue, KDV | `FinanceJournalEntry` | EPIC-LEG-005 |
| ALG-17 | TCMB FX fetch | emare-crm `DovizService` | XML parse, daily rate | `CurrencyRate` | EPIC-LEG-021 |
| ALG-18 | Installment schedule | Finance `TaksitServisi` | N installment plan | `InstallmentPlan` | EPIC-LEG-008 |
| ALG-19 | Supplier scorecard | Finance `ProcurementReportController` | delivery, match, price rates | `SupplierScorecard` | EPIC-LEG-010 |
| ALG-20 | Reorder suggestions | Finance `ProcurementReportController` | stock vs consumption | `ReorderSuggestion` | EPIC-LEG-013 |
| ALG-21 | Workstation capacity | Finance `Workstation` | capacity_per_hour | `Workstation` | EPIC-LEG-013 |
| ALG-22 | Expected cash day-end | Finance `GunSonuServisi` | cash_in − cash_out + sales | `CashDayEnd` | EPIC-LEG-008 |
| ALG-23 | Ticket load balance | emare-crm `TicketRoutingService` | open ticket count per agent | `TicketAssignment` | EPIC-LEG-018 |
| ALG-24 | SLA risk hours | emare-crm `SupportDashboard` | acil 4h, yüksek 8h, normal 24h | `SupportTicket` | EPIC-LEG-018 |
| ALG-25 | Marketplace price/stock | Finance `TrendyolService` | payload normalize | `MarketplaceListing` | EPIC-LEG-021 |
| ALG-26 | Proposal net value | Elyafgroup `CrmProposal` | Value × (1 − discount%) | `CrmProposal` | EPIC-LEG-003 |
| ALG-27 | Crm opportunity pipeline | Elyafgroup stage string | New → Won/Lost | `CrmOpportunity` | EPIC-LEG-002 |
| ALG-28 | DocumentSeries next | Finance `DocumentSeries` | atomic next_number, reset | `DocumentSeries` | EPIC-LEG-022 |
| ALG-29 | NumberSequence tenant | Elyafgroup `NumberSequenceService` | CR-/PR- per tenant | `NumberSequence` | EPIC-LEG-003 |

---

## Stok Yöntemi Conflict

| Yöntem | Kaynak | BOS önerisi |
|--------|--------|-------------|
| Hareket tabanlı | Emare Finance | Primary |
| FIFO lot | raporlama-app | Costing layer — **Needs Architect Review** |

---

## Port Stratejisi

1. Invariant → xUnit (Finance testlerinden)
2. Service interface → Application layer
3. Legacy PHP **kopyalanmaz** — pseudocode + test case
