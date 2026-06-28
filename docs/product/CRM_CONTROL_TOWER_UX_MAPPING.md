# CRM Control Tower UX Mapping

**Versiyon:** 1.1.0  
**Durum:** Draft — Onay Bekliyor  
**Sahip:** Product Board / Agent 5 (UX Review)  
**Son Güncelleme:** 2026-06-28  
**Bağımlı Dokümanlar:** CONTROL_TOWER_FINAL_SCOPE.md, FEATURE_TRACEABILITY_MATRIX.md, DOMAIN_MODEL.md, SECURITY_AUTHORIZATION.md, UX_REVIEW.md, LOCALIZATION_I18N_STANDARDS.md, TASK_013A_CRM_HARDENING_REPORT.md, TASK_013A_PRODUCT_TRACEABILITY_UPDATE.md

---

## Amaç

Bu doküman, **CEO Control Tower** ve **Sales Control Tower** ekranlarında CRM verisinden beslenen kartların UX yerleşimini, rol/permission eşlemesini, entity kaynağını ve MVP kabul kriterlerini tanımlar.

> Kod içermez. Private kod reposuna dokunulmaz.

---

## Task 013A Hizalama Notu (2026-06-28)

Task 013A CRM Foundation Hardening sonrası aşağıdaki domain alanları UX mapping'e resmen bağlanmıştır:

| Alan | Entity | Aralık / Değer | Etkilenen kartlar |
|---|---|---|---|
| `Segment` | `CrmAccount` | A · B · C · D | Customer Panel, segment filtreleri |
| `NpsScore` | `CrmAccount` | 0–10 | NPS KPI, Customer Panel |
| `HealthScore` | `CrmAccount` | 0–100 | Customer Health Score |
| `RiskScore` | `CrmAccount` | 0–100 | Customer Risk Score |
| Satır kalemleri | `CrmProposalItem` | `Description`, `Quantity`, `UnitPrice`, `Currency`, `LineTotal` | Proposal Pipeline, Approval Queue, Proposals menüsü |

**Yeni permission seti (least privilege):** `CRM.Opportunity.Read/Write`, `CRM.Activity.Read/Write` — fırsat ve aktivite kartlarında `CRM.Account.Read` yerine dar yetki kullanılır ([TASK_013A_PRODUCT_TRACEABILITY_UPDATE.md](../project-management/reports/TASK_013A_PRODUCT_TRACEABILITY_UPDATE.md)).

---

## Kapsam Özeti

| Kart | CEO CT | Sales CT | UI Bölgesi (standart) |
|---|---|---|---|
| Customer Count | ✅ KPI satırı | ✅ KPI / Customer Panel | KPI Kartları |
| Active Opportunities | ○ Snapshot özet | ✅ KPI satırı | KPI Kartları |
| Proposal Pipeline | — | ✅ Menü + widget | KPI + Opportunities Pipeline |
| Proposal Item Details | — | ✅ Proposal expand / modal | Proposals & Quotes |
| Customer Health Score | ✅ Stakeholder / Health | ✅ Health Score widget | Risk / Health Score |
| Customer Risk Score | ✅ Stakeholder / Health | ✅ Health Score widget | Risk / Health Score |
| NPS | ✅ KPI satırı | ✅ Customer Panel kolonu | KPI Kartları |
| Open Activities | — | ✅ Customer Panel / Priorities | Today's Priorities |
| Proposal Approval Queue | ○ Priorities (yüksek tutar) | ✅ Priorities / Queue | Today's Priorities |
| Segment Filters | ✅ Toolbar + Stakeholder | ✅ Toolbar + Customer Panel | Export / Filter / Date controls |

**Lejant:** ✅ birincil yerleşim · ○ ikincil/özet görünüm · — doğrudan kart yok

---

## Ortak UX Kuralları

- Tüm kart etiketleri `emare-i18n` üzerinden; hardcoded metin yasak ([LOCALIZATION_I18N_STANDARDS.md](LOCALIZATION_I18N_STANDARDS.md)).
- KPI kartları: ana değer + trend ok + periyot karşılaştırması ([UX_REVIEW.md](UX_REVIEW.md) § KPI Card Standards).
- Loading / empty / error state zorunlu (Skeleton, "—", yeniden dene).
- Tenant izolasyonu: tüm sorgular `TenantId` filtresi ile; permission yoksa kart gizlenir (403 değil, graceful hide).
- Tarih aralığı + **segment filtresi** global toolbar'dan tüm CRM kartlarına propagate edilir.
- Skor alanları domain validasyonu ile uyumlu gösterilir: NPS 0–10, Health/Risk 0–100; geçersiz değer UI'da "—" + audit uyarısı.

---

## Segment Filtreleri (Cross-Cutting)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `common.filters.segment` |
| **Kullanıcı rolü** | CEO, SalesManager, TenantAdmin (Auditor read-only) |
| **Veri kaynağı entity** | `CrmAccount.Segment` (A \| B \| C \| D) |
| **Permission** | `CEO.ControlTower.View` / `Sales.ControlTower.View` + `CRM.Account.Read` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Toolbar'da multi-select chip filtresi (Tümü + A/B/C/D); seçim KPI, panel, health/risk ve NPS kartlarına anında yansır; URL query (`?segment=A,B`) ile paylaşılabilir deep link; segment badge renkleri legend'da; RTL'de chip sırası mirror; filtresiz toplam ile filtreli alt küme tutarlı |

**Etkilenen API'ler:** tüm `GET /api/control-tower/{ceo\|sales}/...` CRM endpoint'leri `segment` query param kabul eder.

---

## Kart Tanımları

### 1. Customer Count (Aktif Müşteri Sayısı)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.ceo.kpi.activeCustomers` / `pages.sales.kpi.newCustomers` |
| **Kullanıcı rolü** | **CEO CT:** CEO, TenantAdmin, Auditor. **Sales CT:** SalesManager, CEO, TenantAdmin |
| **Veri kaynağı entity** | `CrmAccount` (`IsDeleted = false`, durum Active; segment filtresine tabi) |
| **Permission** | `CEO.ControlTower.View` + `CRM.Account.Read` · `Sales.ControlTower.View` + `CRM.Account.Read` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Segment filtresi aktifken yalnızca seçili segment(ler) sayılır; trend ±% + ok; tıklanınca filtreli `Customer Accounts` listesi; CEO/Sales aynı segment+periyotta aynı sayı |

**API:** `GET /api/control-tower/ceo/kpis/active-customers` · `GET /api/control-tower/sales/kpis/new-customers`

---

### 2. Active Opportunities (Aktif Fırsatlar)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.kpi.activeOpportunities` |
| **Kullanıcı rolü** | SalesManager, CEO, TenantAdmin · CEO CT: Executive Snapshot özet |
| **Veri kaynağı entity** | `CrmOpportunity`, `CrmAccount` (segment via account) |
| **Permission** | `Sales.ControlTower.View` + **`CRM.Opportunity.Read`** |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Sayı + para birimi toplam değer; segment filtresi account üzerinden uygulanır; "View all" → Opportunities Pipeline; mobil KPI carousel |

**API:** `GET /api/control-tower/sales/kpis/active-opportunities`

---

### 3. Proposal Pipeline (Teklif Hunisi)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.widgets.proposalPipeline` |
| **Kullanıcı rolü** | SalesManager, CEO, TenantAdmin, FinanceManager (read-only) |
| **Veri kaynağı entity** | `CrmProposal`, **`CrmProposalItem`** (tutar = `LineTotal` toplamı), `CrmOpportunity` |
| **Permission** | `Sales.ControlTower.View` + `CRM.Proposal.Read` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Hunide 4+ aşama, adet + tutar (kalem toplamlarından); segment account bazlı filtre; stage tıklanınca Proposals listesi; kalem tutarları header tutarı ile ±0.01 toleransla eşleşir |

**API:** `GET /api/control-tower/sales/kpis/proposal-conversion` · `GET /api/crm/proposals`

---

### 4. Proposal Item Details (Teklif Kalem Detayları)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.widgets.proposalItemDetails` |
| **Kullanıcı rolü** | SalesManager, CEO, TenantAdmin, FinanceManager (read-only) |
| **Veri kaynağı entity** | **`CrmProposalItem`** (child of `CrmProposal`): `Description`, `Quantity`, `UnitPrice`, `Currency`, `LineTotal` |
| **Permission** | `CRM.Proposal.Read` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** (Task 013A zorunlu) |
| **Kabul kriteri** | Proposal satırında expand veya side panel ile kalem listesi; kolonlar: açıklama, miktar, birim fiyat, para birimi, satır toplamı; `LineTotal = Quantity × UnitPrice` UI'da doğrulanır; onay kuyruğunda en az ilk 3 kalem özet; boş kalem listesi empty state; i18n para birimi locale formatı; mobilde accordion |

**API:** `GET /api/crm/proposals` (items nested) · `GET /api/crm/proposals/{id}/items` (detay drill-down)

---

### 5. Customer Health Score (Müşteri Sağlık Skoru)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.shared.widgets.customerHealthScore` |
| **Kullanıcı rolü** | **Sales CT:** SalesManager, CEO · **CEO CT:** CEO, TenantAdmin |
| **Veri kaynağı entity** | **`CrmAccount.HealthScore`** (0–100), `CrmOpportunity` (pipeline sağlığı), `CompanyHealthScore` (CEO aggregate) |
| **Permission** | `Sales.ControlTower.View` · `CEO.ControlTower.View` + `CRM.Account.Read` |
| **MVP önceliği** | 🟠 **P1 — Sprint 2A** (domain alanı Task 013A ile kilitli) |
| **Kabul kriteri** | Gauge 0–100 + A–F legend eşlemesi; portföy ortalaması segment filtresine duyarlı; CEO Top 10 müşteri panelinde `HealthScore` kolonu; null skor "—"; skor güncellemesi `CrmAccountUpdated` sonrası ≤60 sn; tooltip'te skor bileşenleri özeti; WCAG `aria-label`: "Sağlık skoru 72, iyi" |

**API:** `GET /api/control-tower/sales/health-scores` · `GET /api/control-tower/ceo/health-scores` · `GET /api/control-tower/ceo/stakeholders`

---

### 6. Customer Risk Score (Müşteri Risk Skoru)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.shared.widgets.customerRiskScore` |
| **Kullanıcı rolü** | **Sales CT:** SalesManager, CEO · **CEO CT:** CEO, TenantAdmin |
| **Veri kaynağı entity** | **`CrmAccount.RiskScore`** (0–100); cross-context sinyaller: `FinanceInvoice`, `QcClaim`, `SalesOrder` (logical FK) |
| **Permission** | `Sales.ControlTower.View` + `CRM.Account.Read` · CEO drill-down: `Finance.Invoice.Read`, `QC.Claim.Read` |
| **MVP önceliği** | 🟠 **P1 — Sprint 2A** |
| **Kabul kriteri** | `RiskScore` 0–100 gauge; eşik ≥70 kırmızı badge + Critical Alerts link; segment filtresi uygulanır; en yüksek risk 5 müşteri listesi (Sales); CEO stakeholder panelinde `RiskScore` kolonu; domain dışı değer UI'da gösterilmez |

**API:** `GET /api/control-tower/sales/health-scores` · `GET /api/control-tower/ceo/alerts/critical`

---

### 7. NPS (Net Promoter Score)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.ceo.kpi.nps` · `pages.sales.panel.npsColumn` |
| **Kullanıcı rolü** | CEO, TenantAdmin, SalesManager |
| **Veri kaynağı entity** | **`CrmAccount.NpsScore`** (0–10 per account), `KPIValue` (aggregate snapshot) |
| **Permission** | `CEO.ControlTower.View` + `CRM.Account.Read` · Sales panel: `CRM.Account.Read` |
| **MVP önceliği** | 🟠 **P1 — Sprint 2A** |
| **Kabul kriteri** | CEO KPI: tenant ortalama NPS (0–10 skala, tek skala dokümante); trend vs geçen çeyrek; Promoter (9–10) / Passive (7–8) / Detractor (0–6) dağılımı expand veya tooltip; veri yoksa N/A (sıfır ile karışmaz); Sales Customer Panel'de hesap bazlı `NpsScore` kolonu; segment filtresine duyarlı; `CrmAccountUpdated` event ile güncellenir |

**API:** `GET /api/control-tower/ceo/kpis/nps` · `GET /api/control-tower/sales/customers`

---

### 8. Open Activities (Açık Aktiviteler)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.widgets.openActivities` |
| **Kullanıcı rolü** | SalesManager, CEO · Employee: ABAC kendi kayıtları |
| **Veri kaynağı entity** | `CrmActivity` / `SalesActivityLog` |
| **Permission** | `Sales.ControlTower.View` + **`CRM.Activity.Read`** |
| **MVP önceliği** | 🟠 **P1 — Sprint 2A** |
| **Kabul kriteri** | Max 10 kayıt + "View all"; segment account üzerinden filtre; geciken aktivite badge; yazma CTA yalnızca `CRM.Activity.Write` ile |

**API:** `GET /api/control-tower/sales/priorities/today` · `GET /api/control-tower/sales/customers`

---

### 9. Proposal Approval Queue (Teklif Onay Kuyruğu)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.widgets.proposalApprovalQueue` |
| **Kullanıcı rolü** | SalesManager (`CRM.Proposal.Approve`), CEO (eşik üstü), TenantAdmin |
| **Veri kaynağı entity** | `CrmProposal`, **`CrmProposalItem`**; workflow: `CrmProposalApproval` |
| **Permission** | `Sales.ControlTower.View` + `CRM.Proposal.Read` · onay: `CRM.Proposal.Approve` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Satırda tutar (kalem toplamı), müşteri, segment badge, SLA, kalem sayısı; expand ile Proposal Item Details; onay/red human-in-the-loop; CEO CT yalnızca eşik üstü; 24h SLA → Critical Alerts; `CrmProposalApproved` sonrası anında düşer |

**API:** `GET /api/control-tower/sales/priorities/today` · `GET /api/crm/proposals?status=pendingApproval` · `POST /api/crm/proposals/{id}/approve`

---

## CEO Dashboard — CRM Kart Kabul Kriterleri

| # | Kart / Bölge | Zorunlu kabul kriteri |
|---|---|---|
| C1 | **KPI — Aktif Müşteri** | Segment filtresi + trend; `CRM.Account.Read` |
| C2 | **KPI — NPS** | Ortalama 0–10; `CrmAccount.NpsScore` aggregation; N/A state |
| C3 | **Risk / Health Score** | Şirket gauge + müşteri alt skorları (`CrmAccount.HealthScore`, `RiskScore` ortalaması) |
| C4 | **Customer Panel (Stakeholders)** | Top 10: segment badge, NPS, health, risk kolonları; sıralama health asc / risk desc |
| C5 | **Segment filtresi** | Toolbar chip; C1–C4 ile senkron |
| C6 | **Today's Priorities** | Yüksek tutarlı `CrmProposal` onay bekleyenleri (kalem detayı expand) |
| C7 | **Critical Alerts** | Yüksek `RiskScore` müşteri eskalasyonları |
| C8 | **Genel** | 15 UI bloğu scope uyumu; 4 dil i18n; loading/empty/error; WCAG 2.2 AA trend+skor `aria-label` |

**CEO minimum CRM KPI slot:** Aktif Müşteri + NPS en az 2/10 KPI satırında CRM kaynaklı.

---

## Sales Dashboard — CRM Kart Kabul Kriterleri

| # | Kart / Bölge | Zorunlu kabul kriteri |
|---|---|---|
| S1 | **KPI — Aktif Fırsatlar** | `CRM.Opportunity.Read`; segment filtreli |
| S2 | **KPI — Yeni Müşteri / dönüşüm** | `CRM.Account.Read` |
| S3 | **Proposal Pipeline** | Kalem toplamlı tutar; `CRM.Proposal.Read` |
| S4 | **Proposal Item Details** | Expand/modal; 5 alan; LineTotal doğrulama |
| S5 | **Health / Risk widget** | `CrmAccount.HealthScore` + `RiskScore`; portföy + bottom/top 5 |
| S6 | **Customer Panel** | Segment, status, NPS, health, risk kolonları; `CRM.Activity.Read` |
| S7 | **Open Activities** | `CRM.Activity.Read`; segment filtreli liste |
| S8 | **Proposal Approval Queue** | Kalem özeti + onay aksiyonu; `CRM.Proposal.Approve` |
| S9 | **Segment filtresi** | Toolbar; S1–S8 senkron |
| S10 | **Genel** | Min. 4 KPI CRM kaynaklı; Opportunities Pipeline menüsü `CRM.Opportunity.Read`; Proposals menüsü `CrmProposalItem` nested |

**Sales permission matrisi (Task 013A):**

| Kart grubu | Minimum permission |
|---|---|
| Fırsat KPI / Pipeline | `CRM.Opportunity.Read` |
| Teklif / kalem / onay | `CRM.Proposal.Read` (+ `Approve` for queue action) |
| Müşteri / skor / NPS | `CRM.Account.Read` |
| Aktivite | `CRM.Activity.Read` |
| Kule erişimi | `Sales.ControlTower.View` |

---

## CEO ↔ Sales Kart Matrisi (Detay)

| Kart | CEO — Birincil widget | Sales — Birincil widget |
|---|---|---|
| Customer Count | KPI: Aktif Müşteri | KPI: Yeni Müşteri + Panel özeti |
| Active Opportunities | Executive Snapshot | KPI: Aktif Fırsatlar |
| Proposal Pipeline | — | Pipeline hunisi |
| Proposal Item Details | — | Proposals expand + Approval Queue |
| Customer Health Score | Stakeholder + Health Scores | Health widget |
| Customer Risk Score | Stakeholder + Critical Alerts | Risk widget |
| NPS | KPI: NPS | Customer Panel kolonu |
| Open Activities | — | Activities list |
| Proposal Approval Queue | Priorities (eşik üstü) | Approval Queue widget |
| Segment Filters | Toolbar + Stakeholder | Toolbar + tüm CRM kartları |

---

## MVP Sprint Sıralaması (Sprint 2A — güncel)

| Sıra | Kart | Gerekçe |
|---|---|---|
| 1 | Segment Filters | Tüm CRM kartları için cross-cutting |
| 2 | Customer Count | Basit aggregation + segment |
| 3 | Active Opportunities | `CRM.Opportunity.Read` |
| 4 | Proposal Pipeline + Item Details | Task 013A `CrmProposalItem` |
| 5 | Proposal Approval Queue | Workflow entegrasyonu |
| 6 | Customer Health / Risk Score | `CrmAccount` skor alanları |
| 7 | NPS | `CrmAccount.NpsScore` aggregation |
| 8 | Open Activities | `CRM.Activity.Read` |

---

## İlgili Workflow ve Event'ler

| Kart | Domain Event | Workflow |
|---|---|---|
| Customer Count | `CrmAccountCreated`, `CrmAccountUpdated` | — |
| Active Opportunities | `CrmOpportunityCreated` | — |
| Proposal Pipeline / Items | `CrmProposalCreated`, `CrmProposalApproved` | `CrmProposalApproval` |
| Health / Risk / NPS / Segment | `CrmAccountUpdated` | — |
| NPS aggregate | `PerformanceKPIValueUpdated`, `CrmAccountUpdated` | — |
| Open Activities | `CrmOpportunityCreated` | — |
| Proposal Approval Queue | `CrmProposalCreated`, `CrmProposalApproved` | `CrmProposalApproval` |

---

## Revizyon Geçmişi

| Versiyon | Tarih | Açıklama |
|---|---|---|
| 1.0.0 | 2026-06-28 | İlk CRM Control Tower UX mapping (Agent 5) |
| 1.1.0 | 2026-06-28 | Task 013A fix: ProposalItem, skor/segment/NPS alanları, segment filtreleri, CEO/Sales kabul kriterleri |

---

## Referanslar

- [CONTROL_TOWER_FINAL_SCOPE.md](CONTROL_TOWER_FINAL_SCOPE.md) — §1 CEO, §2 Sales
- [FEATURE_TRACEABILITY_MATRIX.md](FEATURE_TRACEABILITY_MATRIX.md) — §1 CEO, §2 Sales (v1.1 Task 013A)
- [DOMAIN_MODEL.md](../../DOMAIN_MODEL.md) — CRM Entity Matrix
- [SECURITY_AUTHORIZATION.md](../../SECURITY_AUTHORIZATION.md) — Permission Matrix
- [UX_REVIEW.md](UX_REVIEW.md) — KPI / Widget standartları
- [TASK_013A_CRM_HARDENING_REPORT.md](../project-management/reports/TASK_013A_CRM_HARDENING_REPORT.md)
- [TASK_013A_PRODUCT_TRACEABILITY_UPDATE.md](../project-management/reports/TASK_013A_PRODUCT_TRACEABILITY_UPDATE.md)
- [WORKFLOW_ENGINE.md](../../WORKFLOW_ENGINE.md) — `CrmProposalApproval`

---

*Bu doküman ürün UX eşlemesi içerir. Kod içermez.*  
*Güncellemeler Product Board onayı ile yapılır.*
