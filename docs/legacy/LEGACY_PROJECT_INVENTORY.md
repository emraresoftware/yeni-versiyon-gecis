# Legacy Project Inventory — TASK 021

**Tarih:** 2026-06-28 (TASK 021-B genişletme: aynı gün)  
**Kapsam:** Yerel makine taraması — git repo + arşiv + Derviş dedup (kod değişikliği yok)  
**Referans:** Elyafgroup `AGENTS.md`, `ANAYASA.md`, `DOMAIN_MODEL.md`, `CONTROL_TOWER_FINAL_SCOPE.md`, `FEATURE_TRACEABILITY_MATRIX.md`

---

## Özet

Bu bilgisayarda **12+ birincil** ve **genişletilmiş taramada 35+ ERP/CRM/operasyon adayı** tespit edildi (`Dergah/` altında ~74 git repo). İki paralel hat var:

1. **.NET 8 Emare BOS hattı** — `Elyafgroup` (aktif, stratejik hedef platform)
2. **Laravel ERP/CRM hattı** — `emarerp/emare-crm` + `Emare Finance` standalone (olgun domain, farklı stack)

Çağrı merkezi, POS ve B2B CRM ayrı repolarda. Tekstil/üretim domain'i **yalnızca Control Tower UI stub'ları ve Emare Finance BOM/MRP** ile temsil ediliyor; kumaş/iplik/dokuma entity'si yok.

---

## Proje Envanteri

### 1. Elyafgroup (Emare Ai Dashboard / Emare BOS)

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Elyafgroup` |
| **Teknoloji** | .NET 8 (Clean Architecture, CQRS/MediatR), Next.js 16, PostgreSQL, EF Core, Asterisk, Python voice bridge |
| **Kaynak dosya** | ~847 `.cs`, ~399 `.ts/.tsx`, ~48 test dosyası |
| **Durum** | **Aktif** — son commit 2026-06-28, branch `gece-otonom` |
| **Rol** | Yeni Emare BOS hedef platformu; legacy + greenfield birlikte |

**Domain modülleri:**

| Modül | Durum |
|-------|-------|
| CRM | Olgun (legacy Customer + yeni Elyaf CrmAccount/Opportunity/Proposal) |
| Sales | Hafif (SalesLead, legacy Order/Proposal; SalesOrder entity yok) |
| Finance | Stub (UI mock, entity yok) |
| HR | Stub |
| Production | Stub (KPI mock) |
| Planning / MRP | Plan only (doküman) |
| Inventory / Purchasing | Plan only |
| Logistics | Stub UI |
| QC | Stub UI |
| Maintenance | Yok |
| Costing | Yok |
| Reporting | Olgun (service desk); Elyaf raporları mock |
| Ticket / Service Desk | Olgun |
| Call Center / Telephony | Olgun |
| Textile Control Tower | UI + seed (16 rol dashboard) |

**Dashboard:** CEO, Sales, Finance, Production, QC, Fabric, Merchandising, Design, Logistics, HR, Compliance, Licensing, Performance, Modelroom, Accessories, Digitalization — `web/src/features/elyaf-control-tower/`

**i18n:** `emare-i18n` paketi, 50+ locale dosyası; kanonik hedef tr-TR, en-US, de-DE, ar-SA

**Yeniden kullanılabilirlik:** ★★★★☆ (platform iskelet, tenant, RBAC, omnichannel, AI)

---

### 2. emarerp / emare-crm

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/emarerp/emare-crm` |
| **Teknoloji** | Laravel 11, PHP 8.2, Livewire 4, Alpine.js, Tailwind 3, PostgreSQL, Sanctum, Horizon, Gemini AI |
| **Kaynak dosya** | ~665 PHP app, 186 model, 107 blade, 89 test |
| **Durum** | **Aktif** — ana CRM/ERP monorepo bileşeni |

**Domain modülleri:**

| Modül | Durum |
|-------|-------|
| CRM | Olgun (Hesap, Kişi, Fırsat, Aday, Aktivite) |
| Sales | Olgun (Teklif, Sözleşme, Fatura, Kampanya, Kanban) |
| Finance | Kısmi (`HesapPlani`, `YevmiyeFisi`, `CariHesap`, Finance modülü taşınıyor) |
| HR | Orta (Çalışan, İzin, Eğitim) |
| Production | Yok (saha `IsEmri` var, üretim değil) |
| Inventory | Orta (Depo, StokHareketi, MalKabul) |
| Purchasing | Orta (SatinalmaTalebi, Tedarikci) |
| Logistics | Hafif |
| QC | Veri kalite kuralları |
| Reporting | Olgun (Raporlama Livewire, executive report) |
| Call Center | Orta (TicketQueue, CagriKaydi) |
| Workflow | Olgun (Blueprint state machine, OnayAkisi, OtomasyonKurali) |

**Dashboard:** ErpDashboard, SalesDashboard, FinanceDashboard, SupportDashboard, CallCenterDashboard

**i18n:** Türkçe ağırlıklı; ayrı lang altyapısı yok

**Yeniden kullanılabilirlik:** ★★★★☆ (iş kuralları ve domain model referansı; stack farklı)

---

### 3. Emare Finance (Emare Dashboard — standalone)

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/Emare Finance` |
| **Teknoloji** | Laravel 12, PHP 8.2, Blade, Tailwind 4, Alpine.js, Turbo, multi-tenant |
| **Kaynak dosya** | ~518 PHP app, 194 model, 365 blade, 58 test (+ mobile companion) |
| **Durum** | **Aktif / prod** — 300 test yeşil, deploy script mevcut |

**Domain modülleri:**

| Modül | Durum |
|-------|-------|
| CRM | Hafif (Lead, Opportunity, CustomerContact) |
| Sales | Olgun (Sale, Quote, POS, Campaign) |
| Finance | **Olgun** (AccountPlan, JournalEntry, bilanço, mizan, e-fatura) |
| HR | Olgun (Employee, Leave, Timesheet, Recruitment) |
| Production | **Olgun** (Bom, BomLine, BomOperation, Workstation, MrpRule, MrpSuggestion) |
| Inventory | Olgun (StockMovement, ProductBatch, ProductSerial) |
| Purchasing | Olgun (PurchaseOrder, GoodsReceipt, SupplierProposal) |
| Logistics | Orta (Shipment) |
| QC | Yok |
| Costing | BOM unitCost, fire oranı |
| Reporting | Olgun (ReportController 734+ satır, CSV export) |
| Marketplace | Trendyol, Hepsiburada, N11 |

**Dashboard:** Ana dashboard, muhasebe dashboard, tedarik raporları

**i18n:** TR + EN (`lang/tr`, `lang/en`, SetLocale middleware); ~350 view henüz `__()` kullanmıyor

**Textile:** `industry=textile` firma seçeneği; domain entity yok

**Yeniden kullanılabilirlik:** ★★★★★ (finans, BOM, MRP, stok, satın alma — iş mantığı kaynağı)

---

### 4. emarerp / Emare Finance (gömülü kopya)

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/emarerp/Emare Finance` |
| **Teknoloji** | Laravel (eski snapshot) |
| **Kaynak dosya** | ~128 PHP app, 65 model |
| **Durum** | **Legacy** — standalone'ın gerisinde |

**Yeniden kullanılabilirlik:** ★★☆☆☆ (referans değil; standalone kullanılmalı)

---

### 5. emarecc / emarecallcenter

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/emarecc` (+ prod kopya `/Users/emre/emarecallcenter`) |
| **Teknoloji** | Node.js/Express/TS, React/Vite/MUI, PostgreSQL, Redis, BullMQ, Asterisk 18 |
| **Kaynak dosya** | ~22k toplam (çoğu node_modules); backend ~48 route dosyası |
| **Durum** | **Aktif** — git 2026, prod backup dump'ları mevcut |

**Domain modülleri:** Telephony, tahsilat CRM, kampanya dialer, CDR, SMS, wallboard

**Dashboard:** Agent dashboard, wallboard, CDR/müşteri raporları

**Permissions:** admin / supervisor / agent (JWT + DB rol)

**Yeniden kullanılabilirlik:** ★★★☆☆ (CC/tahsilat; ERP değil)

---

### 6. Floragenix CRM

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Genel/Floragenix_CRM` |
| **Teknoloji** | Next.js 16, React 19, Prisma/SQLite, NextAuth, MUI 7 |
| **Kaynak dosya** | ~157 dosya `src/` |
| **Durum** | **Aktif** — Şubat 2026 commit'leri |

**Domain modülleri:** Lead CRM, Proposal, Product/Stock, dealer network, automation, calendar, warehouse, reports

**Dashboard:** KPI, pipeline, trend, stok özeti; CSV/XLSX/PDF export

**Permissions:** ADMIN, LEADER, EMPLOYEE, DEALER, WAREHOUSE

**Yeniden kullanılabilirlik:** ★★★☆☆ (satış hunisi + bayi hiyerarşisi pattern)

---

### 7. emarepos (Emare POS)

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/emarepos/pos-system` |
| **Teknoloji** | Laravel 12, PHP 8.2, Blade, ESC/POS |
| **Kaynak dosya** | ~349 PHP (vendor hariç) |
| **Durum** | **Aktif** — Mart 2026 migration'lar |

**Domain modülleri:** POS, restoran (masa/mutfak), stok, kasa, tenant/plan/module SaaS

**Dashboard:** Dashboard KPI, finansal/stok raporları

**Yeniden kullanılabilirlik:** ★★★☆☆ (perakende stok + tenant SaaS modeli)

---

### 8. Emare Ticket 17.03.18 (Desktop snapshot)

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Desktop/Emare Ticket 17.03.18` |
| **Teknoloji** | .NET 8 + Next.js (EmareTicket solution) |
| **Durum** | **Snapshot / legacy** — Elyafgroup ile aynı mimari, eski tarih |

**Not:** Elyafgroup aktif geliştirme hattıdır; bu kopya referans amaçlı.

**Yeniden kullanılabilirlik:** ★★☆☆☆ (Elyafgroup tercih edilmeli)

---

### 9. emare-crm-mobile

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/emarerp/emare-crm-mobile` |
| **Teknoloji** | React Native 0.76, Expo 52 |
| **Kaynak dosya** | 24 dosya |
| **Durum** | **MVP** |

**Yeniden kullanılabilirlik:** ★★☆☆☆

---

### 10. Elyafgroup / reseller-portal

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Elyafgroup/reseller-portal` |
| **Teknoloji** | Next.js (16 dosya) |
| **Durum** | **Hafif / yardımcı** — multi-tenant reseller yönetimi |

**Yeniden kullanılabilirlik:** ★★★☆☆ (SaaS reseller pattern)

---

### 11. Emare contact

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Emare contact` |
| **Kaynak dosya** | ~200 kaynak dosya |
| **Durum** | **Yardımcı** — iletişim/CRM benzeri |

**Yeniden kullanılabilirlik:** ★★☆☆☆

---

### 12. emarecloud

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/emarecloud` |
| **Kaynak dosya** | ~229 kaynak dosya |
| **Durum** | **Altyapı / hosting** — ERP domain değil |

**Yeniden kullanılabilirlik:** ★☆☆☆☆ (ERP domain için)

---

## Textile / Manufacturing Özel Arama Sonuçları

| Kavram | Bulunduğu Proje | Not |
|--------|-----------------|-----|
| Fabric | Elyafgroup Control Tower UI | Mock KPI; entity yok |
| Yarn / Dyeing / Knitting / Weaving | — | Kod tabanında yok |
| Sample | Elyafgroup `ElyafSample` | Hafif entity |
| Merchandising | Elyafgroup dashboard + `ElyafCollection` | UI olgun, backend seed |
| BOM | Emare Finance standalone | Tam implementasyon + test |
| MRP | Emare Finance standalone | MrpRule, MrpSuggestion + test |
| Routing (üretim) | Emare Finance `BomOperation` | İş istasyonu bağlantılı |
| WorkOrder / ProductionOrder | Emare Finance (migration) | emare-crm'de saha IsEmri (farklı domain) |
| Costing | Emare Finance `Bom::unitCost()` | Fire oranı dahil |
| Capacity Planning | Elyafgroup KPI mock | OEE, kapasite grafikleri seed |

---

## Aktif vs Legacy Sınıflandırması

| Proje | Sınıf |
|-------|-------|
| Elyafgroup | Aktif — stratejik hedef |
| emarerp/emare-crm | Aktif — domain referans |
| Emare Finance standalone | Aktif — finans/üretim kaynağı |
| emarecc / emarecallcenter | Aktif — CC prod |
| Floragenix CRM | Aktif — B2B pattern |
| emarepos | Aktif — POS/stok |
| emarerp/Emare Finance (gömülü) | Legacy |
| Desktop Emare Ticket 17.03.18 | Legacy snapshot |
| emare-crm-mobile | MVP |

---

## Notlar

- `Ortak Çalışma/moduller/modules.json` birçok repoda **EmareTicket (.NET) modül haritasını** içerir; Laravel projeleri için güvenilir değil. Kaynak: ilgili repo `composer.json` / `README.md`.
- Public repo (`emraresoftware/yeni-versiyon-gecis`) kod içermez; **mimari referans** olarak TASK 021-B'de incelendi.
- `/Users/emre/Dergah/emareapi/Dervisler/` altında **50+ proje kopyası** var — envanterde canonical path sayılır, duplicate olarak işaretlenir.

---

# TASK 021-B — Genişletilmiş Keşif

## Tarama Yöntemi

1. `find … -name '.git'` → Dergah altında **74 repo**
2. Arşiv: `/Users/emre/Dergah/Emare projeler/tüm projeler/26.03.2026/` (**43 klasör**)
3. Manifest taraması: `composer.json`, `*.sln`, `requirements.txt`
4. README/HAFIZA grep: ERP, CRM, finans, stok, tedarik
5. Duplicate dedup: Derviş kopyaları, worktree'ler, arşiv vs aktif path

## Yeni Keşfedilen Projeler (TASK 021'de yoktu)

### A) ERP/Operasyon — Yüksek değer

| # | Proje | Konum | Stack | Dosya | Durum | Puan |
|---|-------|-------|-------|-------|-------|------|
| 13 | **Emare Saloon** | `Dergah/Emare projeler/Emare saloon` | Laravel 12, PayTR/Iyzico, DomPDF | ~100 app PHP, 96 model | Aktif | ★★★★★ |
| 14 | **raporlama-app** | `Desktop/raporlama/raporlama-app` | Laravel 13, multi-tenant | ~22 app PHP | Aktif | ★★★★★ |
| 15 | **Emare Pazar** | `Dergah/Emare projeler/Emare pazar` | FastAPI, Celery, PostgreSQL | ~67 kaynak | Aktif | ★★★★☆ |
| 16 | **emareciftlik** | arşiv `26.03.2026/emareciftlik` | Laravel 13, 50 model | ~346 | Arşiv (git yok) | ★★★★☆ |
| 17 | **emareaplincedesk** | arşiv `26.03.2026/emareaplincedesk` | Laravel 12, servis masası | ~82, 13 model | Arşiv 2026-03-09 | ★★★★☆ |
| 18 | **emareasistan** | `Dergah/Emare projeler/emareasistan` | FastAPI, RAG, WhatsApp | ~240 | Aktif | ★★★☆☆ |
| 19 | **ecomaiq** | `Desktop/ecomaiq` | React+Express V1, Turbo V2 | ~10k (node_modules dahil) | Aktif | ★★★☆☆ |
| 20 | **translation-manager** | `Dergah/Emare projeler/translation-manager` | Laravel 12, Filament 3 | ~28 app PHP | Aktif | ★★★★☆ |

### B) Arşiv snapshot — `26.03.2026/` (43 klasör)

**Arşiv donma tarihi:** çoğu repo **2026-03-09**; istisna **emarepos → 2026-03-22**.

| Proje | ERP relevance | Not |
|-------|---------------|-----|
| **emarepos** (arşiv) | Yüksek | Aktif POS kopyası; 53 Eloquent model, 71+ route |
| **emareciftlik** | Yüksek | Vertical tarım ERP: Animal, MilkRecord, InventoryItem, Financial* |
| **emareaplincedesk** | Orta-yüksek | ServiceRequest, Invoice, SparePart, Technician |
| **emaretedarik** | Orta (iskelet) | FastAPI stub — tedarik domain planlı, kod minimal |
| **emarepazar** (arşiv) | Orta (iskelet) | FastAPI+Next stub; aktif kopya `Emare pazar` |
| **emareflow** | Orta | n8n benzeri workflow; Finance node planlı |
| **emaresuperapp** | Orta | Platform shell: auth, wallet, marketplace planned |
| **emareflux** | Düşük | Event bus stub |
| **emare_dashboard** | Düşük | Flask — Derviş/proje envanteri (devops) |
| **emarework** | Düşük | Meta — `ceyiz_hazirla.py` tüm iskeletlerin kaynağı |
| **emaresetup** | Yok | AI yazılım fabrikası (OpenHands) |
| emareai, emareapi, Emaresiber, emareteam, … | Yok/Düşük | AI, API vault, güvenlik, ekip — ERP dışı |

### C) Meta / Mimari (kod değil, blueprint)

| Proje | Konum | Rol | Puan |
|-------|-------|-----|------|
| **yeni-versiyon-gecis** | `/Users/emre/yeni-versiyon-gecis` | Public mimari: ADR, Control Tower, traceability | ★★★★★ |
| **emare-public** | `/Users/emre/emare-public` | Public portal + cursor-kit | ★★★☆☆ |
| **emare-workspace** | `/Users/emre/emare-workspace` | Ajan playbook: erp-architect, erp-finance, erp-domain… | ★★☆☆☆ |
| **emare-is-havuzu** | `/Users/emre/emare-is-havuzu` | TASKS.md koordinasyon | ★★☆☆☆ |

### D) Diğer

| Proje | Konum | Not |
|-------|-------|-----|
| **flovla (Closy)** | arşiv `flovla` | Digital deal rooms — B2B satış UX, ERP core değil |
| **netfactor** | `/Users/emre/netfactor` | Kurumsal site + ESXi — ERP dışı |
| **Floragenix Websitesi** | arşiv | Statik site |

---

## Emare Saloon — Detay (yeni birincil kaynak)

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/Emare saloon` |
| **Teknoloji** | Laravel 12, PHP 8.2, Tailwind 4, DomPDF, PayTR/Iyzico, PWA |
| **Kaynak** | ~96 model (Emare Finance modül envanterinden), observer zinciri |
| **Modüller** | Randevu, CRM, personel, kasa/ödeme, stok, rapor, SMS/kampanya, modül yönetimi |
| **Dashboard** | Salon ERP dashboard, kasa, stok raporları |
| **i18n** | TR ağırlıklı |
| **Yeniden kullanılabilirlik** | ★★★★★ — Emare Finance soyundan perakende/hizmet ERP |

---

## Emare Pazar — Detay

| Alan | Değer |
|------|-------|
| **Konum** | `/Users/emre/Dergah/Emare projeler/Emare pazar` |
| **Teknoloji** | FastAPI, SQLAlchemy 2, PostgreSQL, Redis, Celery |
| **Modüller** | 14 marketplace adapter, ürün kataloğu, sipariş/stok sync |
| **Entity'ler** | Marketplace, Product, ProductVariant, Order, CategoryMapping |
| **İş kuralları** | Adapter normalizasyon; 15dk sipariş / 5dk stok sync |
| **Yeniden kullanılabilirlik** | ★★★★☆ — e-ticaret entegrasyon katmanı |

---

## emareciftlik — Detay (vertical ERP)

| Alan | Değer |
|------|-------|
| **Konum** | arşiv `26.03.2026/emareciftlik` |
| **Teknoloji** | Laravel 13, PHP 8.3, SQLite, 50 model |
| **Modüller** | Hayvancılık, süt, yem, sağlık, stok, finans, CRM, personel, sulama |
| **Entity'ler** | Animal, MilkRecord, InventoryItem, Contact, Staff, Field, Equipment |
| **Yeniden kullanılabilirlik** | ★★★★☆ — stok/finans/CRM pattern; tekstil değil tarım vertical |

---

## Duplicate / Dedup Matrisi

| Canonical (say) | Duplicate (sayma) |
|-----------------|-------------------|
| `Dergah/Emare projeler/emarepos` | arşiv `26.03.2026/emarepos`, `emareapi/Dervisler/emarepos Dervishi` |
| `Dergah/Emare projeler/Emare pazar` | arşiv `26.03.2026/emarepazar` |
| `Elyafgroup` | `.windsurf/worktrees/`, `.claude/worktrees/`, Desktop Ticket snapshot |
| `Emare Finance standalone` | `emarerp/Emare Finance` gömülü kopya |
| `emarecc` | `emarecallcenter` (prod fork) |

**Toplam benzersiz ERP adayı:** ~35  
**Toplam git repo (Dergah):** 74  
**Duplicate kopya (Dervişler+worktree):** ~60+

---

## Güncellenmiş Aktif vs Legacy

| Proje | Sınıf |
|-------|-------|
| Emare Saloon | Aktif — perakende/hizmet ERP |
| Emare Pazar | Aktif — marketplace entegrasyon |
| emareasistan | Aktif — omnichannel asistan |
| raporlama-app | Aktif — rapor/import |
| translation-manager | Aktif — i18n merkezi |
| ecomaiq | Aktif — Trendyol Q&A |
| yeni-versiyon-gecis | Aktif — mimari blueprint |
| Arşiv 26.03.2026 (bulk) | Legacy snapshot 2026-03-09 |
| emareciftlik (arşiv) | Legacy — vertical ERP referans |
| Derviş kopyaları | Duplicate — canonical path kullan |
