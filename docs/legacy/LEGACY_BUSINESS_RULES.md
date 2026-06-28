# Legacy Business Rules — TASK 021

**Tarih:** 2026-06-28  
**Amaç:** Eski projelerden çıkarılan iş kuralları; Emare BOS migrasyonu için referans

---

## 1. CRM & Satış

### Teklif (Proposal) Yaşam Döngüsü

| Kural | Kaynak | BOS hedef |
|-------|--------|-----------|
| Teklif durumları: Draft → Sent → Approved/Declined | Elyafgroup `CrmProposal`, emare-crm `Teklif`, Floragenix `Proposal` | `CrmProposalApproval` workflow |
| Onay yetkisi ayrı permission (`CRM.Proposal.Approve`) | FEATURE_TRACEABILITY_MATRIX | SECURITY_AUTHORIZATION |
| Teklif numarası otomatik: CR- prefix | Elyafgroup `NumberSequenceService` | `NumberSequence` entity |
| Teklif satır toplamı = header total | Elyafgroup `CrmProposalItem` | Aggregate invariant |
| Win/Lost fırsat stage geçişi | `CrmOpportunity` stage string | Pipeline kuralları |

### Satış Hunisi

| Kural | Kaynak |
|-------|--------|
| Lead → Opportunity → Proposal → Order | emare-crm Blueprint, Floragenix automation |
| Bayi hiyerarşisi: parent Lead, alt dealer kullanıcıları | Floragenix `Lead.parentId`, `User.dealerLeadId` |
| Kampanya indirim kuralları | emare-crm `Kampanya`, Finance `Campaign` |
| Fiyat listesi / birim (Adet, Koli, litre) | Floragenix `ProposalItem`, Finance `Product` |

### Müşteri (Account)

| Kural | Kaynak |
|-------|--------|
| Cari hesap soft delete + tenant izolasyonu | Elyafgroup `ITenantEntity`, Finance `BelongsToTenant` |
| Müşteri not/aktivite/dosya ilişkisi | Elyafgroup `CustomerNote/Activity/File` |
| Kredi limiti kontrolü (veresiye) | emarepos `credit_limit` migration |
| Sektör bazlı AI bilgi tabanı | Elyafgroup `Sector`, `SectorKnowledgeEntry` |

---

## 2. Finans & Muhasebe

### Yevmiye / Muhasebe

| Kural | Kaynak | BOS kuralı |
|-------|--------|------------|
| Borç toplamı = Alacak toplamı olmadan fiş post edilemez | DOMAIN_MODEL.md + Finance `JournalEntry` | **Taşınmalı — P0** |
| Hesap planı tek düzen (120, 320 vb.) | emare-crm `HesapPlani`, Finance `AccountPlan` | `FinanceAccountPlan` |
| Cari hesap hareketleri fatura/ödeme ile bağlantılı | `CariHesap`, `FinancePayment` | Cross-module FK (logical) |
| Mizan, bilanço, gelir tablosu türetilmiş raporlar | Finance `AccountingController` | Reporting module |
| E-fatura / e-SMM entegrasyonu | Finance `EInvoice`, `ESmmDocument` | Entegrasyon katmanı |

### Ödeme & Tahsilat

| Kural | Kaynak |
|-------|--------|
| Karma ödeme dağılımı doğrulama (nakit+kart+veresiye=toplam) | emarepos `SaleService::odemeDagiliminiDogrula` |
| Veresiye için müşteri zorunlu | emarepos |
| Tahsilat script placeholder: borç tutarı, dosya no | emarecc `scripts/seed.js` |
| Disposition: payment_promise, refused, unreachable | emarecc `init.sql` |
| Ödeme sözü takibi | emarecc `customers` şeması |

### Bütçe & Nakit

| Kural | Kaynak |
|-------|--------|
| Bütçe vs gerçekleşen karşılaştırma | CONTROL_TOWER CEO KPI |
| Nakit açığı eşik uyarısı | CONTROL_TOWER Critical Alerts |
| Döviz kuru güncelleme | Finance `CurrencyRate`, emare-crm `DovizKuru` |

---

## 3. Stok & Lojistik

| Kural | Kaynak | BOS kuralı |
|-------|--------|------------|
| Yetersiz stokta transfer tamamlanamaz | DOMAIN_MODEL.md | `LogisticsStockTransfer` |
| FIFO stok hareketi | DOMAIN_MODEL hedef | Finance `StockMovement` |
| Min stok seviyesi uyarısı | Floragenix cron, Finance `MrpRule` | Stok alert |
| Lot/seri/batch takibi | Finance `ProductBatch`, `ProductSerial` | Textile traceability adayı |
| Depolar arası transfer onayı | DOMAIN_MODEL `StockTransferApproved` | Workflow |
| Mal kabul → stok girişi | emare-crm `MalKabul`, Finance `GoodsReceipt` | Purchasing flow |

---

## 4. Satın Alma

| Kural | Kaynak |
|-------|--------|
| Satın alma talebi → onay → PO | emare-crm `SatinalmaTalebi`, Finance `PurchaseOrder` |
| Tedarikçi teklif karşılaştırma | Finance `ProcurementReportController`, `SupplierProposal` |
| MRP önerisi → PO draft otomatik | Finance `MrpCoreFlowTest` |
| min/max stock, lead time, reorder point | Finance `MrpRule` |

---

## 5. Üretim & Planlama

| Kural | Kaynak |
|-------|--------|
| BOM maliyet = malzeme + fire oranı | Finance `Bom::unitCost()` |
| BOM operasyon → iş istasyonu routing | `BomOperation`, `Workstation` |
| MRP: stok seviyesi + talep → öneri | `MrpSuggestion`, `MrpRule` |
| Kapasite / OEE KPI (mock) | Elyafgroup Production dashboard seed |
| OTD (on-time delivery) style risk | `ElyafStyle` risk alanları |
| Numune lead time | `ElyafSample.LeadTimeDays` |

**Not:** Knitting, weaving, dyeing, yarn spesifik kurallar **kod tabanında yok** — yalnızca Control Tower KPI isimleri ve yol haritası dokümanları.

---

## 6. Kalite Kontrol

| Kural | Kaynak | BOS |
|-------|--------|-----|
| FailedQuantity ≤ TestedQuantity | DOMAIN_MODEL.md | `QcTestResult` |
| Kalite şikayeti → CAPA | DOMAIN_MODEL `QcClaim` | QC module |
| Veri kalite skoru / kural motoru | emare-crm `VeriKaliteKurali`, `VeriKaliteSkoru` | Metadata driven QC adayı |
| QC red oranı KPI | CONTROL_TOWER CEO | Reporting |

---

## 7. İnsan Kaynakları

| Kural | Kaynak | BOS |
|-------|--------|-----|
| İzin onaylandığında bakiye düşürülür | DOMAIN_MODEL.md | `HrLeaveApproved` |
| İzin onay akışı (multi-step) | Finance `LeaveApprovalFlowTest` | Workflow engine |
| Personel sayısı KPI | CONTROL_TOWER | HR module |
| Puantaj / timesheet | Finance `Timesheet` | HR extension |

---

## 8. Service Desk & Ticket

| Kural | Kaynak |
|-------|--------|
| Ticket stage değişince otomatik e-posta | Elyafgroup `WorkflowEngine.EvaluateStageChangeAsync` |
| Yapılandırılabilir ticket süreci (process + stages) | `TicketProcess`, `TicketProcessStage` |
| Özel alan kuralları (field rules) | `TicketFieldDefinition`, `TicketFieldRule` |
| AI routing skoru | Elyafgroup AI layer |
| SLA / öncelik alanları | SupportTicket entity |

---

## 9. Çağrı Merkezi & Tahsilat

| Kural | Kaynak |
|-------|--------|
| Preview dialer kampanya lead akışı | emarecc `dialer.ts` |
| Screen-pop: müşteri borç bilgisi agent'a | emarecc customers + calls |
| Agent transfer log | emarecc migration 019 |
| Rol: admin > supervisor > agent | emarecc RBAC |
| Wallboard public token erişimi | emarecc README |

---

## 10. Workflow & Onay Süreçleri

### emare-crm Blueprint (State Machine)

- `Blueprint` → `BlueprintState` → `BlueprintTransition`
- Transition approval gerektirebilir
- Modül bazlı otomasyon: tetikleyici + koşul + aksiyon JSON (`OtomasyonKurali`)

### Onay Akışı (OnayAkisi)

- Modül + tutar eşiği ile uygun akış seçimi: `OnayAkisi::uygunAkisBul`
- `OnayTalebi` kayıt durumu

### BOS Hedef Workflow'lar (henüz implement edilmemiş)

| Workflow | Durum Elyafgroup | Legacy referans |
|----------|------------------|-----------------|
| `CrmProposalApproval` | Stub | emare-crm OnayAkisi, Floragenix approvals |
| `DecisionLogApproval` | Stub | — |
| `HrLeaveApproval` | Stub | Finance LeaveApprovalFlowTest |
| `FinanceJournalEntryPost` | Stub | Finance JournalEntry posting |
| `LogisticsStockTransferApproval` | Stub | DOMAIN_MODEL |

---

## 11. Yetkilendirme Kuralları

| Kural | Kaynak |
|-------|--------|
| `Module.Resource.Action` permission pattern | Elyafgroup Platform `Permissions.cs` |
| Super admin bypass | Finance `CheckPermission.php` |
| Modül toggle (tenant plan) | Finance `CheckModule`, emarepos `Module` |
| Elyaf Control Tower rol→kule haritası | `ElyafDashboardAuthorization.cs` |
| CEO tüm pilot kulelere read-only | Elyafgroup authorization |
| Tenant slug guard (`elyaf-group`) | `ElyafControllerBase.cs` |
| 15 Laravel Policy (Hesap, Firsat, Teklif…) | emare-crm |
| Floragenix route guard: DEALER kısıtları | `middleware.js` |

---

## 12. Raporlama Kuralları

| Rapor tipi | Kaynak |
|------------|--------|
| Dashboard özet (müşteri/görev/çağrı) | Elyafgroup `ReportsController` |
| Executive report (console) | emare-crm `GenerateExecutiveReport` |
| Günlük satış, kâr, personel | Finance `ReportController` |
| Tedarikçi skor, fiyat karşılaştırma | Finance `ProcurementReportController` |
| CSV/XLSX/PDF export | Floragenix, Finance, Control Tower scope |
| CDR / müşteri CC raporu | emarecc |
| P&L, Cash Flow, Board Report | CONTROL_TOWER CEO scope |

---

## 13. Multi-Tenant & SaaS

| Kural | Kaynak |
|-------|--------|
| TenantId zorunlu tüm entity'lerde | DOMAIN_MODEL, Elyafgroup global filter |
| Plan → modül feature gating | Elyafgroup `TenantFeature`, emarepos `Plan/Module` |
| Reseller tenant provisioning | Elyafgroup `ResellerTenantsController`, reseller-portal |
| Branch (şube) izolasyonu | Finance `Branch`, emarepos |
| White-label: marka adı env'den | ANAYASA Article 4 |

---

## 14. Localization Kuralları

| Kural | Kaynak |
|-------|--------|
| UI string hardcode yasak (Control Tower) | LOCALIZATION_I18N_STANDARDS |
| Desteklenen diller: tr-TR, en-US, de-DE, ar-SA | i18n standart |
| RTL: ar-SA layout kuralları | i18n standart |
| Backend API mesajları i18n key | BOS hedef |
| `@money`, `@tarih` Blade directive | Finance README |

---

## Dashboard İş Kuralları (Control Tower)

| Kural | Kaynak |
|-------|--------|
| Her kule minimum 4 KPI kartı, trend ok | CONTROL_TOWER_FINAL_SCOPE |
| Today's Priorities: onay bekleyen belgeler listesi | FEATURE_TRACEABILITY |
| Critical Alerts: eşik aşımında kırmızı alarm | CONTROL_TOWER |
| Health Score 1-100 veya A-F | CONTROL_TOWER |
| Export: CSV/Excel + tarih filtresi zorunlu | CONTROL_TOWER |
| Mock vs DB fallback: `USE_MOCK` env flag | Elyafgroup `elyafKpiApi.ts` |

---

# TASK 021-B — Yeni İş Kuralları

## Emare Saloon

| Kural | Kaynak |
|-------|--------|
| Satış → ödeme → kasa observer zinciri | `app/Observers/SaleObserver.php` |
| Stok transfer onay akışı | `docs/01-urun-kapsami.md` |
| Tenant/branch modül gating | `Module`, `TenantModule` |
| Kasa oturumu aç/kapa | Cash register session |

## Emare Pazar

| Kural | Kaynak |
|-------|--------|
| Adapter tabanlı ürün/sipariş normalizasyon | `app/integrations/base.py` |
| Periyodik sync: sipariş 15dk, stok 5dk | `app/tasks/sync_tasks.py`, README |
| Marketplace credential izolasyonu | `MarketplaceCredential` |
| Retry on sync failure | Celery tasks |

## raporlama-app

| Kural | Kaynak |
|-------|--------|
| Import batch: preview → commit → rollback | `DataImportService.php` |
| Tenant + permission (`reports.view`, `reports.export`) | `routes/web.php` |
| 10+ rapor tipi: günlük, korelasyon, stok lot, personel | `ReportController.php` |

## emareciftlik

| Kural | Kaynak |
|-------|--------|
| Hayvan → süt kaydı → envanter tüketimi | `PROJE.md`, modeller |
| Contact/tedarikçi cari hareket | `ContactTransaction` |
| Personel + saha/ekipman takibi | Staff, Equipment |

## emareaplincedesk

| Kural | Kaynak |
|-------|--------|
| Servis talebi → teknisyen atama → parça kullanımı → fatura | `routes/web.php` |
| Yedek parça stok düşümü | `SparePartUsage` |

## emareasistan

| Kural | Kaynak |
|-------|--------|
| ResponseRule öncelik eşleşmesi (kanal + intent) | `services/workflow/rules.py` |
| Sipariş state machine | `services/core/state_machine.py` |
| Tenant workflow pipeline | `TenantWorkflow` |
| RAG embedding ile ürün/soru eşleşmesi | `Embedding` model |

## emareflow (arşiv)

| Kural | Kaynak |
|-------|--------|
| Workflow node: AI, HTTP, Finance, WhatsApp | `frontend/src/components/nodes/` |
| n8n benzeri görsel akış | React Flow |

## translation-manager

| Kural | Kaynak |
|-------|--------|
| Proje içi unique namespace + key | `TranslationDomainTest.php` |
| Export: PHP/JSON/ARB format dönüşümü | `TranslationExporter.php` |

## ecomaiq

| Kural | Kaynak |
|-------|--------|
| Mağaza bazlı yetki (multi-store) | README, server.ts |
| AI cevap puanlama + auto-reply worker | scripts/feature-monitor |
| Deploy sonrası health cron | README |

---

## İlk Taşınması Gereken 20 İş Kuralı (TASK 021-B güncel)

| # | İş Kuralı | Legacy Kaynak | BOS Hedef | Öncelik |
|---|-----------|---------------|-----------|---------|
| 1 | Yevmiye: borç = alacak olmadan post edilemez | Emare Finance | `FinanceJournalEntryPosted` | P0 |
| 2 | Teklif onay workflow | emare-crm, Elyafgroup | `CrmProposalApproval` | P0 |
| 3 | Tenant izolasyonu | Elyafgroup, Finance, Saloon | Kernel | P0 |
| 4 | CRM Account→Contact→Opportunity→Proposal | emare-crm, Elyafgroup | CRM | P0 |
| 5 | Stok yetersizse transfer tamamlanamaz | DOMAIN_MODEL | Logistics | P0 |
| 6 | Satış→ödeme→kasa observer zinciri | **Emare Saloon** | Finance/POS | P0 |
| 7 | Import batch preview/rollback | **raporlama-app** | Reporting | P1 |
| 8 | Marketplace adapter normalizasyon + sync SLA | **Emare Pazar** | Integration | P1 |
| 9 | BOM birim maliyet + fire oranı | Emare Finance | Costing | P1 |
| 10 | MRP min/max + lead time → PO önerisi | Emare Finance | Planning | P1 |
| 11 | İzin onayında bakiye düşürme | DOMAIN_MODEL | HR | P1 |
| 12 | QC failed≤tested | DOMAIN_MODEL | QC | P1 |
| 13 | Satın alma talebi→onay→PO | emare-crm, Finance | Purchasing | P1 |
| 14 | RBAC Module.Resource.Action | Platform Permissions | Security | P1 |
| 15 | Servis talebi→parça→fatura | **emareaplincedesk** | Service/Inventory | P2 |
| 16 | ResponseRule öncelik + workflow pipeline | **emareasistan** | AI/Workflow | P2 |
| 17 | Çeviri key unique + multi-format export | **translation-manager** | i18n | P2 |
| 18 | Ticket stage→workflow e-posta | Elyafgroup WorkflowEngine | Service desk | P2 |
| 19 | Otomasyon trigger+condition+action | emare-crm OtomasyonKurali | Workflow engine | P2 |
| 20 | DateTime UTC (PostgreSQL) | ANAYASA | Persistence | P0 |
