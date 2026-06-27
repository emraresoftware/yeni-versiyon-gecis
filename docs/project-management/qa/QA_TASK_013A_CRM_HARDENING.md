# QA Review — Task 013A CRM Foundation Hardening

**Task:** 013A — CRM Foundation Hardening (Fix pass)  
**Date:** 2026-06-28  
**Reviewer:** Agent 2 (Independent QA)  
**Review pass:** 2 (013A fix sonrası yeniden koşu)  
**Scope:** Task 013A kabul kriterleri — `CrmProposalItem`, account skorları/segment, permission stub'ları, pre-flight/event/DDD dokümantasyonu, CRM test genişlemesi  
**Method:** `dotnet restore/build/test` + kaynak inceleme + `TASK_013A_CRM_HARDENING_REPORT.md` çapraz doğrulama  
**Kısıt:** Kod değiştirilmedi. Private repo commit/push yapılmadı.

**Referanslar:** `TASK_013A_CRM_HARDENING_REPORT.md`, `TASK_013_CRM_FOUNDATION_PLAN.md`, `EVENT_BUS.md`, `AGENTS.md`

**Önceki QA (Pass 1):** **FAIL** — `CrmProposalItem`, skor testleri ve Agent raporu eksikti.

---

## Final Verdict

# CONDITIONAL PASS

Task 013A fix kapsamı büyük ölçüde tamamlandı: build/test **104/104**, `CrmProposalItem`, skor/segment validasyon testleri, permission stub'ları ve Agent raporu mevcut. **Tek kalan gap:** Agent raporundaki event suffix / outbox açıklaması runtime kodla **tam uyumlu değil** (aşağıda).

---

## Build & Test

**PASS**

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | ✅ |
| `dotnet build Emare.sln` | ✅ **0 hata**, 5 uyarı (CA1000 ×4, CS1998 ×1) |
| `dotnet test Emare.sln` | ✅ **104/104** |

| Proje | Geçen | Δ (Pass 1) |
|-------|-------|------------|
| `Emare.BuildingBlocks.Tests` | 8 | — |
| `Emare.Platform.Domain.Tests` | 28 | +8 |
| `Emare.Platform.Persistence.Tests` | 21 | +2 |
| `Emare.Platform.API.Tests` | 47 | — |
| **Toplam** | **104** | **+10** |

**Agent rapor düzeltmesi:** Rapor `0 uyarı` iddia ediyor; QA koşusunda **5 uyarı** var (kritik değil).

---

## Kontrol Matrisi (Task 013A Checklist)

| # | Kontrol | Sonuç | Kanıt |
|---|---------|--------|-------|
| 1 | `TASK_013A_CRM_HARDENING_REPORT.md` var mı? | ✅ | `docs/project-management/reports/TASK_013A_CRM_HARDENING_REPORT.md` |
| 2 | Pre-flight checklist raporda var mı? | ✅ | § Pre-flight Checklist — AGENTS, ANAYASA, DOMAIN_MODEL, EVENT_BUS, SECURITY_AUTHORIZATION |
| 3 | `CrmProposalItem` var mı? | ✅ | `src/Platform/Domain/Entities/Crm/CrmProposalItem.cs`, `CrmProposalItemConfiguration.cs`, `EmareDbContext.CrmProposalItems` |
| 4 | Child entity olarak modellenmiş mi? | ✅ | `CrmProposal.Items`, `AddItem` / `RemoveItem` (Draft only), `RecalculateAmount()`; raporda DDD gerekçesi var |
| 5 | `CrmProposalItem` EF indexes doğru mu? | ✅ | Config: `TenantId`, `CrmProposalId`, `{ TenantId, CrmProposalId }`; `EFModel_Indexes_ShouldBeRegisteredCorrectly` assert ediyor |
| 6 | Proposal item line total testleri var mı? | ✅ | Domain: `CrmProposalItem_ShouldCalculateLineTotalCorrectly_AndRecalculateProposalAmount`; Persistence: `CrmProposalWithItems_CanBeSavedAndRetrieved_AndRecalculatesAmount` |
| 7 | NPS / Risk / Health aralık testleri var mı? | ✅ | `CrmAccount_InvalidNpsScore_ShouldFail` (-1, 11); `InvalidRiskScore` / `InvalidHealthScore` (-1, 101); Create + UpdateScores boundary |
| 8 | Event suffix açıklaması raporda var mı? | ⚠️ | § Event Suffix Açıklaması **mevcut**; ancak outbox runtime iddiası kodla **uyumsuz** (aşağı) |
| 9 | Build/test 104/104 mü? | ✅ | QA bağımsız koşu doğruladı |
| 10 | Kodda `DateTime.Now` / `throw new Exception`? | ✅ | `src/Platform/**/Crm/**` production kodunda yok; yalnızca domain test UTC dönüşümü için bilinçli `DateTime.Now` kullanıyor |

---

## Doğrulanan Uygulama Detayları

### `CrmProposalItem` + aggregate davranışı

- Alanlar: `CrmProposalId`, `Description`, `Quantity`, `UnitPrice`, `Currency`, `LineTotal` (computed: `Quantity * UnitPrice`)
- `CrmProposal.AddItem` → item oluşturur, `_items`'a ekler, `Amount` yeniden hesaplar
- Draft dışı durumda modify engeli: `CrmProposal.CannotModify`

### Skor ve segment

- `CrmAccount`: `Segment` (`CrmAccountSegment` A–D), `NpsScore` (0–10), `RiskScore` / `HealthScore` (0–100)
- `UpdateSegment`, `UpdateScores` metotları mevcut
- Persistence: skor/segment save+reload testi (`CrmProposalWithItems_*`)

### Permission constants

- 11/11 CRM permission — persistence test `PermissionConstants_ShouldBeDefinedCorrectly`

---

## Event Suffix — Rapordaki Açıklama vs Runtime

Agent raporu:

> Outbox Payload üzerinde `CrmAccountCreated` olarak serileştirilir.

**QA doğrulaması (`OutboxWriter.cs`):**

```csharp
var eventType = domainEvent.GetType().Name;  // → "CrmAccountCreatedDomainEvent"
var payload = JsonSerializer.Serialize(domainEvent, domainEvent.GetType());
```

Outbox testi: `m.EventType == nameof(CrmAccountCreatedDomainEvent)` — **DomainEvent suffix korunuyor**.

| Katman | Agent rapor iddiası | QA gerçek |
|--------|---------------------|-----------|
| C# tip adı | `CrmAccountCreatedDomainEvent` | ✅ |
| Outbox `EventType` | `CrmAccountCreated` | ❌ → `CrmAccountCreatedDomainEvent` |
| `EVENT_BUS.md` canonical ad | `CrmAccountCreated` | Mapping/strip henüz uygulanmamış |

**Sonuç:** Açıklama **var** ama outbox runtime için **kısmen yanlış**. İleride relay/worker'da suffix strip veya mapping tablosu gerekir; dokümantasyon buna göre güncellenmeli.

---

## Küçük Notlar (PASS engeli değil)

| Not | Detay |
|-----|--------|
| `CrmProposalItem` inheritance | `BaseAuditableEntity` / `AggregateRoot` — child entity pratiği `AddItem` ile sağlanıyor; ayrı DbSet var (Platform convention) |
| Plan §5.5 alanları | Plan: `ProductCode`, `DiscountRate`, `TaxRate`; uygulama: sadeleştirilmiş `Description` + `LineTotal` — Sprint 2A foundation için kabul edilebilir |
| Build uyarıları | Agent rapor `0 uyarı`; gerçek: 5 (CA1000, CS1998) |

---

## Pass 1 → Pass 2 Karşılaştırma

| Madde | Pass 1 | Pass 2 |
|-------|--------|--------|
| Verdict | FAIL | **CONDITIONAL PASS** |
| Test | 94/94 | **104/104** |
| `CrmProposalItem` | ❌ | ✅ |
| Skor boundary testleri | ❌ | ✅ |
| Agent 013A raporu | ❌ | ✅ |
| Pre-flight checklist | ❌ | ✅ |
| Event suffix doc | ❌ | ⚠️ (var, runtime iddiası hatalı) |

---

## PASS İçin Kalan (opsiyonel / Task 014+)

1. Outbox `EventType` → `EVENT_BUS.md` canonical ad mapping (strip `DomainEvent` veya explicit mapper).
2. Agent raporundaki event suffix bölümünü runtime ile hizala.
3. (Opsiyonel) `CrmProposalItem` plan alanları (`ProductCode`, discount/tax) genişletmesi.

---

## QA Metadata

| Alan | Değer |
|------|--------|
| Pass 1 verdict | FAIL |
| Pass 2 verdict | **CONDITIONAL PASS** |
| Private repo | `/Users/emre/Elyafgroup` |
| Public repo | `/Users/emre/yeni-versiyon-gecis` (`gece-otonom`) |
| Kod değişikliği | Yok (QA only) |
