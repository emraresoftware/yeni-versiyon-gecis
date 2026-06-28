# Domain Gap Analysis — BOS vs Legacy

**Version:** 2.0 · **Task:** 022 · **Agent:** 6  
**Önceki:** `project-management/legacy/ARCHITECTURE_GAP_MATRIX.md` (v1) — bu dosya kanonik v2

---

## Özet

| Metrik | v1 (022) | v2 (022 program) |
|--------|----------|------------------|
| Gap kapasitesi | 42 | **58** |
| P0 | 11 | **13** |
| Epic | 21 | **22** (+ EPIC-LEG-022 DocumentSeries) |
| Domain keşfi | — | **24 bounded area** |

**Format:** `[LEGACY] → BOS hedef → GAP → EPIC → Öncelik`

---

## Domain Discovery Matrix

| Domain area | Legacy olgunluk | BOS durumu | Gap | Epic |
|-------------|-----------------|------------|-----|------|
| CRM | ★★★★ | Kısmi entity | API, approval | EPIC-LEG-002 |
| Sales | ★★★★ | Spec only | SalesOrder | EPIC-LEG-004 |
| Finance | ★★★★★ | Stub UI | Full backend | EPIC-LEG-005/006 |
| Inventory | ★★★★ | Spec | Handlers | EPIC-LEG-010 |
| Warehouse | ★★★★ | Spec | Warehouse CRUD | EPIC-LEG-010 |
| Purchasing | ★★★★ | Yok | PO flow | EPIC-LEG-010 |
| Production | ★★★★ | Mock | BOM/MRP | EPIC-LEG-013 |
| MRP | ★★★★★ | Yok | MrpRule | EPIC-LEG-013 |
| BOM | ★★★★★ | Yok | Bom aggregate | EPIC-LEG-013 |
| Costing | ★★★★ | Yok | unitCost+fire | EPIC-LEG-013 |
| HR | ★★★★ | Stub | Employee/Leave | EPIC-LEG-009 |
| Payroll | ★★ | Yok | v2+ | — |
| Planning | ★★★ | Mock | Capacity | EPIC-LEG-013 |
| Maintenance | ★ | Yok | v2+ | — |
| Quality | ★★★ | Spec+mock | Qc module | EPIC-LEG-017 |
| Compliance | ★★ | Mock CT | v2 | — |
| Ticket | ★★★★★ | Olgun | ERP bridge | EPIC-LEG-018 |
| AI | ★★★★★ | Olgun | Workflow merge | EPIC-LEG-019 |
| Reseller | ★★★ | Stub | v2 | EPIC-LEG-020 |
| Localization | ★★★★ | Kısmi | Central mgmt | EPIC-LEG-015 |
| Control Tower | ★★★ (UI) | Mock data | Data layer | EPIC-LEG-007 |
| Textile | ★ (mock) | Hafif entity | Full domain | EPIC-LEG-016 |
| Laboratory | ★ (mock) | Yok | SME | EPIC-LEG-016 |
| Merchandising | ★★★ | Entity | Workflow | EPIC-LEG-016 |
| Sample | ★★★ | Entity | Workflow | EPIC-LEG-016 |
| Capacity / Forecast / OEE / MES / APS | ★ (mock) | Yok | SME | EPIC-LEG-016 |

---

## Kritik P0 Gap'ler

1. Finance JournalEntry + borç=alacak — Finance standalone kanıt, BOS yok
2. SalesOrder — traceability CEO KPI blocker
3. CrmProposal approval — üç legacy kaynak, BOS workflow yok
4. Control Tower 92 widget — ~%5 implemented
5. DecisionLog — CEO spec, entity yok
6. Mock KPI fallback — ElyafDashboardService seed

---

## Gap → Sprint Etkisi

| Sprint gate | Blocker gap |
|-------------|-------------|
| Sprint 2A (CEO/Sales CT) | EPIC-LEG-002, 003, 004, 007 |
| Sprint 2B (Finance CT) | EPIC-LEG-005, 006, 007 |
| Sprint 3 (Ops towers) | EPIC-LEG-010, 013, 016, 017 |

---

## Conflicts

See `LEGACY_MIGRATION_STRATEGY.md` § Conflict Kayıtları

---

## Risk Register (gap-derived)

| ID | Risk | Severity |
|----|------|----------|
| R-GAP-01 | Mock CT prod beklentisi | Critical |
| R-GAP-03 | Textile domain empty | Critical |
| R-GAP-04 | Laravel→.NET port error | High |
| R-GAP-05 | UTC DateTime legacy | Medium |

---

## Referans

Detay epic tanımları: `EPIC_MIGRATION_PLAN.md`  
İş kuralı detay: `BUSINESS_RULE_MIGRATION_MATRIX.md`
