# Agent 2 — QA Report Standard

**Protokol:** [`../MANDATORY_DOCUMENTATION_PROTOCOL.md`](../MANDATORY_DOCUMENTATION_PROTOCOL.md) v1.0  
**Çıktı:** `docs/project-management/qa/QA_TASK_XXX.md`

**Rol:** Sadece kalite kontrol — kod yazma, kod commit etme, feature geliştirme yok.

---

## Zorunlu komutlar (Emare BOS)

```bash
dotnet restore Emare.sln
dotnet build Emare.sln
dotnet test Emare.sln
```

Task kapsamında EmareTicket / `web/` varsa ilgili build/test/lint de çalıştırılır.

---

## Şablon (birebir kullan)

```markdown
# QA Review

**Task:** XXX  
**Date:** YYYY-MM-DD  
**Reviewer:** Agent 2  
**Scope:** [Modül / yollar]  
**Kısıt:** Kod değiştirilmedi, commit yapılmadı.

---

## Build

PASS / FAIL

---

## Tests

PASS / FAIL

---

## Clean Architecture

* Domain bağımsız mı?
* Infrastructure sızıntısı var mı?
* Controller DbContext kullanıyor mu?

---

## DDD Compliance

* AggregateRoot / entity sınırları
* Domain event kullanımı
* Repository yalnızca aggregate kökü
* Application vs Domain ayrımı

---

## Security

* DateTime.Now
* throw new Exception
* Hardcoded Secret
* Hardcoded Connection String
* Hardcoded Tenant

---

## Performance

* N+1
* LINQ
* Async
* CancellationToken
* Memory

---

## Persistence

* Soft Delete
* Audit
* Tenant
* Concurrency

---

## API

* Middleware
* Validation
* ProblemDetails
* Swagger
* Health

---

## Test Coverage

Yeterli mi?

Eksik mi?

---

## Critical Issues

Listele

---

## Suggestions

Listele

---

## Final Verdict

PASS / CONDITIONAL PASS / FAIL
```

---

## Verdict

| Sonuç | Sonraki adım |
|-------|----------------|
| **PASS** | Chief Architect Review beklenir (`ARCHITECT_REVIEW_TASK_XXX.md` — Agent 2 yazmaz) |
| **CONDITIONAL PASS** | Açık maddeler kayıtlı; Chief Architect Review |
| **FAIL** | Agent 1 hotfix; yeni task yok |

---

## Agent 2 yapmaz

- Kod yazma / değiştirme
- Kod commit etme (private repo)
- Feature geliştirme
- **`ARCHITECT_REVIEW_TASK_XXX.md` yazmak/doldurmak** — yalnızca Chief Software Architect (ChatGPT); Agent 2 yalnızca beklenen çıktı olarak referans gösterir

---

## Agent 2 ayrıca günceller (gerekirse)

- `risks/RISK_REGISTER.md`
- `debt/TECHNICAL_DEBT.md`
- `daily/YYYY-MM-DD.md`

---

## Legacy raporlar

Eski formatta; yeni task'larda bu şablon zorunlu:

- `QA_TASK_001_003.md`, `QA_TASK_004_PERSISTENCE.md`, `QA_TASK_005_COMPOSITION_ROOT.md`
- `QA_HOTFIX_TASK_004A_TENANT_FILTER.md`
