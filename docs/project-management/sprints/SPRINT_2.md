# Sprint 2 — Control Tower (CEO · Sales · Finance)

**Başlangıç:** Sprint 1 platform çekirdeği tamamlandı (Task 001–008A)  
**Son güncelleme:** 2026-06-28  
**İlerleme:** **20%** (CRM Foundation tamamlandı)

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
| **Task 013** | Agent 1 (Dev) | [TASK_013_REPORT.md](../reports/TASK_013_REPORT.md) | Domain + Persistence for CRM Entities | ✅ Tamamlandı |

**Task 009 özeti:** 92 widget traceability satırı (CEO 32 · Sales 29 · Finance 31). Kod yazılmadı.

**Task 013 özeti:** 6 CRM entity'si (`CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal`, `CrmActivity`, `CrmTag`) validation kuralları, domain event'leri, EF Core konfigürasyonları ve testleri tamamlandı.

---

## Backlog (sıradaki)

| # | Task | Ajan | Bağımlılık |
|---|------|------|------------|
| 1 | Chief Architect Review — Task 009 & 013 | Chief Architect | TASK_009_REPORT, TASK_013_REPORT |
| 2 | CRM Application / API Handler (CQRS Command/Query) | Agent 1 | TASK_013 |
| 3 | Sales Order API | Agent 1 | Matris §2 |
| 4 | CEO Control Tower read endpoints | Agent 1 | Matris §1 |
| 5 | Finance Journal / Invoice / Payment API | Agent 1 | Matris §3 |
| 6 | Finance Control Tower read endpoints | Agent 1 | Matris §3 |
| 7 | Control Tower frontend shell (3 kule) | Agent 1 | i18n standard |
| 8 | Permission matrix güncelleme (`*.ControlTower.View`) | Agent 1 | SECURITY_AUTHORIZATION |


---

## Traceability referansı

- Kanonik matris: [`docs/product/FEATURE_TRACEABILITY_MATRIX.md`](../../product/FEATURE_TRACEABILITY_MATRIX.md)
- Ürün kapsamı: [`docs/product/CONTROL_TOWER_FINAL_SCOPE.md`](../../product/CONTROL_TOWER_FINAL_SCOPE.md)

---

## Sprint 1 bağlantısı

Sprint 1 tamamlandı — bkz. [`SPRINT_1.md`](SPRINT_1.md) (Task 001–008A, 61 test yeşil).

---

*Agent 2 Task 009 ile oluşturuldu. Implementasyon task'ları Agent 1 tarafından güncellenir.*
