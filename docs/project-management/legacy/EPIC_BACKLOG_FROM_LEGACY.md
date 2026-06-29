# Epic Backlog from Legacy — TASK 022

**Tarih:** 2026-06-28  
**Agent:** 6 (Enterprise Knowledge Architect)  
**Kaynak:** `ARCHITECTURE_GAP_MATRIX.md`, TASK 021 legacy analizi  
**Format:** Her epic → legacy kanıt → BOS hedef → kabul kriteri

---

## Öncelik Sözlüğü

| Kod | Anlam |
|-----|-------|
| P0 | Control Tower / Sprint gate blocker |
| P1 | ERP çekirdek modül |
| P2 | Operasyon genişletme |
| P3 | v2+ veya ayrı ürün |

---

## EPIC-LEG-001 — Mimari Blueprint Senkronizasyonu

| Alan | Değer |
|------|-------|
| **Öncelik** | P0 |
| **Legacy** | yeni-versiyon-gecis ADR, traceability |
| **BOS hedef** | Elyafgroup `docs/product/*` kanonik |
| **GAP** | Public/private repo doküman drift |

**Kapsam:** ADR, DOMAIN_MODEL, FEATURE_TRACEABILITY değişikliklerinin iki repo arasında eşlenmesi.

**Kabul kriterleri:**
- [ ] Her Sprint gate öncesi traceability diff kontrolü
- [ ] Legacy analiz çıktıları private repo `legacy/` altında güncel
- [ ] Public repo'da kod yok (yalnızca rapor/mimari)

**Bağımlılık:** Yok  
**Tahmini effort:** Sürekli (her sprint 0.5 gün)

---

## EPIC-LEG-002 — CRM Çekirdek API & Pipeline

| Alan | Değer |
|------|-------|
| **Öncelik** | P0 |
| **Legacy** | Elyafgroup Platform CRM, emare-crm Hesap/Kisi/Firsat, Floragenix Lead |
| **BOS hedef** | CrmAccount, CrmContact, CrmOpportunity CQRS + API |
| **GAP** | Task 013 domain tamam; handler/API eksik |

**Kapsam:** CRUD, list, tenant izolasyonu, opportunity stage geçiş kuralları.

**Kabul kriterleri:**
- [ ] `FEATURE_TRACEABILITY_MATRIX` Sales/CEO widget'larının en az %30'u gerçek CRM verisine bağlı
- [ ] Win/Lost stage invariant testleri
- [ ] `CrmAccountCreated` outbox event yayınlanır

**Bağımlılık:** Platform kernel (mevcut)  
**Önerilen faz:** Faz 0–1

---

## EPIC-LEG-003 — Teklif Onay Workflow

| Alan | Değer |
|------|-------|
| **Öncelik** | P0 |
| **Legacy** | emare-crm OnayAkisi, Elyafgroup CrmProposal status |
| **BOS hedef** | `CrmProposalApproval` workflow |
| **GAP** | Entity var; onay motoru yok |

**Kapsam:** Draft→Sent→Approved/Declined, `CRM.Proposal.Approve` permission, numara serisi CR-.

**Kabul kriterleri:**
- [ ] Onaysız Approved geçişi reddedilir
- [ ] Onay sonrası `CrmProposalApproved` event
- [ ] Sales Control Tower "Today's Priorities" onay bekleyen teklifleri listeler

**Bağımlılık:** EPIC-LEG-002  
**Önerilen faz:** Faz 1

---

## EPIC-LEG-004 — SalesOrder Aggregate

| Alan | Değer |
|------|-------|
| **Öncelik** | P0 |
| **Legacy** | Finance Sale, Ticket Order, emare-crm sipariş |
| **BOS hedef** | SalesOrder + SalesOrderItem |
| **GAP** | DOMAIN_MODEL tanımlı; implementasyon yok |

**Kapsam:** Proposal→Order dönüşümü, satır toplamları, `SalesOrderConfirmed` event.

**Kabul kriterleri:**
- [ ] Generic `Order` entity kullanılmaz (ANAYASA)
- [ ] CEO KPI "Sipariş Backlog Değeri" gerçek veriden hesaplanır
- [ ] Win rate KPI opportunity→order zincirine bağlanır

**Bağımlılık:** EPIC-LEG-003  
**Önerilen faz:** Faz 1

---

## EPIC-LEG-005 — Finance Core (Hesap Planı + Yevmiye)

| Alan | Değer |
|------|-------|
| **Öncelik** | P0 |
| **Legacy** | Emare Finance AccountPlan, JournalEntry |
| **BOS hedef** | FinanceAccountPlan, FinanceJournalEntry |
| **GAP** | Tam backend boşluk |

**Kapsam:** Hesap planı CRUD, yevmiye fişi post, borç=alacak invariant.

**Kabul kriterleri:**
- [ ] Dengesiz fiş post edilemez (legacy Finance test port)
- [ ] `FinanceJournalEntryPosted` event
- [ ] Finance Control Tower EBITDA KPI gerçek yevmiyeden türetilir

**Bağımlılık:** EPIC-LEG-002 (cari bağlantı için)  
**Önerilen faz:** Faz 2

---

## EPIC-LEG-006 — Fatura & Ödeme

| Alan | Değer |
|------|-------|
| **Öncelik** | P0 |
| **Legacy** | Emare Finance Invoice, Payment, CariHesap |
| **BOS hedef** | FinanceInvoice, FinancePayment |
| **GAP** | Tam boşluk |

**Kapsam:** Satış/alış faturası, ödeme kaydı, alacak/borç projection.

**Kabul kriterleri:**
- [ ] Fatura→ödeme→yevmiye zinciri (logical FK)
- [ ] CEO "Toplam Alacak/Borç" KPI
- [ ] Critical alert: geciken fatura eşiği

**Bağımlılık:** EPIC-LEG-005  
**Önerilen faz:** Faz 2

---

## EPIC-LEG-007 — Control Tower Veri Katmanı (Mock→DB)

| Alan | Değer |
|------|-------|
| **Öncelik** | P0 |
| **Legacy** | Elyafgroup CT UI seed, FEATURE_TRACEABILITY 100+ satır |
| **BOS hedef** | KPIValue, DecisionLog, CompanyHealthScore projections |
| **GAP** | UI olgun; backend %95 mock |

**Kapsam:** CEO, Sales, Finance kuleleri için traceability'deki Query/Handler implementasyonu; DecisionLog aggregate.

**Kabul kriterleri:**
- [ ] Sprint 2 gate: CEO + Sales + Finance widget'larının traceability satırları "Implemented" işaretli
- [ ] Mock seed yalnızca demo tenant'ta opsiyonel
- [ ] Export/Filter/Date API'leri çalışır

**Bağımlılık:** EPIC-LEG-002, EPIC-LEG-005 (KPI verisi)  
**Önerilen faz:** Faz 6 (paralel erken başlangıç CEO shell)

---

## EPIC-LEG-008 — Raporlama & Import Pipeline

| Alan | Değer |
|------|-------|
| **Öncelik** | P1 |
| **Legacy** | raporlama-app DataImportBatch, Emare Saloon rapor suite |
| **BOS hedef** | Import batch + ERP rapor katalogu |
| **GAP** | Ticket reports var; ERP import yok |

**Kapsam:** Preview/rollback import, 10 rapor tipi spec çıkarımı, Saloon kasa observer pattern referansı.

**Kabul kriterleri:**
- [ ] Import batch rollback testi
- [ ] CEO "Board Reports" en az 3 gerçek rapor linki
- [ ] Hassas veri import log'a yazılmaz

**Bağımlılık:** EPIC-LEG-005  
**Önerilen faz:** Paralel Faz 2–3

---

## EPIC-LEG-009 — HR Personel & İzin

| Alan | Değer |
|------|-------|
| **Öncelik** | P1 |
| **Legacy** | Emare Finance Employee, Leave testleri |
| **BOS hedef** | HrEmployee, HrLeave |
| **GAP** | Stub UI |

**Kapsam:** Personel kartı, izin talebi, onayda bakiye düşürme.

**Kabul kriterleri:**
- [ ] İzin onayı bakiyeyi atomik düşürür
- [ ] CEO headcount KPI
- [ ] HR Control Tower stub kaldırılır

**Bağımlılık:** EPIC-LEG-011 (onay workflow)  
**Önerilen faz:** Faz 3

---

## EPIC-LEG-010 — Stok & Satın Alma

| Alan | Değer |
|------|-------|
| **Öncelik** | P1 |
| **Legacy** | Emare Finance StockMovement, emare-crm SatinalmaTalebi |
| **BOS hedef** | LogisticsWarehouse, StockMovement, PO, GoodsReceipt |
| **GAP** | Spec only |

**Kapsam:** Depo, stok hareketi, satın alma talebi→PO→mal kabul.

**Kabul kriterleri:**
- [ ] FIFO hareket kuralı
- [ ] Min stok alert
- [ ] Satın alma→PO legacy iş kuralı port

**Bağımlılık:** EPIC-LEG-005  
**Önerilen faz:** Faz 3

---

## EPIC-LEG-011 — ERP Workflow Engine

| Alan | Değer |
|------|-------|
| **Öncelik** | P1 |
| **Legacy** | emare-crm Blueprint, OnayAkisi state machine |
| **BOS hedef** | Modül-agnostic approval engine |
| **GAP** | Ticket workflow only |

**Kapsam:** Onay adımları, delegasyon, Blueprint benzeri tanım (config-driven).

**Kabul kriterleri:**
- [ ] CrmProposal, HrLeave, DecisionLog aynı motoru kullanır
- [ ] `Module.Resource.Action` permission entegrasyonu
- [ ] Audit trail her adım

**Bağımlılık:** Platform kernel  
**Önerilen faz:** Faz 1 (Proposal ile birlikte)

---

## EPIC-LEG-012 — Lojistik Sevk & Transfer

| Alan | Değer |
|------|-------|
| **Öncelik** | P2 |
| **Legacy** | Finance Shipment, DOMAIN_MODEL transfer kuralı |
| **BOS hedef** | LogisticsShipment, LogisticsStockTransfer |
| **GAP** | Kod yok |

**Kapsam:** Sevk irsaliyesi, depolar arası transfer, yetersiz stok engeli.

**Kabul kriterleri:**
- [ ] Transfer onay workflow
- [ ] SalesOrder→Shipment bağlantısı
- [ ] Logistics Control Tower gerçek veri

**Bağımlılık:** EPIC-LEG-010, EPIC-LEG-004  
**Önerilen faz:** Faz 3–4

---

## EPIC-LEG-013 — Üretim BOM, MRP & Maliyet

| Alan | Değer |
|------|-------|
| **Öncelik** | P1 |
| **Legacy** | Emare Finance BOM, MRP, Bom::unitCost |
| **BOS hedef** | Bom, BomOperation, Workstation, MrpRule |
| **GAP** | Legacy test coverage yüksek; BOS sıfır |

**Kapsam:** BOM CRUD, fire oranı, MRP→PO önerisi, birim maliyet.

**Kabul kriterleri:**
- [ ] Legacy Finance unit testlerinden port edilen invariant seti
- [ ] Production Control Tower KPI mock kaldırılır
- [ ] Costing raporu

**Bağımlılık:** EPIC-LEG-010  
**Önerilen faz:** Faz 4

---

## EPIC-LEG-014 — Üretim Emri (WorkOrder)

| Alan | Değer |
|------|-------|
| **Öncelik** | P2 |
| **Legacy** | Finance MrpSuggestion→PO; saha IsEmri (farklı domain) |
| **BOS hedef** | ProductionWorkOrder |
| **GAP** | Traceability hedef; entity yok |

**Kapsam:** MRP çıktısından iş emri, tamamlanma, verimlilik KPI.

**Kabul kriterleri:**
- [ ] `ProductionWorkOrderCompleted` event
- [ ] CEO üretim verimliliği KPI
- [ ] Saha servis IsEmri ile karıştırılmaz

**Bağımlılık:** EPIC-LEG-013  
**Önerilen faz:** Faz 4

---

## EPIC-LEG-015 — Merkezi i18n Yönetimi

| Alan | Değer |
|------|-------|
| **Öncelik** | P1 |
| **Legacy** | translation-manager, emare-i18n |
| **BOS hedef** | Key export/import + runtime paket |
| **GAP** | CT'de hardcoded key riski |

**Kapsam:** tr-TR, en-US, de-DE, ar-SA; RTL; çeviri key export pipeline.

**Kabul kriterleri:**
- [ ] Control Tower widget'larında sıfır hardcoded string
- [ ] API hata mesajları i18n key
- [ ] LOCALIZATION_I18N_STANDARDS uyumu

**Bağımlılık:** EPIC-LEG-007 (CT genişlemesi ile paralel)  
**Önerilen faz:** Paralel

---

## EPIC-LEG-016 — Tekstil Domain Extension

| Alan | Değer |
|------|-------|
| **Öncelik** | P2 |
| **Legacy** | ElyafSample, ElyafCollection, ElyafStyle (hafif) |
| **BOS hedef** | Fabric, Yarn, Sample workflow, Capacity |
| **GAP** | Yarn/dyeing/weaving yok |

**Kapsam:** SME workshop çıktısıyla DOMAIN_MODEL genişletme; Fabric/Merchandising/Design CT veri katmanı.

**Kabul kriterleri:**
- [ ] UBIQUITOUS_LANGUAGE güncel
- [ ] En az 3 tekstil-spesifik entity production'da
- [ ] Fabric Dashboard mock kaldırılır

**Bağımlılık:** EPIC-LEG-013, EPIC-LEG-007  
**Önerilen faz:** Faz 5

---

## EPIC-LEG-017 — Kalite Kontrol Modülü

| Alan | Değer |
|------|-------|
| **Öncelik** | P2 |
| **Legacy** | emare-crm VeriKalite, QC failed≤tested kuralı |
| **BOS hedef** | QcStandard, QcTestResult, QcClaim |
| **GAP** | Spec + UI stub |

**Kapsam:** AQL test, claim lifecycle, red oranı KPI.

**Kabul kriterleri:**
- [ ] failed≤tested invariant
- [ ] CEO kalite red oranı KPI
- [ ] QC Control Tower gerçek veri

**Bağımlılık:** EPIC-LEG-010  
**Önerilen faz:** Faz 5

---

## EPIC-LEG-018 — Service Desk ↔ ERP Köprüsü

| Alan | Değer |
|------|-------|
| **Öncelik** | P2 |
| **Legacy** | Elyafgroup SupportTicket + Customer |
| **BOS hedef** | CrmAccount ↔ Ticket ilişkisi |
| **GAP** | İki müşteri modeli |

**Kapsam:** Customer→CrmAccount migration stratejisi, ticket'ta cari görünümü.

**Kabul kriterleri:**
- [ ] Tek canonical müşteri kaydı tenant başına
- [ ] Ticket oluştururken CrmAccount seçimi
- [ ] Breaking change dokümante

**Bağımlılık:** EPIC-LEG-002  
**Önerilen faz:** Faz 1–2

---

## EPIC-LEG-019 — Omnichannel Workflow & CC Tahsilat

| Alan | Değer |
|------|-------|
| **Öncelik** | P2 |
| **Legacy** | emareasistan ResponseRule, emarecc tahsilat |
| **BOS hedef** | AI action + CC collections modülü |
| **GAP** | Kısmi |

**Kapsam:** Kanal workflow birleşimi; opsiyonel tahsilat CC (Finance Payment ile).

**Kabul kriterleri:**
- [ ] ResponseRule benzeri config
- [ ] Tahsilat disposition→FinancePayment (opsiyonel modül)
- [ ] PII loglanmaz

**Bağımlılık:** EPIC-LEG-006, EPIC-LEG-011  
**Önerilen faz:** v2

---

## EPIC-LEG-020 — Bayi & Kampanya (v2)

| Alan | Değer |
|------|-------|
| **Öncelik** | P3 |
| **Legacy** | Floragenix dealer, emare-crm Kampanya |
| **BOS hedef** | Reseller portal genişletme |
| **GAP** | Stub |

**Bağımlılık:** EPIC-LEG-004  
**Önerilen faz:** v2+

---

## EPIC-LEG-021 — e-Belge & Marketplace (v2)

| Alan | Değer |
|------|-------|
| **Öncelik** | P2–P3 |
| **Legacy** | Finance EInvoice, Emare Pazar, ecomaiq |
| **BOS hedef** | Entegrasyon adapter registry |
| **GAP** | Tam boşluk |

**Kapsam:** e-Fatura adapter; marketplace sync SLA (Emare Pazar pattern).

**Bağımlılık:** EPIC-LEG-006  
**Önerilen faz:** v2

---

## Önerilen Uygulama Sırası (İlk 8 Sprint)

```text
Sprint N   → EPIC-LEG-002 (CRM API)
Sprint N+1 → EPIC-LEG-003 + EPIC-LEG-011 (Proposal + workflow)
Sprint N+2 → EPIC-LEG-004 (SalesOrder)
Sprint N+3 → EPIC-LEG-005 (Finance journal)
Sprint N+4 → EPIC-LEG-006 + EPIC-LEG-007 partial (Invoice + CEO KPI)
Sprint N+5 → EPIC-LEG-010 (Inventory)
Sprint N+6 → EPIC-LEG-013 (BOM/MRP)
Sprint N+7 → EPIC-LEG-007 complete (CT data layer)
```

---

## Epic → Task Ayrıştırma Notu

Agent 6 epic tanımlar; **Agent 1** her epic'i `TASK_0XX` implementation task'larına böler. Her task:
- Tek bounded context veya aggregate odaklı olmalı
- `FEATURE_TRACEABILITY_MATRIX` satır referansı içermeli
- Legacy iş kuralı ID'si (`LEGACY_BUSINESS_RULES.md` bölümü) cite edilmeli

---

## İlgili Dosyalar

| Dosya | Rol |
|-------|-----|
| `ARCHITECTURE_GAP_MATRIX.md` | Gap → EPIC eşlemesi |
| `LEGACY_BUSINESS_RULES.md` | İş kuralı kanıtı |
| `LEGACY_REUSABILITY_REPORT.md` | Kaynak proje önceliği |
| `FEATURE_TRACEABILITY_MATRIX.md` | Uygulama doğrulama listesi |
