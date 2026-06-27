# Proje Yönetimi — Emare BOS

Repository **teknik hafızadır.** Sohbet geçmişi referans değildir.

## Zorunlu standart (v1.0)

**[`MANDATORY_DOCUMENTATION_PROTOCOL.md`](MANDATORY_DOCUMENTATION_PROTOCOL.md)**

Tüm Agent 1, Agent 2 ve Architect işleri bu protokole uyar. Task, zorunlu dokümanlar commit edilmeden tamamlanmış sayılmaz.

```text
Kod → Build → Test → Task Report → QA Report → Architect Review → Commit → Sonraki Task
```

---

## Rol ayrımı

| Agent | Yapar | Yapmaz |
|-------|--------|--------|
| **Agent 1** | Kod, build, test, `TASK_XXX_REPORT.md`, sprint güncelleme | QA raporu |
| **Agent 2** | `QA_TASK_XXX.md`, risk, debt, daily | Kod, commit |
| **Chief Architect** | `ARCH_REVIEW_TASK_XXX.md`, ADR | Uygulama kodu (varsayılan) |

---

## Klasör yapısı

```text
docs/project-management/
├── MANDATORY_DOCUMENTATION_PROTOCOL.md   ← zorunlu v1.0
├── DEVELOPMENT_PROTOCOL.md
├── reports/          TASK_XXX_REPORT.md
├── qa/               QA_TASK_XXX.md
├── architect/        ARCH_REVIEW_TASK_XXX.md
├── risks/            RISK_REGISTER.md
├── debt/             TECHNICAL_DEBT.md
├── sprints/          SPRINT_N.md
├── tasks/
└── daily/            YYYY-MM-DD.md
```

---

## Şablonlar

| Rol | Şablon |
|-----|--------|
| Agent 1 | [`reports/TASK_REPORT_STANDARD.md`](reports/TASK_REPORT_STANDARD.md) |
| Agent 2 | [`qa/QA_REPORT_STANDARD.md`](qa/QA_REPORT_STANDARD.md) |

---

## Definition of Done

- [ ] Kod, build, test
- [ ] Task Report + QA Report
- [ ] Sprint güncellendi
- [ ] Risk / debt (gerekirse)
- [ ] Daily log
- [ ] Architect Review
- [ ] Hepsi commit'te

---

## Kurallar

- Hassas veri yazma.
- Eski konum `.cursor/günlük/` → yönlendirme; kanonik `daily/` burada.

## İlgili

- `Emare.sln` — Emare BOS
- `Yeni versiyon geçiş/ANAYASA.md` — kod kalitesi
- `emare-dashboard/docs/adr/` — ADR
