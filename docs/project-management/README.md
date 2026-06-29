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

| Ajan | Private Repo | Public Repo |
|------|--------------|-------------|
| Agent 1 | ✅ Kod + Commit | ✅ Rapor |
| Agent 2 | ❌ | ✅ QA |
| Agent 3 | ❌ | ✅ Product Docs |
| Agent 4 | ❌ | ✅ Security Docs |
| Agent 5 | ❌ | ✅ UX Docs |
| **Agent 6** | 👀 Sadece Okur | ✅ Legacy Dokümanları (`docs/legacy/`) |
| Chief Architect | ❌ | ✅ Architect Review |

Detay: public repo `docs/legacy/README.md` v2.1

---

## Rol ayrımı (yazar / yazmaz)

| Rol | Yazar | Yazmaz |
|-----|--------|--------|
| **Agent 1** | Kod, `TASK_XXX_REPORT.md`, sprint | QA, **Architect Review** |
| **Agent 2** | `QA_TASK_XXX.md`, risk, debt, daily | Kod, commit, **Architect Review** |
| **Agent 6** | Public: `docs/legacy/` + TASK raporu (👀 private sadece okur) | Kod, private commit, migration, QA, Architect Review |
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
├── daily/       YYYY-MM-DD.md             (Agent 2)
└── legacy/      arşiv (TASK 021) — kanonik: public repo docs/legacy/
```

Agent 6 charter (kanonik): **public repo** `docs/legacy/README.md` · Private arşiv: [`legacy/README.md`](legacy/README.md)
