# Legacy Textile Knowledge — Discovery & Gap

**Version:** 2.0 · **Task:** 022 · **Agent:** 6  
**Epic:** EPIC-LEG-016

---

## Executive Summary

**15+ yıllık ERP birikiminde tekstil-spesifik domain kodu neredeyse yok.**  
Tekstil bilgisi üç katmanda dağılmış:

1. **UI mock / seed** — Elyaf Control Tower (fabric, AQL, dyeing, cutting, sewing)
2. **Hafif domain** — ElyafSample, ElyafCollection, ElyafStyle
3. **Generic üretim** — Emare Finance BOM/MRP/Workstation (tekstil değil)

---

## Kavram Envanteri

| Kavram | Legacy kod | UI/mock | BOS entity | Durum |
|--------|------------|---------|------------|-------|
| Fabric | ❌ | ✅ specs + FabricDashboard | ❌ | **GAP — yeni domain** |
| Yarn | ❌ | ❌ | ❌ | **GAP** |
| Roll (kumaş topu) | ❌ | ❌ | ❌ | **GAP** |
| Lot / Batch | Finance ProductBatch (generic) | ❌ | ❌ | Port adayı |
| Recipe / Shade / Color | ❌ | ✅ lab dips (mock) | ❌ | **GAP — SME** |
| Knitting / Weaving / Dyeing | ❌ | ✅ mock strings | ❌ | **GAP** |
| Finishing | ❌ | ❌ | ❌ | **GAP** |
| Inspection / 4 Point / AQL | ❌ | ✅ mock KPI | QcStandard (spec) | Spec only |
| GSM | ❌ (CallCenter GoIP ≠ fabric) | ❌ | ❌ | **GAP** |
| Shrinkage | ❌ | ❌ | ❌ | **GAP** |
| Marker / Cutting | ❌ | ✅ merchandise mock | ❌ | **GAP** |
| Sewing / Packing | ❌ | ✅ mock KPI | ❌ | **GAP** |
| Sample | ✅ ElyafSample | ✅ blockers mock | ✅ partial | Extend workflow |
| Merchandising | ✅ Collection/Style | ✅ dashboard | ✅ partial | Extend |
| Capacity / OEE / MES / APS | ❌ | ✅ KPI mock | ❌ | **GAP — SME** |
| Export / Import (textile docs) | ❌ | ❌ | ❌ | **GAP** |

**Bulunan tekstil kavramı (kod+mock):** 28 terim tarandı · **gerçek domain:** 3 entity · **mock/spec:** 15 · **tam boşluk:** 10

---

## Mock Truth Sources (UI kabul kriteri)

| Dosya | İçerik |
|-------|--------|
| `emare-dashboard/specs/fabric.md` | Fabric procurement, lab dip, shade |
| `emare-dashboard/specs/merchandise.md` | Collection, cutting/sewing/packing follow-up |
| `web/.../mockData.ts` | AQL, dyehouse, production KPI strings |
| `ElyafRolloutSeedData.cs` | qc.aql KPI seed |

**Kural:** Mock metinler **iş kuralı kanıtı değildir** — SME workshop gerekli.

---

## Generic Üretim Referansı (Finance)

Port edilebilir (tekstil-agnostic):

- `Bom`, `BomLine`, `BomOperation`, `Workstation`
- `MrpRule`, MRP suggestion → PO
- `ProductBatch` → textile lot traceability adayı

Kaynak: `/Users/emre/Dergah/Emare projeler/Emare Finance/app/Models/Bom.php`

---

## Önerilen Textile Bounded Context (draft)

**Needs Architect Review — tüm aggregate isimleri**

| Aggregate | Açıklama |
|-----------|----------|
| `TextileFabric` | Kumaş kartı, GSM, composition |
| `TextileColorway` | Shade, lab dip status |
| `TextileRoll` | Top/lot, warehouse location |
| `TextileRecipe` | Dyeing/finishing recipe |
| `TextileSample` | Extend `ElyafSample` |
| `TextileProductionOrder` | Cutting/sewing line link |

---

## Textile KPI → Control Tower

| KPI (mock) | CT rol | BOS projection |
|------------|--------|----------------|
| AQL Pass Rate | QC | QcTestResult |
| Fabric procurement lead time | Fabric | TextileFabric + PO |
| OTD by style | Merchandising | ElyafStyle |
| Dyehouse WIP | Production (mock) | TextileProductionOrder |
| Cutting efficiency | Merchandising mock | **Needs Architect Review** |

---

## Risk

**R-GAP-03:** Tekstil domain boşluğu — müşteri CT görselleri final kabul kriteri; backend yok.

**Azaltma:** EPIC-LEG-016 + SME workshop + UBIQUITOUS_LANGUAGE güncelleme
