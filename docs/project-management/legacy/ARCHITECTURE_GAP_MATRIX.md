# Architecture Gap Matrix — TASK 022

**Tarih:** 2026-06-28  
**Agent:** 6 (Enterprise Knowledge Architect)  
**Girdi:** TASK 021/021-B legacy envanter, `DOMAIN_MODEL.md`, `CONTROL_TOWER_FINAL_SCOPE.md`, `FEATURE_TRACEABILITY_MATRIX.md`  
**Format:** `[LEGACY: kaynak] → [BOS: hedef] → GAP → EPIC`

---

## Özet

| Metrik | Değer |
|--------|-------|
| Analiz edilen modül/kapasite | 42 |
| Tam karşılık (gap yok / olgun) | 4 |
| Kısmi (entity veya UI var, backend eksik) | 18 |
| Tam boşluk (spec only veya yok) | 20 |
| P0 gap | 11 |
| P1 gap | 16 |
| P2 gap | 11 |
| P3 / ayrı ürün | 4 |

**Kritik tema:** Control Tower ve traceability matrisi **hedef API/entity katmanını tanımlıyor**; Elyafgroup'ta çoğu widget hâlâ mock/seed. Legacy Laravel ERP (Emare Finance, emare-crm) **domain kanıtı** taşır; .NET BOS'a port edilmedi.

---

## Gap Matrisi — Platform & Omnichannel

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 1 | Elyafgroup Platform kernel | Tenant, RBAC, Outbox, Audit | Olgun — sürekli iyileştirme | — | — |
| 2 | Elyafgroup EmareTicket | Service Desk, omnichannel | Olgun — ERP ile entegrasyon eksik | EPIC-LEG-018 | P2 |
| 3 | emare-crm Blueprint + OnayAkisi | ERP workflow engine | Ticket workflow var; ERP onay yok | EPIC-LEG-011 | P1 |
| 4 | emareasistan ResponseRule | AI action + workflow | Kısmi AI; kanal workflow birleşik değil | EPIC-LEG-019 | P2 |
| 5 | translation-manager | emare-i18n + CT i18n | Paket var; merkezi key yönetimi yok | EPIC-LEG-015 | P1 |
| 6 | yeni-versiyon-gecis ADR | BOS dokümantasyon | Devam eden senkron | EPIC-LEG-001 | P0 |

---

## Gap Matrisi — CRM & Sales

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 7 | Elyafgroup + emare-crm CrmAccount/Contact | Platform CRM entities | Domain olgun; API/handler kısmi (Task 013+) | EPIC-LEG-002 | P0 |
| 8 | emare-crm Firsat + Floragenix Lead | CrmOpportunity pipeline | Entity var; stage kuralları + API eksik | EPIC-LEG-002 | P0 |
| 9 | Üç projede Teklif/Proposal | CrmProposal + approval | Entity var; `CrmProposalApproval` workflow yok | EPIC-LEG-003 | P0 |
| 10 | Finance Sale + Ticket Order | SalesOrder aggregate | DOMAIN_MODEL tanımlı; kod yok | EPIC-LEG-004 | P0 |
| 11 | Floragenix dealer hierarchy | Reseller / bayi modeli | Kısmi Reseller Portal stub | EPIC-LEG-020 | P3 |
| 12 | emare-crm Kampanya | Sales campaign | Yok | EPIC-LEG-020 | P3 |

---

## Gap Matrisi — Finance

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 13 | Emare Finance AccountPlan | FinanceAccountPlan | Stub UI; entity/handler yok | EPIC-LEG-005 | P0 |
| 14 | Emare Finance JournalEntry | FinanceJournalEntry | Borç=alacak kuralı legacy'de kanıtlı; BOS yok | EPIC-LEG-005 | P0 |
| 15 | Emare Finance Invoice/Payment | FinanceInvoice, FinancePayment | Yok | EPIC-LEG-006 | P0 |
| 16 | Finance EInvoice/ESmm | e-Belge entegrasyon | Yok | EPIC-LEG-021 | P2 |
| 17 | CONTROL_TOWER CEO Budget vs Actuals | BudgetTarget, BudgetLine | Spec + traceability; entity yok | EPIC-LEG-007 | P1 |
| 18 | Finance CurrencyRate | Döviz kuru | Yok | EPIC-LEG-021 | P2 |
| 19 | Emare Saloon kasa observer | Satış→ödeme→kasa | Perakende pattern; BOS ERP'de yok | EPIC-LEG-008 | P1 |

---

## Gap Matrisi — HR

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 20 | Emare Finance Employee/Leave | HrEmployee, HrLeave | Stub UI; entity yok | EPIC-LEG-009 | P1 |
| 21 | Finance izin bakiye düşürme | HrLeave approval | İş kuralı legacy testte; BOS yok | EPIC-LEG-009 | P1 |
| 22 | CONTROL_TOWER CEO headcount KPI | HrEmployee projection | KPI spec var; veri yok | EPIC-LEG-009 | P1 |

---

## Gap Matrisi — Inventory, Purchasing, Logistics

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 23 | Finance StockMovement + Depo | LogisticsWarehouse, StockMovement | DOMAIN_MODEL tanımlı; kod yok | EPIC-LEG-010 | P1 |
| 24 | emare-crm SatinalmaTalebi | Purchase requisition | Yok | EPIC-LEG-010 | P1 |
| 25 | Finance PO + GoodsReceipt | Purchasing flow | Yok | EPIC-LEG-010 | P1 |
| 26 | DOMAIN_MODEL transfer kuralı | LogisticsStockTransfer | Yetersiz stok kuralı spec'te; kod yok | EPIC-LEG-012 | P2 |
| 27 | Finance Shipment | LogisticsShipment | Kısmi legacy; BOS yok | EPIC-LEG-012 | P2 |
| 28 | Finance ProductBatch/Serial | Lot traceability | Textile adayı; BOS yok | EPIC-LEG-016 | P2 |

---

## Gap Matrisi — Production, Planning, Costing

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 29 | Emare Finance BOM | Production BOM | Test coverage legacy'de; BOS yok | EPIC-LEG-013 | P1 |
| 30 | Emare Finance MRP | MrpRule, MrpSuggestion | Yok | EPIC-LEG-013 | P1 |
| 31 | Finance Bom::unitCost + fire | Costing | İş kuralı kanıtlı; BOS yok | EPIC-LEG-013 | P1 |
| 32 | Finance Workstation, BomOperation | Routing | Genel üretim referansı; BOS yok | EPIC-LEG-013 | P1 |
| 33 | Traceability ProductionWorkOrder | ProductionWorkOrder | CEO KPI hedefi; entity yok | EPIC-LEG-014 | P2 |
| 34 | — | Yarn/Dyeing/Knitting/Weaving | Tekstil domain sıfırdan | EPIC-LEG-016 | P2 |

---

## Gap Matrisi — QC & Compliance

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 35 | emare-crm VeriKaliteKurali | QcStandard, QcTestResult | Entity spec; handler yok | EPIC-LEG-017 | P2 |
| 36 | QC failed≤tested kuralı | QcClaim | İş kuralı dokümante; kod yok | EPIC-LEG-017 | P2 |
| 37 | CONTROL_TOWER quality reject KPI | QcTestResult projection | Mock KPI | EPIC-LEG-017 | P2 |

---

## Gap Matrisi — Control Tower & CEO

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 38 | Elyafgroup 16 rol CT UI | Control Tower shell | UI + seed olgun; backend mock | EPIC-LEG-007 | P0 |
| 39 | FEATURE_TRACEABILITY 100+ widget | API/Query/Handler | Traceability onaylı; uygulama %5 altı | EPIC-LEG-007 | P0 |
| 40 | — | DecisionLog + approval | CEO spec; entity/handler yok | EPIC-LEG-007 | P0 |
| 41 | ElyafKpiSnapshot mock | KPIValue projection | Mock→DB projection yok | EPIC-LEG-007 | P0 |
| 42 | ElyafSample, ElyafCollection, ElyafStyle | Textile ops CT | Entity hafif; workflow yok | EPIC-LEG-016 | P2 |

---

## Gap Matrisi — Reporting, Marketplace, Entegrasyon

| # | [LEGACY] | BOS hedef | GAP | EPIC | Öncelik |
|---|----------|-------|-----|------|---------|
| 43 | raporlama-app import batch | DataImportBatch | Yok | EPIC-LEG-008 | P1 |
| 44 | raporlama-app 10 rapor tipi | Reporting suite | Ticket reports olgun; ERP rapor yok | EPIC-LEG-008 | P1 |
| 45 | Emare Pazar 14 adapter | Marketplace sync | Yok | EPIC-LEG-008 | P1 |
| 46 | ecomaiq Trendyol Q&A | E-commerce QA | Yok | EPIC-LEG-021 | P3 |
| 47 | emarecc tahsilat CC | Call center collections | Ticket CC olgun; tahsilat modülü ayrı | EPIC-LEG-019 | P2 |

---

## Ayrı Ürün / Taşınmamalı (Gap Değil)

| [LEGACY] | Karar | Gerekçe |
|----------|-------|---------|
| emarepos restoran POS | Ayrı ürün | Restoran SaaS; BOS ERP kapsamı dışı |
| emareciftlik tarım ERP | Vertical ayrı | Tekstil BOS ile birleştirilmez |
| Dervişler/worktree kopyaları | Ignore | dedup manifest |
| emarerp gömülü Finance | Obsolete | Standalone Finance birincil |
| Desktop Ticket snapshot | Obsolete | Elyafgroup canonical |

---

## Gap → Faz Eşlemesi

| Faz | EPIC'ler | Sprint hedefi (öneri) |
|-----|----------|------------------------|
| **Faz 0** (devam) | EPIC-LEG-001, EPIC-LEG-002 | CRM API + doküman senkron |
| **Faz 1** | EPIC-LEG-003, EPIC-LEG-004 | Proposal approval + SalesOrder |
| **Faz 2** | EPIC-LEG-005, EPIC-LEG-006 | Finance core |
| **Faz 3** | EPIC-LEG-010, EPIC-LEG-012 | Stok + lojistik |
| **Faz 4** | EPIC-LEG-013, EPIC-LEG-014 | BOM/MRP/WorkOrder |
| **Faz 5** | EPIC-LEG-016, EPIC-LEG-017 | Textile + QC |
| **Faz 6** | EPIC-LEG-007 | Control Tower veri katmanı |
| **Paralel** | EPIC-LEG-008, EPIC-LEG-011, EPIC-LEG-015 | Rapor, workflow, i18n |

---

## Risk Bayrakları

| Risk ID | GAP alanı | Etki | Azaltma |
|---------|-----------|------|---------|
| R-GAP-01 | Mock CT → prod beklentisi | Yüksek | EPIC-LEG-007 önce CEO/Sales/Finance kuleleri |
| R-GAP-02 | İki CRM modeli (Ticket Customer vs Platform CrmAccount) | Orta | Platform canonical; migration planı |
| R-GAP-03 | Textile domain boşluğu | Yüksek | SME workshop + EPIC-LEG-016 |
| R-GAP-04 | Laravel→.NET port hatası | Yüksek | İş kuralı + test port; kod kopyalama yasak |
| R-GAP-05 | UTC DateTime legacy ihlalleri | Orta | ANAYASA enforcement migration'da |

---

## Sonraki Adım

- **EPIC_BACKLOG_FROM_LEGACY.md** — her EPIC için kabul kriteri ve bağımlılık
- **Agent 1** — EPIC-LEG-002/003/005 sırasıyla implementation task'ları
- **Chief Architect** — gap matrisi onayı (`ARCHITECT_REVIEW_TASK_022.md`)
