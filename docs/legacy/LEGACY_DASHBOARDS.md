# Legacy Dashboard Intelligence — KPI Discovery

**Version:** 2.0 · **Task:** 022 · **Agent:** 6  
**BOS hedef:** `CONTROL_TOWER_FINAL_SCOPE.md`, `FEATURE_TRACEABILITY_MATRIX.md`

---

## Özet

| Kaynak proje | KPI / metrik sayısı |
|--------------|---------------------|
| Emare Finance | 19 |
| emare-crm | 6 |
| raporlama-app | 8 |
| Elyafgroup CT (mock/seed) | 120+ (spec) |
| Saloon | 4 |
| **Legacy kod KPI (gerçek hesap)** | **37** |
| **CT hedef KPI (traceability)** | **92** (Sprint 2 gate) |

---

## Legacy KPI → Control Tower Eşlemesi

| Legacy KPI | Hesaplama (legacy) | Kaynak | BOS Control Tower | BOS Entity | Epic | Durum |
|------------|-------------------|--------|-------------------|------------|------|-------|
| total_revenue | SUM(grand_total) completed sales | Finance DashboardController | CEO monthly revenue | SalesOrder | EPIC-LEG-007 | GAP |
| month_change | MoM revenue % | Finance DashboardController | CEO snapshot trend | KPIValue | EPIC-LEG-007 | GAP |
| low_stock_count | stock ≤ critical | Finance DashboardController | Production critical alerts | InventoryItem | EPIC-LEG-010 | GAP |
| monthly_debit/credit | posted journal sums | Finance AccountingController | Finance KPI | FinanceJournalEntry | EPIC-LEG-005 | GAP |
| gross_profit | revenue − landed − commission | Finance ReportController | Finance / CEO EBITDA proxy | SalesAnalytics | EPIC-LEG-008 | GAP |
| deliveryRate | supplier scorecard | Finance ProcurementReport | Supplier panel | SupplierScorecard | EPIC-LEG-010 | GAP |
| acikTalepSayisi | open tickets | emare-crm SupportDashboard | Ticket KPI (ops) | SupportTicket | — | Partial BOS |
| slaRiskindekiler | priority hour thresholds | emare-crm SupportDashboard | CEO critical alerts | SupportTicket | EPIC-LEG-018 | Partial |
| executive revenue delta | period-over-period | emare-crm GenerateExecutiveReport | CEO executive snapshot | KPIValue | EPIC-LEG-007 | GAP |
| profit_margin | comparison report | raporlama-app ReportController | Finance reports | SalesAnalytics | EPIC-LEG-008 | GAP |
| stockWarnings | SUM(lot) < 5 | raporlama-app ReportController | Warehouse KPI | StockLot | EPIC-LEG-010 | GAP |
| cash/card/credit split | payment method agg | raporlama-app ReportApi | Finance cash position | FinancePayment | EPIC-LEG-006 | GAP |
| AQL pass rate | mock string only | Elyaf mockData.ts | QC Control Tower | QcTestResult | EPIC-LEG-017 | Mock only |
| OTD risk | ElyafStyle field | Elyafgroup domain | Merchandising CT | ElyafStyle | EPIC-LEG-016 | Partial entity |
| production efficiency | mock KPI | Elyaf seed | CEO KPI | ProductionWorkOrder | EPIC-LEG-014 | Mock only |
| headcount | — (spec only) | CONTROL_TOWER CEO | CEO KPI | HrEmployee | EPIC-LEG-009 | GAP |
| order backlog | — (spec only) | CONTROL_TOWER CEO | CEO KPI | SalesOrder | EPIC-LEG-004 | GAP |
| quality reject rate | — (spec only) | CONTROL_TOWER CEO | CEO KPI | QcTestResult | EPIC-LEG-017 | GAP |
| NPS | — (spec only) | CONTROL_TOWER CEO | CEO KPI | KPIValue | EPIC-LEG-007 | GAP |
| budget vs actual | — (spec only) | CONTROL_TOWER CEO | CEO menu screen | BudgetTarget | EPIC-LEG-007 | GAP |

---

## Dashboard Mantığı (legacy pattern)

| Pattern | Legacy | BOS hedef |
|---------|--------|-----------|
| Executive snapshot command | emare-crm `GenerateExecutiveReport` | Scheduled read-model refresh |
| Finance panel cache | emare-crm `FinanceDashboardSnapshotCommand` | KPI snapshot table |
| 7-day chart | Finance DashboardController | Time-series projection |
| Top-N ranking | Finance ReportController products | Paginated query |
| Seed fallback | Elyaf `ElyafDashboardService` | **Kaldırılacak** — EPIC-LEG-007 |

---

## KPI Veri Hattı (hedef)

```text
Domain Event → Outbox → Projection Handler → KPIValue / ReadModel
                                              ↓
                              Control Tower Query Handler → API → UI
```

Legacy'de çoğu KPI **doğrudan SQL aggregate** (controller içi). BOS'ta projection zorunlu (ANAYASA + traceability).

---

## Needs Architect Review

- EBITDA vs gross profit tanımı Finance CT'de — **Needs Architect Review**
- CEO "production efficiency" formülü — legacy'de yok, SME gerekli
