# QA Review — Task 013A CRM Foundation Hardening

**Task:** 013A — CRM Foundation Hardening  
**Date:** 2026-06-28  
**Reviewer:** Agent 2 (Independent QA)  
**Scope:** Task 013A kabul kriterleri — `CrmProposalItem`, account skorları/segment, permission stub'ları, DDD/event dokümantasyonu, CRM test genişlemesi  
**Method:** `dotnet restore/build/test` + kaynak inceleme + `TASK_013_CRM_FOUNDATION_REPORT.md` çapraz doğrulama  
**Kısıt:** Kod değiştirilmedi. Private repo commit/push yapılmadı.

**Referanslar:** `TASK_013_CRM_FOUNDATION_PLAN.md`, `TASK_013_CRM_FOUNDATION_REPORT.md`, `QA_TASK_013_CRM_FOUNDATION.md`, `EVENT_BUS.md`, `AGENTS.md`, `DOMAIN_MODEL.md`

**Önceki QA:** Task 013 → **CONDITIONAL PASS** (013A gap'leri bu görevin kapsamı)

---

## Final Verdict

# FAIL

Build/test yeşil; kısmi hardening kodda mevcut (segment, skorlar, permission'lar). Ancak Task 013A checklist'inin **çekirdek maddeleri** (`CrmProposalItem`, skor aralık testleri, pre-flight rapor bloğu, event suffix açıklaması) tamamlanmamış veya dokümante edilmemiş.

---

## Build & Test

**PASS**

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | ✅ |
| `dotnet build Emare.sln` | ✅ 0 hata, 1 uyarı (CS1998 — persistence test) |
| `dotnet test Emare.sln` | ✅ **94/94** |

| Proje | Geçen |
|-------|-------|
| `Emare.BuildingBlocks.Tests` | 8 |
| `Emare.Platform.Domain.Tests` | 20 |
| `Emare.Platform.Persistence.Tests` | 19 |
| `Emare.Platform.API.Tests` | 47 |

**Not:** Test sayısı Task 013 ile aynı; 013A için beklenen yeni test metodu **eklenmemiş**.

---

## Kontrol Matrisi (Task 013A Checklist)

| # | Kontrol | Sonuç | Kanıt |
|---|---------|--------|-------|
| 1 | Pre-flight rapora eklenmiş mi? | ❌ | `TASK_013_CRM_FOUNDATION_REPORT.md` — DDD gerekçeleri var; `AGENTS.md` § PRE-FLIGHT checklist (`✓ AGENTS.md`, `✓ ANAYASA.md`, `✓ DOMAIN_MODEL.md` …) **yok**. Ayrı `TASK_013A` raporu yok. |
| 2 | `CrmProposalItem` var mı? | ❌ | `src/Platform/Domain/Entities/Crm/` altında yok; solution grep: Platform'da `CrmProposalItem` / `ProposalItem` tanımı yok |
| 3 | Proposal item child entity olarak modellenmiş mi? | ❌ | `CrmProposal` yalnızca header alanları (`Amount`, `ProposalNumber`); item koleksiyonu / `AddItem` yok |
| 4 | Segment / NPS / risk / health score var mı? | ⚠️ Kısmi | `CrmAccount`: `Segment` (`CrmAccountSegment` A–D), `NpsScore`, `RiskScore`, `HealthScore`; `Create` + `UpdateScores` + `UpdateSegment`. EF config'de explicit property mapping/index yok (convention ile çalışır) |
| 5 | NPS ve score aralıkları test edilmiş mi? | ❌ | `CrmDomainTests.cs` — skor/segment testi yok; `InvalidNpsScore` / `InvalidRiskScore` / `InvalidHealthScore` hiç assert edilmiyor |
| 6 | Permission constants tamam mı? | ✅ | `Permissions.CRM`: 11/11 — `Account`, `Contact`, `Opportunity`, `Proposal` (Read/Write/Approve), `Activity` (Read/Write) |
| 7 | Event suffix açıklaması doğru mu? | ❌ | Raporda event listesi `*DomainEvent` suffix ile; `EVENT_BUS.md` (`CrmAccountCreated`) ↔ outbox `EventType` mapping **açıklanmamış** |
| 8 | DDD aggregate gerekçeleri raporda var mı? | ✅ | `TASK_013_CRM_FOUNDATION_REPORT.md` § "Aggregate & Model Kararları (Gerekçeleriyle)" + logical reference notu |
| 9 | Build/test yeşil mi? | ✅ | 0 hata, 94/94 test |

---

## Kod İncelemesi — Olumlu (kısmi hardening)

### `CrmAccount` skor ve segment validasyonu

```csharp
// Create / UpdateScores — NPS 0–10, Risk & Health 0–100
if (npsScore.HasValue && (npsScore.Value < 0 || npsScore.Value > 10))
    return Result.Failure<CrmAccount>(Error.Validation("CrmAccount.InvalidNpsScore", ...));
```

- `CrmAccountSegment` enum: `A`, `B`, `C`, `D` (`CrmEnums.cs`)
- UTC / Result pattern korunmuş; `TaxNumberVal` alias shadowing çözümü duruyor

### Permission set (plan §8 ile uyumlu)

| Permission | Durum |
|------------|--------|
| `CRM.Account.Read/Write` | ✅ |
| `CRM.Contact.Read/Write` | ✅ |
| `CRM.Opportunity.Read/Write` | ✅ |
| `CRM.Proposal.Read/Write/Approve` | ✅ |
| `CRM.Activity.Read/Write` | ✅ |

---

## Eksikler (013A blocker)

| Madde | Beklenen | Mevcut |
|-------|----------|--------|
| `CrmProposalItem` entity | Domain + EF config + test | Yok |
| Child entity under `CrmProposal` | `ICollection<CrmProposalItem>`, line total hesabı | Yok |
| Skor aralık unit testleri | Theory/InlineData boundary 0, 10, 11, -1 vb. | Yok |
| Segment testi | `UpdateSegment(CrmAccountSegment.A)` | Yok |
| Pre-flight rapor bloğu | Agent 1 report § PRE-FLIGHT | Yok |
| Event suffix dokümantasyonu | `CrmAccountCreated` ↔ `CrmAccountCreatedDomainEvent` tablosu | Yok |
| `TASK_013A` Agent 1 raporu | `docs/project-management/reports/TASK_013A_*.md` | Yok |

---

## Agent 1 Rapor Durumu

| Beklenen | Durum |
|----------|--------|
| `TASK_013A` completion report | ❌ Bulunamadı |
| `TASK_013_CRM_FOUNDATION_REPORT.md` güncellemesi (013A maddeleri) | ⚠️ DDD/event listesi var; NPS/segment/ProposalItem/013A scope **yok** |
| Technical debt: Yok iddiası | ❌ `CrmProposalItem` borcu devam |

---

## PASS İçin Gerekli İşler (Agent 1)

1. **`CrmProposalItem`** — child entity (`CrmProposalId` logical FK, `LineTotal` hesabı), EF config, domain test.
2. **`CrmProposal`** — item koleksiyonu ve aggregate sınırı (item yalnızca proposal üzerinden).
3. **Skor/segment testleri** — NPS 0–10, risk/health 0–100 sınır; geçersiz değerler `Result.Failure`.
4. **Pre-flight bloğu** — Agent raporuna `AGENTS.md` checklist ekle.
5. **Event suffix tablosu** — raporda `EVENT_BUS.md` adı ↔ `*DomainEvent` ↔ outbox `EventType` mapping.
6. **`TASK_013A` raporu** — scope, dosya listesi, build/test sonucu.
7. (Opsiyonel) `CrmAccountConfiguration` — `Segment` / skor kolonları ve CEO KPI index'i.

---

## QA Metadata

| Alan | Değer |
|------|--------|
| Verdict | **FAIL** |
| Private repo | `/Users/emre/Elyafgroup` |
| Public repo | `/Users/emre/yeni-versiyon-gecis` (`gece-otonom`) |
| Kod değişikliği | Yok (QA only) |
