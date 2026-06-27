# CRM Control Tower UX Mapping

**Versiyon:** 1.0.0  
**Durum:** Draft — Onay Bekliyor  
**Sahip:** Product Board / Agent 5 (UX Review)  
**Son Güncelleme:** 2026-06-28  
**Bağımlı Dokümanlar:** CONTROL_TOWER_FINAL_SCOPE.md, FEATURE_TRACEABILITY_MATRIX.md, DOMAIN_MODEL.md, SECURITY_AUTHORIZATION.md, UX_REVIEW.md, LOCALIZATION_I18N_STANDARDS.md

---

## Amaç

Bu doküman, **CEO Control Tower** ve **Sales Control Tower** ekranlarında CRM verisinden beslenen kartların UX yerleşimini, rol/permission eşlemesini, entity kaynağını ve MVP kabul kriterlerini tanımlar.

> Kod içermez. Private kod reposuna dokunulmaz.

---

## Kapsam Özeti

| Kart | CEO CT | Sales CT | UI Bölgesi (standart) |
|---|---|---|---|
| Customer Count | ✅ KPI satırı | ✅ KPI / Customer Panel | KPI Kartları |
| Active Opportunities | ○ Snapshot özet | ✅ KPI satırı | KPI Kartları |
| Proposal Pipeline | — | ✅ Menü + widget | KPI + Opportunities Pipeline |
| Customer Health Score | ✅ Stakeholder / Health | ✅ Health Score widget | Risk / Health Score |
| Customer Risk Score | ✅ Stakeholder / Health | ✅ Health Score widget | Risk / Health Score |
| NPS | ✅ KPI satırı | ○ Customer Panel | KPI Kartları |
| Open Activities | — | ✅ Customer Panel / Priorities | Today's Priorities |
| Proposal Approval Queue | ○ Priorities (yüksek tutar) | ✅ Priorities / Queue | Today's Priorities |

**Lejant:** ✅ birincil yerleşim · ○ ikincil/özet görünüm · — doğrudan kart yok (üst kule verisi yok)

---

## Ortak UX Kuralları

- Tüm kart etiketleri `emare-i18n` üzerinden; hardcoded metin yasak ([LOCALIZATION_I18N_STANDARDS.md](LOCALIZATION_I18N_STANDARDS.md)).
- KPI kartları: ana değer + trend ok + periyot karşılaştırması ([UX_REVIEW.md](UX_REVIEW.md) § KPI Card Standards).
- Loading / empty / error state zorunlu (Skeleton, "—", yeniden dene).
- Tenant izolasyonu: tüm sorgular `TenantId` filtresi ile; permission yoksa kart gizlenir veya maskelenir (403 değil, graceful hide).
- Tarih aralığı: global toolbar seçimi KPI ve liste kartlarına propagate edilir.

---

## Kart Tanımları

### 1. Customer Count (Aktif Müşteri Sayısı)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.ceo.kpi.activeCustomers` / `pages.sales.kpi.newCustomers` (Sales'te aylık yeni müşteri varyantı) |
| **Kullanıcı rolü** | **CEO CT:** CEO, TenantAdmin, Auditor (read-only KPI). **Sales CT:** SalesManager, CEO, TenantAdmin |
| **Veri kaynağı entity** | `CrmAccount` (aktif statü: `IsDeleted = false`, hesap durumu Active) |
| **Permission** | `CEO.ControlTower.View` + `CRM.Account.Read` (CEO) · `Sales.ControlTower.View` + `CRM.Account.Read` (Sales) |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | KPI kartında tenant-scoped aktif müşteri sayısı gösterilir; seçili periyoda trend (±%) ve ok yönü vardır; veri yoksa empty state; `CrmAccountCreated` sonrası 60 sn içinde güncellenir; CEO ve Sales aynı sayıyı aynı filtrede gösterir; tıklanınca ilgili müşteri listesine (`Customer Accounts`) gider |

**API referansı:** `GET /api/control-tower/ceo/kpis/active-customers` · `GET /api/control-tower/sales/kpis/new-customers` (Sales aylık varyant)

---

### 2. Active Opportunities (Aktif Fırsatlar)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.kpi.activeOpportunities` |
| **Kullanıcı rolü** | **Sales CT:** SalesManager, CEO, TenantAdmin. **CEO CT:** yalnızca Executive Snapshot özet satırında (ayrı KPI kartı değil) |
| **Veri kaynağı entity** | `CrmOpportunity`, `CrmAccount` (toplam değer = fırsat tutarları toplamı) |
| **Permission** | `Sales.ControlTower.View` + `CRM.Account.Read` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Kart sayı + para birimi formatlı toplam değer gösterir; açık/kapanmamış stage filtresi scope ile uyumlu; trend önceki aya göre; Sales KPI satırında min. 4 kart içinde yer alır; "View all" → `Opportunities Pipeline` menüsü; mobilde KPI carousel'de görünür |

**API referansı:** `GET /api/control-tower/sales/kpis/active-opportunities`

---

### 3. Proposal Pipeline (Teklif Hunisi)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.widgets.proposalPipeline` |
| **Kullanıcı rolü** | SalesManager, CEO, TenantAdmin, FinanceManager (read-only teklif görünümü) |
| **Veri kaynağı entity** | `CrmProposal`, `CrmProposalItem`, `CrmOpportunity` (stage: Draft → Sent → Approved → Rejected) |
| **Permission** | `Sales.ControlTower.View` + `CRM.Proposal.Read` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Hunide en az 4 aşama (Taslak, Gönderildi, Onay Bekliyor, Onaylandı) ve her aşamada adet + tutar; legend/status renkleri tablo altında; stage tıklanınca filtrelenmiş `Proposals & Quotes` listesi açılır; KPI "Teklife Dönüşüm Oranı" ile tutarlı veri; i18n stage etiketleri 4 dilde |

**API referansı:** `GET /api/control-tower/sales/kpis/proposal-conversion` (KPI) · `GET /api/crm/proposals` (detay liste) · Menü: Proposals & Quotes

---

### 4. Customer Health Score (Müşteri Sağlık Skoru)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.shared.widgets.customerHealthScore` |
| **Kullanıcı rolü** | **Sales CT:** SalesManager, CEO. **CEO CT:** CEO, TenantAdmin (Top 10 müşteri panelinde skor kolonu + aggregate gauge) |
| **Veri kaynağı entity** | `CrmAccount` (hesaplanmış skor projection), `CrmOpportunity` (pipeline sağlığı), `KPIValue` (opsiyonel cache) |
| **Permission** | `Sales.ControlTower.View` (Sales) · `CEO.ControlTower.View` + `CRM.Account.Read` (CEO) |
| **MVP önceliği** | 🟠 **P1 — Sprint 2A** (aggregate MVP; müşteri bazlı detay P1 sonu) |
| **Kabul kriteri** | Skala 0–100 gauge + A–F legend; renk yalnızca semantik token (`status-ok` / `status-warning` / `status-critical`); skor formülü tooltip'te özet metin; CEO stakeholder panelinde Top 10 müşteri health kolonu; Sales'te portföy ortalaması + en düşük 5 müşteri listesi; WCAG: skor `aria-label` ile okunur |

**API referansı:** `GET /api/control-tower/sales/health-scores` · `GET /api/control-tower/ceo/health-scores` · `GET /api/control-tower/ceo/stakeholders`

---

### 5. Customer Risk Score (Müşteri Risk Skoru)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.shared.widgets.customerRiskScore` |
| **Kullanıcı rolü** | **Sales CT:** SalesManager, CEO. **CEO CT:** CEO, TenantAdmin (Müşteri Memnuniyet / risk göstergesi ile hizalı) |
| **Veri kaynağı entity** | `CrmAccount`, `FinanceInvoice` (gecikmiş alacak — logical FK), `QcClaim` (şikâyet — logical FK), `SalesOrder` (limit aşımı) |
| **Permission** | `Sales.ControlTower.View` + `CRM.Account.Read` · CEO için ek: `Finance.Invoice.Read`, `QC.Claim.Read` (detay drill-down) |
| **MVP önceliği** | 🟠 **P1 — Sprint 2A** |
| **Kabul kriteri** | Risk skoru 0–100; yüksek risk eşiği kırmızı badge + Critical Alerts cross-link; en az 3 risk sinyali legend'da (gecikmiş tahsilat, açık şikâyet, limit aşımı); CEO Critical Alerts'te "müşteri eskalasyonu" ile aynı kayıt seti; tıklanınca müşteri detayına gider; PII kart üzerinde maskelenmez (yetkili rol) |

**API referansı:** `GET /api/control-tower/sales/health-scores` · `GET /api/control-tower/ceo/alerts/critical` (eskalasyon cross-ref)

---

### 6. NPS (Net Promoter Score)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.ceo.kpi.nps` |
| **Kullanıcı rolü** | CEO, TenantAdmin, SalesManager (CEO CT KPI); Sales CT Customer Panel'de NPS kolonu (ikincil) |
| **Veri kaynağı entity** | `CrmAccount` (NPS survey alanı / aggregation), `KPIValue` (periyot snapshot) |
| **Permission** | `CEO.ControlTower.View` + `CRM.Account.Read` |
| **MVP önceliği** | 🟡 **P1 — Sprint 2A** (veri yoksa N/A state; anket modülü P2 genişletme) |
| **Kabul kriteri** | KPI kartında −100..+100 veya 0–100 normalize skala (tek skala dokümante); trend ok + "vs geçen çeyrek"; veri yoksa "Anket verisi yok" empty state (sıfır ile karışmaz); Promoter/Passive/Detractor dağılımı tooltip veya expand; i18n sayı formatı locale'e göre |

**API referansı:** `GET /api/control-tower/ceo/kpis/nps`

---

### 7. Open Activities (Açık Aktiviteler)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.widgets.openActivities` |
| **Kullanıcı rolü** | SalesManager, CEO, Employee (yalnızca kendi aktiviteleri — ABAC) |
| **Veri kaynağı entity** | `SalesActivityLog` (scope) / `CrmActivity` (traceability alias — aynı bounded context projection) |
| **Permission** | `Sales.ControlTower.View` + `CRM.Account.Read` · Employee: ABAC `AssignedUserId = current user` |
| **MVP önceliği** | 🟠 **P1 — Sprint 2A** |
| **Kabul kriteri** | Liste widget: max 10 kayıt + "View all"; kolonlar: müşteri, aktivite tipi, vade, sorumlu; geciken aktivite amber/kırmızı status badge; Today's Priorities ile overlap kayıtlar tekilleştirilir; boş liste empty state + "Yeni aktivite" CTA (yazma yetkisi varsa); tarih aralığı filtresine uyar |

**API referansı:** Sales Today's Priorities (`CrmOpportunity`, takip listesi) · Customer Panel (`CrmActivity`) · `GET /api/control-tower/sales/priorities/today`

---

### 8. Proposal Approval Queue (Teklif Onay Kuyruğu)

| Alan | Değer |
|---|---|
| **Kart adı (i18n)** | `pages.sales.widgets.proposalApprovalQueue` |
| **Kullanıcı rolü** | SalesManager (`CRM.Proposal.Approve`), CEO (yüksek tutar eskalasyonu), TenantAdmin |
| **Veri kaynağı entity** | `CrmProposal`, `CrmProposalItem`; workflow: `CrmProposalApproval` |
| **Permission** | `Sales.ControlTower.View` + `CRM.Proposal.Read`; onay aksiyonu: `CRM.Proposal.Approve` |
| **MVP önceliği** | 🔴 **P0 — Sprint 2A** |
| **Kabul kriteri** | Kuyruk widget: onay bekleyen teklifler SLA süresi ile listelenir; her satırda tutar, müşteri, bekleme süresi, eskalasyon seviyesi; SalesManager satır içi "Onayla" / "Reddet" (human-in-the-loop); CEO CT'te yalnızca eşik üstü tutarlar Today's Priorities'te görünür; 24 saat SLA aşımında Critical Alerts tetiklenir; onay sonrası kart anında güncellenir (`CrmProposalApproved` event) |

**API referansı:** `GET /api/control-tower/sales/priorities/today` · `GET /api/crm/proposals?status=pendingApproval` · `POST /api/crm/proposals/{id}/approve`

---

## CEO ↔ Sales Kart Matrisi (Detay)

| Kart | CEO — Birincil widget | Sales — Birincil widget |
|---|---|---|
| Customer Count | KPI: Aktif Müşteri Sayısı | KPI: Yeni Müşteri (Ay) + Customer Panel sayı özeti |
| Active Opportunities | Executive Snapshot (özet cümle) | KPI: Aktif Fırsat Sayısı ve Değeri |
| Proposal Pipeline | — | Pipeline hunisi + Proposals menüsü |
| Customer Health Score | Stakeholder panel kolonu + Health Scores | Health Score widget (portföy) |
| Customer Risk Score | Health Scores + Critical Alerts (eskalasyon) | Health Score widget (risk tarafı) |
| NPS | KPI: NPS | Customer Panel NPS kolonu |
| Open Activities | — | Open Activities list + Priorities |
| Proposal Approval Queue | Today's Priorities (CEO eşik üstü) | Proposal Approval Queue widget |

---

## MVP Sprint Sıralaması (Sprint 2A)

| Sıra | Kart | Gerekçe |
|---|---|---|
| 1 | Customer Count | CRM foundation doğrulama; en basit aggregation |
| 2 | Active Opportunities | Sales KPI çekirdeği |
| 3 | Proposal Pipeline | Hunı görsel kabul kriteri |
| 4 | Proposal Approval Queue | Workflow + permission entegrasyonu |
| 5 | Open Activities | Günlük satış operasyonu |
| 6 | NPS | KPI slot doldurma (CEO 10 KPI) |
| 7 | Customer Health Score | Hesaplanmış skor projection |
| 8 | Customer Risk Score | Cross-context veri (Finance/QC) bağımlı |

---

## İlgili Workflow ve Event'ler

| Kart | Domain Event | Workflow |
|---|---|---|
| Customer Count | `CrmAccountCreated`, `CrmAccountUpdated` | — |
| Active Opportunities | `CrmOpportunityCreated` | — |
| Proposal Pipeline | `CrmProposalCreated`, `CrmProposalApproved` | `CrmProposalApproval` |
| Customer Health / Risk | `CrmAccountUpdated`, `PerformanceKPIValueUpdated` | — |
| NPS | `PerformanceKPIValueUpdated` | — |
| Open Activities | `CrmOpportunityCreated` (aktivite log side-effect) | — |
| Proposal Approval Queue | `CrmProposalCreated`, `CrmProposalApproved` | `CrmProposalApproval` |

---

## Referanslar

- [CONTROL_TOWER_FINAL_SCOPE.md](CONTROL_TOWER_FINAL_SCOPE.md) — §1 CEO, §2 Sales
- [FEATURE_TRACEABILITY_MATRIX.md](FEATURE_TRACEABILITY_MATRIX.md) — §1 CEO, §2 Sales
- [DOMAIN_MODEL.md](../../DOMAIN_MODEL.md) — CRM Entity Matrix
- [SECURITY_AUTHORIZATION.md](../../SECURITY_AUTHORIZATION.md) — Permission Matrix
- [UX_REVIEW.md](UX_REVIEW.md) — KPI / Widget standartları
- [WORKFLOW_ENGINE.md](../../WORKFLOW_ENGINE.md) — `CrmProposalApproval`

---

*Bu doküman ürün UX eşlemesi içerir. Kod içermez.*  
*Güncellemeler Product Board onayı ile yapılır.*
