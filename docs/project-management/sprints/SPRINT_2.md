# Sprint 2 — Control Tower (CEO · Sales · Finance)

**Başlangıç:** Sprint 1 platform çekirdeği tamamlandı (Task 001–008A)  
**Son güncelleme:** 2026-07-01  
**İlerleme:** **61%** (CEO, QC ve Logistics V2 entegrasyonu tamamlandı)

---

## Hedef

Elyaf Control Tower ekranlarının Sprint 2A (CRM + Sales) ve Sprint 2B (Finance) kapsamında backend + frontend implementasyonu.  
Sprint başlamadan önce ürün izlenebilirlik matrisi zorunludur (`CONTROL_TOWER_FINAL_SCOPE.md` § Sprint Hazırlık Notu).

---

## Sprint 2 alt fazları

| Faz | Kapsam | Control Tower | Backend modüller |
|-----|--------|---------------|------------------|
| **2A** | CRM + Sales | CEO, Sales | CRMModule, SalesModule, ReportingModule |
| **2B** | Finance + Cash | Finance | FinanceModule, BankModule, BudgetModule |

---

## Tamamlanan tasklar

| Task | Ajan | Rapor | Çıktı | Durum |
|------|------|-------|-------|-------|
| **Task 009** | Agent 2 (Product) | [TASK_009_REPORT.md](../reports/TASK_009_REPORT.md) | [FEATURE_TRACEABILITY_MATRIX.md](../../product/FEATURE_TRACEABILITY_MATRIX.md) | ✅ Tamamlandı |
| **Task 013** | Agent 1 (Dev) | [TASK_013_CRM_FOUNDATION_REPORT.md](../reports/TASK_013_CRM_FOUNDATION_REPORT.md) | Domain + Persistence for CRM Entities | ✅ Tamamlandı |
| **Task 013A** | Agent 1 (Dev) | [TASK_013A_CRM_HARDENING_REPORT.md](../reports/TASK_013A_CRM_HARDENING_REPORT.md) | CRM Domain + Persistence Hardening | ✅ Tamamlandı |
| **Task 013A Security** | Agent 4 (Sec) | [TASK_013A_REPORT.md](../reports/TASK_013A_REPORT.md) | [CRM_SECURITY_REVIEW_TASK_013A.md](../security/CRM_SECURITY_REVIEW_TASK_013A.md) | ✅ Tamamlandı |
| **Task 014** | Agent 1 (Dev) | [TASK_014_REPORT.md](../reports/TASK_014_REPORT.md) | CRM Application Layer (CQRS Commands, Queries, Handlers, DTOs, Validators) | ✅ Tamamlandı |
| **Task 015** | Agent 1 (Dev) | [TASK_015_CRM_API_REPORT.md](../reports/TASK_015_CRM_API_REPORT.md) | CRM REST API Endpoints (Controllers + Integration Tests) | ✅ Tamamlandı |
| **Task 015 QA** | Agent 2 (QA) | [QA_TASK_015.md](../qa/QA_TASK_015.md) | Quality Assurance Review for CRM API layer | ✅ Tamamlandı |
| **Task 025** | Agent 1 (Dev) | [TASK_025_REPORT.md](../reports/TASK_025_REPORT.md) | Nginx Routing Hotfix for asistan.emarecloud.tr | ✅ Tamamlandı |
| **Task 026** | Agent 1 (Dev) | [TASK_026_REPORT.md](../reports/TASK_026_REPORT.md) | Dynamic Tenant Resolution Hotfix for SuperAdmin & Anonymous requests | ✅ Tamamlandı |
| **Task 027** | Agent 1 (Dev) | [TASK_027_REPORT.md](../reports/TASK_027_REPORT.md) | Manual IMAP Sync History Trigger & Date Sync | ✅ Tamamlandı |
| **Task 028** | Agent 1 (Dev) | [TASK_028_REPORT.md](../reports/TASK_028_REPORT.md) | Elyaf V2 Strategic Rollout (A1, A6, A7 Modules) | ✅ Tamamlandı |
| **Task 031** | Agent 1 (Dev) | [TASK_031_REPORT.md](../reports/TASK_031_REPORT.md) | Visual Scenario Graph JSON Repair,Greeting Text Injection Bypass & Demo Deletion | ✅ Tamamlandı |
| **Task 032** | Agent 1 (Dev) | [TASK_032_REPORT.md](../reports/TASK_032_REPORT.md) | SuperAdmin Dashboard 403 Console Errors & Recharts Warnings Hotfix | ✅ Tamamlandı |
| **Task 033** | Agent 1 (Dev) | [TASK_033_REPORT.md](../reports/TASK_033_REPORT.md) | Next.js TypeError & 401 Robustness Mappings Hotfix | ✅ Tamamlandı |
| **Task 034** | Agent 1 (Dev) | [TASK_034_REPORT.md](../reports/TASK_034_REPORT.md) | CRM Redirect Loop and SuperAdmin Dashboard Access | ✅ Tamamlandı |
| **Task 035** | Agent 1 (Dev) | [TASK_035_REPORT.md](../reports/TASK_035_REPORT.md) | Voice Bridge Barge-in & Echo Suppression Optimization | ✅ Tamamlandı |
| **Task 036** | Agent 1 (Dev) | [TASK_036_REPORT.md](../reports/TASK_036_REPORT.md) | Gemini Live Playout Starvation & Supervisor Bypass | ✅ Tamamlandı |

**Task 036 özeti:** Gemini Live telefon görüşmelerinde playout underflow durumlarında oluşan 6.25 Hz robotik ses chattering'i çözüldü (consecutive underflows model). Canlı ses kanalına yapılan Supervisor/Teacher enjeksiyonları bypass edilerek barge-in çakışmaları ve token bloat'u giderildi.

**Task 035 özeti:** Görüşme esnasındaki yankı kaynaklı asistan kesilmelerini (self-interruption) ve lag problemlerini çözmek için barge-in süresi 40ms'den 240ms'ye çıkarıldı. Asistan konuşurken mikrofona yansıyan ses yankısının Gemini VAD motorunu tetiklememesi için sessizlik filtreli echo suppression entegre edildi.

**Task 034 özeti:** Control Tower ekranındaki "CRM'e Dön" butonunun oluşturduğu yönlendirme döngüsü giderildi. Platform yöneticilerinin (`SuperAdmin`/`Admin`) Elyaf Control Tower kule verilerine erişebilmesi için GetTenantId() ve RequireTenant() metotlarındaki tenant kısıtlamaları platform yöneticilerine özel olarak esnetildi.

**Task 033 özeti:** Oturum geçişlerinde (impersonation) ve token yenileme anlarında `tenant-admin` ve `home` sayfalarının çökmesini (TypeError) engellemek için dizi eşleme kontrollerine safety wrapper'lar (`?? []`) ekledik. `inboundEmailsData` veri modelindeki API uyuşmazlığı giderildi.

**Task 032 özeti:** SuperAdmin panelindeki 403 Forbidden ve 500 hatalarını (özellikle ToDictionaryAsync mükerrer key sorunu ve eksik tenantId durumları) ve Recharts ResponsiveContainer genişlik/yükseklik uyarılarını minWidth={0} ekleyerek giderdik.

**Task 031 özeti:** Görsel senaryo akışı JSON onarımı, karşılama metni enjeksiyonu, özel tasarım karşılama metinlerinde otomatik merhaba/isim bypass'ı ve Demo Ajanı paneline özel akış silme entegrasyonu tamamlandı.

**Task 028 özeti:** Implemented V2 strategic rollout for CEO (A1 Decisions Log), Quality Control (A6 Claims & Test Logs), and Logistics (A7 Warehouse stock levels & double-approval transfer workflow) across backend API and frontend Next.js layers.

**Task 027 özeti:** Implemented manual IMAP email synchronization from a specific start date, adding `ImapSyncStartDate` property, updating `ImapPollerBackgroundService`, and exposing a `POST /api/v1/mail-accounts/{id}/sync-history` endpoint. Also resolved database insert crashes for long emails by truncating ticket descriptions to 5000 characters.

**Task 026 özeti:** Resolved blocking 403 Forbidden errors on WhatsApp accounts retrieval for SuperAdmin users by adding dynamic Host-to-Tenant resolution with memory caching in CurrentUserService.

**Task 025 özeti:** Nginx routing and deployment hotfix implemented to resolve 404/403 session and API errors on the `asistan.emarecloud.tr` tenant domain.

**Task 009 özeti:** 92 widget traceability satırı (CEO 32 · Sales 29 · Finance 31). Kod yazılmadı.

**Task 013 özeti:** 6 CRM entity'si (`CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal`, `CrmActivity`, `CrmTag`) validation kuralları, domain event'leri, EF Core konfigürasyonları ve testleri tamamlandı.

**Task 013A özeti:** `CrmProposalItem` child entity'si eklendi. `CrmAccount` NPS/Segment/Risk/Health alanları ve kısıtlamaları uygulandı. CRM izin listesi tamamlandı. 104/104 test başarılı.

**Task 014 özeti:** CRM modülü için CQRS Command, Query, DTO, Validator yapıları ve 117 entegrasyon testinin tamamı yeşil olarak tamamlandı.

**Task 015 özeti:** CRM REST API endpoints and mock-authenticated integration tests implemented successfully under `CrmController` and `CrmControllerTests`. High coverage and strict security permission filters applied.

---

## Backlog (sıradaki)

| # | Task | Ajan | Bağımlılık |
|---|------|------|------------|
| 1 | Chief Architect Review — Task 009, 013 & 013A | Chief Architect | TASK_009_REPORT, TASK_013_CRM_FOUNDATION_REPORT, TASK_013A_CRM_HARDENING_REPORT |
| 2 | Sales Order API | Agent 1 | Matris §2 |
| 3 | CEO Control Tower read endpoints | Agent 1 | Matris §1 |
| 4 | Finance Journal / Invoice / Payment API | Agent 1 | Matris §3 |
| 5 | Finance Control Tower read endpoints | Agent 1 | Matris §3 |
| 6 | Control Tower frontend shell (3 kule) | Agent 1 | i18n standard |
| 7 | Permission matrix güncelleme (`*.ControlTower.View`) | Agent 1 | SECURITY_AUTHORIZATION |


---

## Traceability referansı

- Kanonik matris: [`docs/product/FEATURE_TRACEABILITY_MATRIX.md`](../../product/FEATURE_TRACEABILITY_MATRIX.md)
- Ürün kapsamı: [`docs/product/CONTROL_TOWER_FINAL_SCOPE.md`](../../product/CONTROL_TOWER_FINAL_SCOPE.md)

---

## Sprint 1 bağlantısı

Sprint 1 tamamlandı — bkz. [`SPRINT_1.md`](SPRINT_1.md) (Task 001–008A, 61 test yeşil).

---

*Agent 2 Task 009 ile oluşturuldu. Implementasyon task'ları Agent 1 tarafından güncellenir.*
