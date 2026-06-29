# Legacy Reusability Report — TASK 021

**Tarih:** 2026-06-28 (TASK 021-B genişletme)  
**Amaç:** Legacy projelerden Emare BOS'a taşınabilirlik değerlendirmesi

---

## Değerlendirme Ölçeği

| Puan | Anlam |
|------|-------|
| ★★★★★ | Doğrudan taşınabilir / birincil kaynak |
| ★★★★☆ | Yüksek değer; adaptasyon gerekir |
| ★★★☆☆ | Orta; pattern referansı |
| ★★☆☆☆ | Düşük; yalnızca fikir |
| ★☆☆☆☆ | Taşınmamalı / obsolete |

---

## Proje Bazlı Reusability

| Proje | Genel Puan | Güçlü Alan | Zayıf Alan |
|-------|------------|------------|------------|
| **Elyafgroup** | ★★★★☆ | Platform iskelet, tenant, RBAC, omnichannel, AI, i18n | ERP backend (finans/üretim) stub |
| **Emare Finance standalone** | ★★★★★ | Finans, BOM, MRP, stok, satın alma, HR | Stack farkı (Laravel→.NET) |
| **emare-crm** | ★★★★☆ | CRM, workflow, onay, sektör modelleri | Üretim yok; Finance kısmi |
| **emarecc** | ★★★☆☆ | CC, tahsilat, CDR, dialer | ERP domain dışı |
| **Floragenix CRM** | ★★★☆☆ | Satış hunisi, bayi, automation | SQLite, tek tenant |
| **emarepos** | ★★★☆☆ | POS, stok, tenant SaaS | Restoran odaklı |
| **Emare Saloon** | ★★★★★ | Perakende/hizmet ERP, kasa observer | Laravel stack |
| **raporlama-app** | ★★★★★ | Rapor suite + import batch | Saloon domain |
| **Emare Pazar** | ★★★★☆ | 14 marketplace adapter | Python stack |
| **emareciftlik** | ★★★★☆ | Vertical ERP pattern | Tarım, tekstil değil |
| **translation-manager** | ★★★★☆ | Merkezi i18n model | Filament admin |
| **emareasistan** | ★★★☆☆ | Omnichannel + workflow | Python/FastAPI |
| **yeni-versiyon-gecis** | ★★★★★ | ADR + traceability blueprint | Doküman only |
| **Emare Ticket snapshot** | ★★☆☆☆ | — | Elyafgroup tercih edilmeli |
| **emarerp/Emare Finance gömülü** | ★★☆☆☆ | — | Obsolete kopya |

---

## Modül Bazlı Reusability

| Modül | Birincil Kaynak | Puan | Taşıma Stratejisi |
|-------|-----------------|------|-------------------|
| **CRM** | Elyafgroup Platform + emare-crm | ★★★★☆ | Entity'ler BOS'ta tanımlı; handler'lar Elyafgroup'ta başlamış |
| **Sales** | emare-crm + Floragenix | ★★★★☆ | Proposal→Order akışı Laravel'den domain spec çıkar |
| **Finance** | Emare Finance standalone | ★★★★★ | JournalEntry, AccountPlan, Invoice — birincil kaynak |
| **HR** | Emare Finance | ★★★★☆ | Employee, Leave, approval flow testleri |
| **Production** | Emare Finance BOM/MRP | ★★★★★ | Doğrudan domain analizi; .NET'e port |
| **Planning** | Emare Finance MRP | ★★★★☆ | MrpRule, MrpSuggestion |
| **Inventory** | Emare Finance + emare-crm | ★★★★☆ | StockMovement, Depo, batch/serial |
| **Purchasing** | Emare Finance + emare-crm | ★★★★☆ | PO, GoodsReceipt, SatinalmaTalebi |
| **Logistics** | Emare Finance + DOMAIN_MODEL | ★★★☆☆ | Shipment var; transfer workflow BOS'ta tanımlı |
| **QC** | emare-crm VeriKalite + BOS spec | ★★★☆☆ | QC entity BOS'ta; legacy kısmi |
| **Maintenance** | — | ★☆☆☆☆ | Yok |
| **Costing** | Emare Finance Bom::unitCost | ★★★★☆ | Fire oranı kuralı kanıtlanmış |
| **Reporting** | **raporlama-app** + Finance + Saloon | ★★★★★ | Import batch + 10 rapor tipi |
| **Marketplace / E-ticaret** | **Emare Pazar** + Finance + ecomaiq | ★★★★☆ | 14 adapter + Trendyol Q&A |
| **Ticket/Service Desk** | Elyafgroup EmareTicket | ★★★★★ | Zaten BOS platformunda olgun |
| **Call Center** | Elyafgroup + emarecc | ★★★★☆ | Ticket'ta geniş; emarecc tahsilat odaklı |
| **Textile Control Tower** | Elyafgroup UI + seed | ★★★☆☆ | UI shell taşınır; veri katmanı sıfırdan |
| **Multi-tenant SaaS** | Elyafgroup Platform + Saloon | ★★★★★ | Outbox, event bus, tenant kernel |
| **Workflow Engine** | emare-crm + **emareasistan** + emareflow | ★★★★☆ | Blueprint + ResponseRule pipeline |
| **i18n** | emare-i18n + **translation-manager** | ★★★★★ | Merkezi key/export + runtime paket |
| **AI Layer** | Elyafgroup EmareTicket.AI | ★★★★★ | Governance, agent, telemetry olgun |

---

## Textile-Specific Reusability

| Kavram | Puan | Kaynak | Not |
|--------|------|--------|-----|
| Fabric procurement KPI | ★★☆☆☆ | Elyafgroup FabricDashboard | UI mock only |
| Sample management | ★★★☆☆ | `ElyafSample` | Entity var, workflow hafif |
| Merchandising / Collection | ★★★☆☆ | `ElyafCollection`, `ElyafStyle` | KPI + risk alanları |
| BOM | ★★★★★ | Emare Finance | Test coverage var |
| MRP | ★★★★★ | Emare Finance | Test coverage var |
| Routing / Workstation | ★★★★☆ | `BomOperation`, `Workstation` | Genel üretim |
| Yarn / Dyeing / Knitting / Weaving | ★☆☆☆☆ | — | Sıfırdan domain tasarımı gerekir |
| Capacity planning | ★★☆☆☆ | KPI mock | İş kuralı yok |

---

## Teknik Taşıma Riskleri

| Risk | Etki | Azaltma |
|------|------|---------|
| İki stack (.NET vs Laravel) | Yüksek | Domain spec + test port; kod copy-paste değil |
| Duplicate CRM (Ticket vs Platform) | Orta | Birleşim stratejisi: Platform canonical |
| Mock Control Tower verisi | Yüksek | KPI→DB projection sprint'i |
| emare-crm Finance modülü yarım (4 dosya) | Orta | Standalone Finance birincil kaynak |
| Textile domain boşluğu | Yüksek | Elyaf SME workshop + DOMAIN_MODEL genişletme |
| UTC DateTime ihlalleri legacy'de | Orta | ANAYASA kuralı migration'da enforce |

---

## Önerilen Taşıma Sırası (Fazlar)

### Faz 0 — Platform (mevcut)
- Tenant, RBAC, audit, i18n, event outbox
- Kaynak: Elyafgroup Platform

### Faz 1 — CRM + Sales (Sprint 2 devam)
- CrmAccount/Contact/Opportunity/Proposal CRUD + approval
- Kaynak: Elyafgroup + emare-crm OnayAkisi spec

### Faz 2 — Finance Core
- AccountPlan, JournalEntry, Invoice, Payment
- Kaynak: **Emare Finance standalone** (birincil)

### Faz 3 — Inventory + Purchasing
- StockMovement, PurchaseOrder, GoodsReceipt
- Kaynak: Emare Finance + emare-crm

### Faz 4 — Production + MRP
- Bom, BomOperation, Workstation, MrpRule
- Kaynak: **Emare Finance standalone**

### Faz 5 — Textile Extension
- Fabric, Yarn, Sample workflow, Capacity
- Kaynak: Elyafgroup UI spec + yeni domain design

### Faz 6 — Control Tower Data Layer
- Mock→DB KPI projection
- Kaynak: CONTROL_TOWER_FINAL_SCOPE + FEATURE_TRACEABILITY

---

## Modül Karşılaştırma Tablosu

| Modül | Eski Projede Var | Yeni BOS'ta Var | Taşınmalı mı | Öncelik |
| ----- | ---------------- | --------------- | ------------ | ------- |
| CRM (Account/Contact) | Evet — Elyafgroup, emare-crm, Floragenix | Kısmen — Platform CrmAccount/Contact CRUD | Evet | P0 |
| CRM (Opportunity) | Evet — Elyafgroup, emare-crm | Kısmen — entity + list | Evet | P0 |
| CRM (Proposal + onay) | Evet — üç projede | Kısmen — entity var, approval workflow yok | Evet | P0 |
| Sales Order | Evet — Finance Sale, Ticket Order | Hayır — SalesOrder entity tanımlı, kod yok | Evet | P0 |
| Finance (Hesap Planı) | Evet — Emare Finance, emare-crm | Hayır — stub UI | Evet | P0 |
| Finance (Yevmiye) | Evet — Emare Finance | Hayır | Evet | P0 |
| Finance (Fatura/Ödeme) | Evet — Emare Finance | Hayır | Evet | P0 |
| HR (Personel) | Evet — Emare Finance, emare-crm | Hayır — stub UI | Evet | P1 |
| HR (İzin onay) | Evet — Finance test | Hayır — permission only | Evet | P1 |
| Production (BOM) | Evet — Emare Finance | Hayır | Evet | P1 |
| Production (MRP) | Evet — Emare Finance | Hayır | Evet | P1 |
| Production (WorkOrder) | Kısmi — Finance migration | Hayır — traceability hedef | Evet | P2 |
| Planning / Capacity | Kısmi — MRP + KPI mock | Hayır | Evet | P2 |
| Inventory / Stok | Evet — Finance, emare-crm, emarepos | Hayır — DOMAIN_MODEL tanımlı | Evet | P1 |
| Purchasing | Evet — Finance, emare-crm | Hayır | Evet | P1 |
| Logistics / Sevk | Kısmi — Finance Shipment | Hayır — DOMAIN_MODEL tanımlı | Evet | P2 |
| QC | Kısmi — emare-crm veri kalite, UI mock | Hayır — entity spec var | Evet | P2 |
| Maintenance | Hayır | Hayır | Hayır (v2+) | P3 |
| Costing | Evet — Finance Bom::unitCost | Hayır | Evet | P1 |
| Reporting | Evet — tüm major projeler | Kısmen — Ticket reports olgun | Evet | P1 |
| Service Desk / Ticket | Evet — Elyafgroup olgun | Evet — production modül | Hayır (zaten var) | — |
| Call Center | Evet — Elyafgroup + emarecc | Kısmen — Ticket'ta geniş | Kısmen (tahsilat CC) | P2 |
| Control Tower UI | Evet — 16 rol dashboard | Evet — mock/seed | Evet (veri katmanı) | P0 |
| Multi-tenant SaaS | Evet — Elyafgroup Platform | Evet — kernel | Hayır (devam) | — |
| Workflow Engine (ERP) | Evet — emare-crm Blueprint | Kısmi — ticket workflow only | Evet | P1 |
| i18n | Evet — Elyafgroup emare-i18n | Kısmen — paket var, CT kısmi | Evet (tamamlama) | P1 |
| Textile (Fabric/Yarn/Dyeing) | Hayır (UI isimleri only) | Hayır | Evet (yeni domain) | P2 |
| Sample / Merchandising | Kısmi — ElyafSample, Collection | Kısmi — entity var | Evet | P2 |
| Reseller Portal | Evet — Elyafgroup | Kısmen | Kısmen | P3 |
| POS / Restoran | Evet — emarepos | Hayır | Hayır (ayrı ürün) | P3 |
| Marketplace entegrasyon | Evet — **Emare Pazar**, Finance, ecomaiq | Hayır | Evet | P1 |
| Perakende/hizmet ERP | Evet — **Emare Saloon**, raporlama-app | Hayır | Evet | P0 |
| Rapor import pipeline | Evet — **raporlama-app** | Hayır | Evet | P1 |
| i18n merkezi yönetim | Evet — **translation-manager** | Kısmen — emare-i18n | Evet | P1 |
| Omnichannel asistan | Evet — **emareasistan** | Kısmen — Ticket AI | Kısmen | P2 |
| Vertical ERP (tarım) | Evet — emareciftlik (arşiv) | Hayır | Hayır (ayrı vertical) | P3 |
| Servis masası | Evet — emareaplincedesk | Hayır | Kısmen | P2 |
| Mimari blueprint | Evet — yeni-versiyon-gecis | Kısmen | Devam | P0 |

**Özet:** 37 modülden 26'si taşınmalı; 4'ü zaten BOS'ta; 4'ü ayrı ürün/vertical; 3'ü v2+.

---

## İlk Taşınması Gereken 20 İş Kuralı (TASK 021-B)

Detaylı tablo: `LEGACY_BUSINESS_RULES.md`

1. Yevmiye borç=alacak — Emare Finance
2. Teklif onay workflow — emare-crm
3. Tenant izolasyonu — Elyafgroup/Saloon
4. CRM Account→Proposal zinciri
5. Yetersiz stokta transfer engeli
6. **Satış→ödeme→kasa observer** — Emare Saloon *(yeni)*
7. **Import batch preview/rollback** — raporlama-app *(yeni)*
8. **Marketplace adapter + sync SLA** — Emare Pazar *(yeni)*
9. BOM maliyet + fire oranı — Finance
10. MRP → PO önerisi — Finance
11. İzin onayında bakiye düşürme
12. QC failed≤tested
13. Satın alma→PO akışı
14. RBAC Module.Resource.Action
15. **Servis→parça→fatura** — emareaplincedesk *(yeni)*
16. **ResponseRule workflow** — emareasistan *(yeni)*
17. **Çeviri key export** — translation-manager *(yeni)*
18. Ticket stage→e-posta
19. Otomasyon trigger+condition+action
20. DateTime UTC — ANAYASA

---

## Sonuç (TASK 021-B)

**Birincil taşıma kaynakları (güncel sıra):**

1. **yeni-versiyon-gecis** — ADR, Control Tower traceability (hedef blueprint)
2. **Emare Finance standalone** — finans, BOM, MRP, stok, satın alma, HR
3. **Emare Saloon + raporlama-app** — perakende/hizmet ERP + rapor/import *(yeni)*
4. **Elyafgroup** — platform kernel, CRM, Control Tower UI, omnichannel
5. **Emare Pazar** — marketplace adapter registry *(yeni)*
6. **emare-crm** — workflow/onay, Blueprint state machine
7. **translation-manager** — merkezi i18n *(yeni)*

**Taşınmamalı:** Derviş duplicate kopyaları, emarerp gömülü Finance, Desktop Ticket snapshot, netfactor, emaresetup/emarework meta araçları.

**Ayrı ürün hattı:** emarepos (restoran POS), emareciftlik (tarım vertical), flovla (deal rooms).

**Kritik boşluk:** Tekstil domain (fabric, yarn, dyeing) — hâlâ yok; Control Tower UI + Finance BOM genel üretim referansı.

---

## Dosya Konumu

Bu analiz yalnızca yerel workspace'te tutulur:

```
/Users/emre/Elyafgroup/docs/project-management/legacy/
├── LEGACY_PROJECT_INVENTORY.md
├── LEGACY_ENTITY_CATALOG.md
├── LEGACY_BUSINESS_RULES.md
└── LEGACY_REUSABILITY_REPORT.md
```

Public repo (`emraresoftware/yeni-versiyon-gecis`) — mimari referans olarak TASK 021-B'de incelendi; kod eklenmedi.

---

# TASK 021-B Keşif Özeti

| Metrik | TASK 021 | TASK 021-B |
|--------|----------|------------|
| Tespit edilen projeler | 12 | **35+ benzersiz** |
| Git repo (Dergah) | — | **74** |
| Arşiv klasörleri | 0 | **43** (`26.03.2026/`) |
| Duplicate kopya | — | **~60+** (Dervişler/worktree) |
| Yeni birincil ERP kaynak | — | Emare Saloon, raporlama-app, Emare Pazar |
