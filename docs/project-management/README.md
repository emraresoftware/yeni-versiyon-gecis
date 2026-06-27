# Proje Yönetimi — Emare BOS

Repository **teknik hafızadır.** Sohbet geçmişi referans değildir.

## Zorunlu standart

**[`MANDATORY_DOCUMENTATION_PROTOCOL.md`](MANDATORY_DOCUMENTATION_PROTOCOL.md)** v1.1

```text
Agent 1  → TASK_XXX_REPORT.md
Agent 2  → QA_TASK_XXX.md
Chief Architect (ChatGPT) → ARCHITECT_REVIEW_TASK_XXX.md   ← Agent 1/2 YAZMAZ
```

---

## Rol ayrımı

| Rol | Yazar | Yazmaz |
|-----|--------|--------|
| **Agent 1** | Kod, `TASK_XXX_REPORT.md`, sprint | QA, **Architect Review** |
| **Agent 2** | `QA_TASK_XXX.md`, risk, debt, daily | Kod, commit, **Architect Review** |
| **Chief Architect** | `ARCHITECT_REVIEW_TASK_XXX.md` | Uygulama kodu |

---

## Definition of Done

- [ ] Kod, build, test
- [ ] Task Report (Agent 1) + QA Report (Agent 2)
- [ ] Sprint, daily, risk/debt (gerekirse)
- [ ] **Architect Review** — `ARCHITECT_REVIEW_TASK_XXX.md` **Chief Architect tarafından hazırlanmış olmalı**
- [ ] Public mimari repoya raporlar push edildi

Architect Review olmadan yeni task başlatılamaz.

---

## Klasör yapısı

```text
docs/project-management/
├── reports/     TASK_XXX_REPORT.md        (Agent 1)
├── qa/          QA_TASK_XXX.md            (Agent 2)
├── architect/   ARCHITECT_REVIEW_TASK_XXX.md  (Chief Architect ONLY)
├── sprints/     SPRINT_N.md               (Agent 1)
├── risks/       RISK_REGISTER.md
├── debt/        TECHNICAL_DEBT.md
└── daily/       YYYY-MM-DD.md             (Agent 2)
```
