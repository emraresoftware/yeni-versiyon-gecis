# Agent 1 — Task Report Standard

**Protokol:** [`../MANDATORY_DOCUMENTATION_PROTOCOL.md`](../MANDATORY_DOCUMENTATION_PROTOCOL.md) v1.0  
**Çıktı:** `docs/project-management/reports/TASK_XXX_REPORT.md`

Her Task sonunda **zorunlu**. QA raporu Agent 2'ye aittir.

---

## Şablon (birebir kullan)

```markdown
# Task XXX Report

## Objective

[Task hedefi — 1–3 cümle]

## Scope

[Modül, solution, dosya alanları]

## Files Created

- `path/to/file`

## Files Modified

- `path/to/file`

## Architecture Decisions

[ADR referansı veya kısa karar özeti; yoksa "Yok."]

## Dependencies Added

[NuGet/npm paketleri; yoksa "Yok."]

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet build …` | PASS / FAIL |

## Test Result

| Komut | Sonuç |
|-------|--------|
| `dotnet test …` | PASS / FAIL — N/N geçti |

## Performance Notes

[N+1, async, bellek; yoksa "Yok."]

## Security Notes

[UTC, secret, tenant; yoksa "Yok."]

## Technical Debt

[Yeni TD-xxx maddeleri veya "Yok — bkz. debt/TECHNICAL_DEBT.md"]

## Risks

[Yeni R-xxx maddeleri veya "Yok — bkz. risks/RISK_REGISTER.md"]

## Known Limitations

## Breaking Changes

[Yoksa "Yok."]

## Next Recommended Task
```

---

## Sprint güncelleme

Aynı task commit'inde `docs/project-management/sprints/SPRINT_N.md` güncellenir:

- Tamamlanan task listesi
- İlerleme yüzdesi
- Bloklayıcılar

---

## Agent 1 yapmaz

- QA raporu (`qa/QA_TASK_XXX.md`) — Agent 2
- Architect onayı — Chief Architect
- Hassas veri commit etme
