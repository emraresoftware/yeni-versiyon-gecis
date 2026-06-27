# Development Protocol — Architecture Driven Development

> **Kanonik standart:** [`MANDATORY_DOCUMENTATION_PROTOCOL.md`](MANDATORY_DOCUMENTATION_PROTOCOL.md) v1.1 — tüm ajanlar ve ekip için zorunlu.

Bu dosya ADD task yaşam döngüsünün **kısa özeti**dir.

---

## Teknik hafıza = repository

Sohbet geçmişi referans değildir. Kararlar ADR, Architecture, Reports, QA ve daily log'da kalır.

---

## Task yaşam döngüsü

```text
Kod → Build → Test → Task Report → QA Report → Architect Review → Commit → Sonraki Task
```

**Architect Review olmadan yeni task başlatılamaz.**

---

## Çıktı haritası

| Adım | Sorumlu | Dosya |
|------|---------|-------|
| Task Report | Agent 1 | `reports/TASK_XXX_REPORT.md` |
| QA Review | Agent 2 | `qa/QA_TASK_XXX.md` |
| Architect Review | Chief Architect | `architect/ARCHITECT_REVIEW_TASK_XXX.md` |
| Sprint | Agent 1 | `sprints/SPRINT_N.md` |
| Risk | Agent 2 | `risks/RISK_REGISTER.md` |
| Debt | Agent 1 / Agent 2 | `debt/TECHNICAL_DEBT.md` |
| Daily | Agent 2 | `daily/YYYY-MM-DD.md` |

---

## Şablonlar

- Agent 1: [`reports/TASK_REPORT_STANDARD.md`](reports/TASK_REPORT_STANDARD.md)
- Agent 2: [`qa/QA_REPORT_STANDARD.md`](qa/QA_REPORT_STANDARD.md)

---

## DoD özeti

Kod + build + test + tüm zorunlu dokümanlar + architect onayı + commit — ayrıntı için Mandatory Protocol.
