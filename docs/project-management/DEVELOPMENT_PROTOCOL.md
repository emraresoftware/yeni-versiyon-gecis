# Development Protocol — Architecture Driven Development

> **Kanonik standart:** [`MANDATORY_DOCUMENTATION_PROTOCOL.md`](MANDATORY_DOCUMENTATION_PROTOCOL.md) v1.1

---

## Task yaşam döngüsü

```text
Agent 1: Kod → Build → Test → TASK_XXX_REPORT.md
Agent 2: QA_TASK_XXX.md
Chief Architect (ChatGPT): ARCHITECT_REVIEW_TASK_XXX.md   ← Agent 1/2 YAZMAZ
→ Commit / push → Sonraki Task
```

---

## Çıktı haritası

| Adım | Sorumlu | Dosya | Agent 1/2 yazar mı? |
|------|---------|-------|---------------------|
| Task Report | Agent 1 | `reports/TASK_XXX_REPORT.md` | Agent 1 ✅ |
| QA Review | Agent 2 | `qa/QA_TASK_XXX.md` | Agent 2 ✅ |
| Architect Review | **Chief Architect** | `architect/ARCHITECT_REVIEW_TASK_XXX.md` | **❌ Hayır** |
| Sprint | Agent 1 | `sprints/SPRINT_N.md` | Agent 1 ✅ |
| Risk / Debt / Daily | Agent 2 | `risks/`, `debt/`, `daily/` | Agent 2 ✅ |

---

## DoD özeti

Architect Review **zorunlu** — dosya **Chief Software Architect (ChatGPT) tarafından hazırlanmış olmalıdır**. Agent 1 ve Agent 2 yalnızca beklenen çıktı olarak referans gösterir.
