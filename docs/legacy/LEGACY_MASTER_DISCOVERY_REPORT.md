# Legacy Master Discovery Report — TASK 022 v2.0

**Agent:** 6 — Enterprise Knowledge Architect  
**Program:** Legacy Knowledge Integration  
**Version:** 2.0  
**Tarih:** 2026-06-28  
**Workspace:** `/Users/emre/Elyafgroup`  
**Kanonik çıktı klasörü:** `docs/legacy/`

---

## Executive Summary

15+ yıllık ERP/CRM bilgi birikimi **kod olarak değil**, Emare BOS resmi mimarisine dönüştürülebilir bilgi paketi haline getirildi. Legacy Laravel ERP (Emare Finance, emare-crm, Saloon) domain kanıtı taşır; Elyafgroup BOS hedef platform + Control Tower UI shell'dir. En büyük gap: **Control Tower veri katmanı** ve **tekstil domain**.

---

## Metrik Özeti

| Metrik | Değer |
|--------|-------|
| **İncelenen proje sayısı** | 35+ benzersiz (12 birincil canonical) |
| **İncelenen dosya sayısı (yaklaşık)** | ~2,186 kaynak dosya (518+665+108+895 canonical scan) |
| **Bulunan modül sayısı** | 37 modül karşılaştırması · 24 domain area |
| **Bulunan entity sayısı** | ~280+ legacy entity/model (186 emare-crm + Finance + BOS) |
| **Bulunan business rule sayısı** | **63+** catalogued (48 mined + 15 domain spec) |
| **Bulunan workflow sayısı** | **25** |
| **Bulunan algoritma sayısı** | **29** |
| **Bulunan KPI sayısı** | **37** legacy gerçek + **92** CT hedef |
| **Bulunan entegrasyon sayısı** | **37** |
| **Bulunan localization bileşeni** | **12** (emare-i18n + translation-manager + TCMB + RTL spec) |
| **Bulunan textile kavramı sayısı** | **28** terim · 3 gerçek entity · 15 mock/spec |
| **Önerilen Epic sayısı** | **22** (EPIC-LEG-001 … EPIC-LEG-022) |
| **Domain Gap sayısı** | **58** kapasite/gap |

---

## Oluşturulan Doküman Seti

| # | Dosya | Durum |
|---|-------|-------|
| 1 | `LEGACY_PROJECT_INVENTORY.md` | ✅ TASK 021 + manifest |
| 2 | `LEGACY_ENTITY_CATALOG.md` | ✅ TASK 021-B |
| 3 | `LEGACY_BUSINESS_RULES.md` | ✅ TASK 021 + matrix ref |
| 4 | `LEGACY_REUSABILITY_REPORT.md` | ✅ TASK 021-B |
| 5 | `LEGACY_MIGRATION_STRATEGY.md` | ✅ v2.0 yeni |
| 6 | `LEGACY_WORKFLOWS.md` | ✅ 25 workflow |
| 7 | `LEGACY_ALGORITHMS.md` | ✅ 29 algoritma |
| 8 | `LEGACY_DASHBOARDS.md` | ✅ KPI intelligence |
| 9 | `LEGACY_INTEGRATIONS.md` | ✅ 37 entegrasyon |
| 10 | `LEGACY_DATABASE_PATTERNS.md` | ✅ 12 pattern |
| 11 | `LEGACY_TEXTILE_KNOWLEDGE.md` | ✅ textile gap |
| 12 | `DOMAIN_GAP_ANALYSIS.md` | ✅ 58 gap |
| 13 | `BUSINESS_RULE_MIGRATION_MATRIX.md` | ✅ 63+ kural |
| 14 | `EPIC_MIGRATION_PLAN.md` | ✅ 22 epic |
| 15 | `LEGACY_MASTER_DISCOVERY_REPORT.md` | ✅ bu dosya |
| 16 | `LEGACY_SCAN_PATHS.yaml` | ✅ manifest |
| 17 | `README.md` | ✅ Agent 6 charter v2.0 |

---

## En Kritik 25 İş Kuralı

1. Yevmiye borç = alacak (Finance JournalEntry)
2. Teklif onay workflow (emare-crm OnayMotoru + Elyaf CrmProposal)
3. Tenant izolasyonu (Elyafgroup + Finance BelongsToTenant)
4. CRM Account → Proposal zinciri
5. Yetersiz stokta transfer/satış engeli
6. Satış → ödeme → kasa observer (Saloon)
7. Import batch preview/rollback (raporlama-app)
8. Marketplace adapter + sync SLA (Emare Pazar)
9. BOM maliyet + fire oranı (Finance Bom)
10. MRP → PO önerisi (Finance MrpController)
11. İzin onayında bakiye düşürme (Finance Leave)
12. QC failed ≤ tested (domain spec)
13. Satın alma talebi → PO akışı (emare-crm Satinalma)
14. RBAC Module.Resource.Action (BOS Permissions)
15. SoD: talep eden ≠ onaylayan (OnayMotoru + ExpenseReport)
16. Segregation expense 2-stage (manager → finance)
17. DocumentSeries atomic numbering (Finance)
18. Split payment sum validation (Saloon)
19. FIFO lot cost allocation (raporlama-app)
20. Auto journal from sale (Finance AccountingService)
21. Ticket SLA breach escalation (Finance + emare-crm)
22. Blueprint approval pause (emare-crm)
23. UTC DateTime PostgreSQL (ANAYASA)
24. Generic Order yasak → SalesOrder (DOMAIN_MODEL)
25. Proposal net value discount formula (Elyafgroup CrmProposal)

Detay: `BUSINESS_RULE_MIGRATION_MATRIX.md` P0 tablosu.

---

## İlk Uygulanması Gereken 100 Keşif

| # | Tip | ID | Özet | Epic |
|---|-----|-----|------|------|
| 1 | Rule | BR-001 | MRP rule fields | EPIC-LEG-013 |
| 2 | Rule | BR-002 | MRP target stock | EPIC-LEG-013 |
| 3 | Rule | BR-003 | Projected demand | EPIC-LEG-013 |
| 4 | Rule | BR-004 | MRP→PO | EPIC-LEG-013 |
| 5 | Rule | BR-005 | BOM cost+scrap | EPIC-LEG-013 |
| 6 | Rule | BR-006 | Stock block sale | EPIC-LEG-010 |
| 7 | Rule | BR-007 | Sale stock movement | EPIC-LEG-010 |
| 8 | Rule | BR-008 | Sale reversal | EPIC-LEG-010 |
| 9 | Rule | BR-009 | Goods receipt post | EPIC-LEG-010 |
| 10 | Rule | BR-011 | PO approve draft-only | EPIC-LEG-010 |
| 11 | Rule | BR-013 | Landed unit cost | EPIC-LEG-013 |
| 12 | Rule | BR-017 | Expense SoD | EPIC-LEG-011 |
| 13 | Rule | BR-022 | OnayMotoru match | EPIC-LEG-011 |
| 14 | Rule | BR-023 | Approver SoD | EPIC-LEG-011 |
| 15 | Rule | BR-029 | Ticket SLA targets | EPIC-LEG-018 |
| 16 | Rule | BR-036 | Sale observer | EPIC-LEG-008 |
| 17 | Rule | BR-039 | Split payment | EPIC-LEG-008 |
| 18 | Rule | BR-041 | Cash atomic | EPIC-LEG-008 |
| 19 | Rule | BR-044 | Stock transfer | EPIC-LEG-012 |
| 20 | Rule | BR-048 | Proposal status TS | EPIC-LEG-003 |
| 21 | Workflow | WF-01 | OnayMotoru | EPIC-LEG-011 |
| 22 | Workflow | WF-03 | Expense approval | EPIC-LEG-005 |
| 23 | Workflow | WF-06 | PO lifecycle | EPIC-LEG-010 |
| 24 | Workflow | WF-18 | CrmProposal status | EPIC-LEG-003 |
| 25 | Algo | ALG-01 | MRP demand | EPIC-LEG-013 |
| 26 | Algo | ALG-04 | BOM unit cost | EPIC-LEG-013 |
| 27 | Algo | ALG-07 | FIFO lot | EPIC-LEG-010 |
| 28 | Algo | ALG-16 | Auto journal | EPIC-LEG-005 |
| 29 | KPI | total_revenue | CEO revenue | EPIC-LEG-007 |
| 30 | KPI | gross_profit | Finance CT | EPIC-LEG-008 |
| 31 | KPI | order_backlog | CEO spec | EPIC-LEG-004 |
| 32 | KPI | headcount | CEO spec | EPIC-LEG-009 |
| 33 | KPI | quality_reject | CEO spec | EPIC-LEG-017 |
| 34 | KPI | production_efficiency | CEO spec | EPIC-LEG-014 |
| 35 | KPI | budget_vs_actual | CEO menu | EPIC-LEG-007 |
| 36 | Entity | CrmAccount | Platform CRM | EPIC-LEG-002 |
| 37 | Entity | CrmProposal | + approval | EPIC-LEG-003 |
| 38 | Entity | SalesOrder | Missing | EPIC-LEG-004 |
| 39 | Entity | FinanceJournalEntry | Missing | EPIC-LEG-005 |
| 40 | Entity | FinanceInvoice | Missing | EPIC-LEG-006 |
| 41 | Entity | DecisionLog | CEO spec | EPIC-LEG-007 |
| 42 | Entity | MrpRule | Finance | EPIC-LEG-013 |
| 43 | Entity | BillOfMaterials | Finance | EPIC-LEG-013 |
| 44 | Entity | QcTestResult | Spec | EPIC-LEG-017 |
| 45 | Entity | ElyafSample | Extend | EPIC-LEG-016 |
| 46 | Integration | INT-01 | Trendyol | EPIC-LEG-021 |
| 47 | Integration | INT-04 | Pazar registry | EPIC-LEG-021 |
| 48 | Integration | INT-08 | e-Fatura | EPIC-LEG-021 |
| 49 | Integration | INT-13 | Import batch | EPIC-LEG-008 |
| 50 | DB | DB-04 | DocumentSeries | EPIC-LEG-022 |
| 51 | Security | Tenant filter | AppDbContext | — |
| 52 | Security | Soft delete | Interceptor | — |
| 53 | Security | Feature gate | RequireFeature | — |
| 54 | Textile | Fabric | Mock only | EPIC-LEG-016 |
| 55 | Textile | AQL | Mock only | EPIC-LEG-017 |
| 56 | Textile | Sample | ElyafSample | EPIC-LEG-016 |
| 57 | Gap | CT mock fallback | ElyafDashboardService | EPIC-LEG-007 |
| 58 | Gap | Two CRM models | Customer vs CrmAccount | EPIC-LEG-018 |
| 59 | Epic | EPIC-LEG-002 | CRM API | Sprint N |
| 60 | Epic | EPIC-LEG-003 | Proposal approval | Sprint N+1 |
| 61 | Epic | EPIC-LEG-004 | SalesOrder | Sprint N+2 |
| 62 | Epic | EPIC-LEG-005 | Finance journal | Sprint N+3 |
| 63 | Epic | EPIC-LEG-006 | Invoice/payment | Sprint N+4 |
| 64 | Epic | EPIC-LEG-007 | CT data layer | Sprint N+4–7 |
| 65 | Epic | EPIC-LEG-008 | Report/import | Paralel |
| 66 | Epic | EPIC-LEG-009 | HR | Sprint N+5 |
| 67 | Epic | EPIC-LEG-010 | Inventory | Sprint N+5 |
| 68 | Epic | EPIC-LEG-011 | Workflow engine | Sprint N+1 |
| 69 | Epic | EPIC-LEG-012 | Logistics | Sprint N+6 |
| 70 | Epic | EPIC-LEG-013 | BOM/MRP | Sprint N+6 |
| 71 | Epic | EPIC-LEG-014 | WorkOrder | Sprint N+7 |
| 72 | Epic | EPIC-LEG-015 | i18n central | Paralel |
| 73 | Epic | EPIC-LEG-016 | Textile | Faz 5 |
| 74 | Epic | EPIC-LEG-017 | QC | Faz 5 |
| 75 | Epic | EPIC-LEG-018 | Ticket↔ERP | Sprint N+2 |
| 76 | Epic | EPIC-LEG-019 | Omnichannel WF | v2 |
| 77 | Epic | EPIC-LEG-020 | Reseller | v2+ |
| 78 | Epic | EPIC-LEG-021 | e-Belge/market | v2 |
| 79 | Epic | EPIC-LEG-022 | Doc numbering | Sprint N+1 |
| 80 | Workflow | WF-07 | Goods receipt | EPIC-LEG-010 |
| 81 | Workflow | WF-15 | Satinalma onay | EPIC-LEG-010 |
| 82 | Algo | ALG-12 | Split payment | EPIC-LEG-008 |
| 83 | Algo | ALG-19 | Supplier score | EPIC-LEG-010 |
| 84 | Algo | ALG-28 | DocumentSeries | EPIC-LEG-022 |
| 85 | KPI | low_stock_count | Alert | EPIC-LEG-010 |
| 86 | KPI | slaRiskindekiler | Support | EPIC-LEG-018 |
| 87 | Integration | INT-19 | TCMB FX | EPIC-LEG-021 |
| 88 | Integration | INT-06 | Webhook retry | EPIC-LEG-021 |
| 89 | Rule | BR-024 | Reject skip steps | EPIC-LEG-011 |
| 90 | Rule | BR-034 | PR submit approval | EPIC-LEG-010 |
| 91 | Rule | BR-046 | Stock count var | EPIC-LEG-010 |
| 92 | Workflow | WF-02 | Blueprint engine | EPIC-LEG-011 |
| 93 | Workflow | WF-20 | Import queue | EPIC-LEG-008 |
| 94 | DB | DB-06 | ProductBatch | EPIC-LEG-016 |
| 95 | Textile | Collection/Style | Entity | EPIC-LEG-016 |
| 96 | Gap | Payroll | None | v2+ |
| 97 | Gap | Maintenance | None | v2+ |
| 98 | Conflict | C-01 | CRM dual model | Architect |
| 99 | Conflict | BC-01 | FIFO vs movement | Architect |
| 100 | Process | Pre-flight 10 doc | Mandatory | EPIC-LEG-001 |

---

## Sprint Planına Etkisi

| Sprint | Blocker keşifler | Epic |
|--------|------------------|------|
| **2A gate** | CRM API, Proposal approval, SalesOrder spec, CEO KPI mock kaldırma | 002, 003, 004, 007, 022 |
| **2B gate** | Finance journal, invoice, Finance CT KPI | 005, 006, 007 |
| **3+** | Inventory, BOM, textile, QC | 010, 013, 016, 017 |

Legacy bilgi paketi olmadan Sprint 2 gate **gerçek veri** ile geçilemez.

---

## Riskler

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-GAP-01 | Mock CT → müşteri beklentisi | Critical | EPIC-LEG-007 öncelik |
| R-GAP-03 | Textile domain boş | Critical | SME + EPIC-LEG-016 |
| R-GAP-04 | Laravel→.NET port hatası | High | Test port, kod kopyalama yok |
| R-GAP-05 | UTC DateTime | Medium | ANAYASA enforcement |
| R-LEG-01 | Doküman drift public/private | Medium | EPIC-LEG-001 sync |

---

## Chief Architect'e Öneriler

1. **Onay:** `DOMAIN_GAP_ANALYSIS.md` + `EPIC_MIGRATION_PLAN.md` — Sprint 2 gate öncesi zorunlu referans
2. **Karar iste:** CRM Customer → CrmAccount birleşim zamanlaması (Conflict C-01)
3. **Karar iste:** FIFO lot vs movement-only stok modeli (Conflict BC-01)
4. **Karar iste:** DocumentSeries birleşik numara engine (EPIC-LEG-022)
5. **Textile:** SME workshop — mock CT görselleri final kabul; domain yok
6. **Workflow:** Tek ERP ApprovalWorkflow engine onayı (OnayMotoru + ExpenseReport + Blueprint)
7. **Traceability:** `FEATURE_TRACEABILITY_MATRIX.md` Legacy Epic sütunu — her widget EPIC referansı
8. **Agent 6 kalıcı rol:** Yeni legacy bulunduğunda manifest + ilgili discovery dosyası güncelleme

---

## Başarı Kriteri Değerlendirmesi

| Kriter | Durum |
|--------|-------|
| Legacy BOS resmi bilgi kaynağı | ✅ `docs/legacy/` 17 dosya |
| Her Epic dokümandan referans alabilir | ✅ EPIC_MIGRATION_PLAN + matrix |
| Kod değil bilgi taşındı | ✅ Kod yazılmadı/değiştirilmedi |
| Analiz sürdürülebilir | ✅ LEGACY_SCAN_PATHS.yaml + Agent 6 v2.0 charter |
| FEATURE_TRACEABILITY güncellendi | ✅ Legacy Epic referans bölümü |
| Public repo commit | ⏳ kullanıcı onayı ile |

---

## Sonraki Adımlar

1. Chief Architect → `ARCHITECT_REVIEW_TASK_022.md`
2. Public repo → `docs/legacy/` push
3. Agent 1 → EPIC-LEG-002 implementation task
4. Agent 6 (incremental) → yeni legacy path bulunduğunda manifest güncelle

---

*Agent 6 — Enterprise Knowledge Architect · Legacy Knowledge Integration Program v2.0*  
*Kod içermez · Hassas veri içermez*
