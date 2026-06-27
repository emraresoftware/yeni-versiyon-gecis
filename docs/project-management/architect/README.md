# Architect Review — Chief Software Architect ONLY

**Zorunlu gate:** Her task sonrası Chief Software Architect (ChatGPT) onayı.

**Dosya:** `ARCHITECT_REVIEW_TASK_XXX.md`  
**Protokol:** [`../MANDATORY_DOCUMENTATION_PROTOCOL.md`](../MANDATORY_DOCUMENTATION_PROTOCOL.md) v1.1

---

## Sahiplik (kritik)

| Rol | Architect Review dosyası |
|-----|--------------------------|
| **Chief Software Architect (ChatGPT)** | ✅ Yazar / onaylar |
| **Koordinatör** | ChatGPT çıktısını **birebir** public mimari repoya ekler |
| **Agent 1** | ❌ Yazamaz — yalnızca beklenen çıktı olarak referans |
| **Agent 2** | ❌ Yazamaz — yalnızca beklenen çıktı olarak referans |

---

## Görev tamamlanma sırası

```text
1. Agent 1  → reports/TASK_XXX_REPORT.md
2. Agent 2  → qa/QA_TASK_XXX.md
3. Chief Architect → architect/ARCHITECT_REVIEW_TASK_XXX.md
```

---

## Girdiler (repository'den okunur)

- `reports/TASK_XXX_REPORT.md`
- `qa/QA_TASK_XXX.md`

---

## Definition of Done

Task, `ARCHITECT_REVIEW_TASK_XXX.md` **Chief Architect tarafından hazırlanmadan** tamamlanmış sayılmaz.

Architect Review tamamlanmadan sonraki task başlatılamaz.
