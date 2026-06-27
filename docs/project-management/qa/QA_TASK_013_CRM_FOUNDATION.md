# QA Review — Task 013 CRM Foundation

**Task:** 013 — CRM Foundation (Sprint 2A)  
**Date:** 2026-06-28  
**Reviewer:** Agent 2 (Independent QA)  
**Scope:** Emare BOS Platform — `src/Platform/Domain/Entities/Crm/*`, `CrmEvents.cs`, `CrmEnums.cs`, `Persistence/Configurations/Crm*.cs`, `EmareDbContext` CRM DbSets, CRM unit/integration tests  
**Method:** Pre-flight docs + `dotnet restore/build/test` + kaynak inceleme + Agent 1 `TASK_013_REPORT.md` çapraz doğrulama  
**Kısıt:** Kod değiştirilmedi. Private repo commit/push yapılmadı.

**Referanslar:** `TASK_013_CRM_FOUNDATION_PLAN.md`, `TASK_013_REPORT.md`, `DOMAIN_MODEL.md`, `EVENT_BUS.md`, `SECURITY_AUTHORIZATION.md`, `FEATURE_TRACEABILITY_MATRIX.md`, `ANAYASA.md`, `AGENTS.md`

---

## Final Verdict

# FAIL

Solution derlenmiyor. Agent 1 raporu (`98/98 test`, `0 hata`) mevcut kod tabanıyla **doğrulanamıyor**. Domain, Persistence konfigürasyonları ve testler **aynı model üzerinde hizalanmamış**; CRM testleri derlenemiyor ve çalıştırılamıyor.

---

## Pre-Flight

| Doküman | Durum | Not |
|---------|--------|-----|
| `AGENTS.md` | ⚠️ | QA tarafında okundu. Agent 1 `TASK_013_REPORT.md` içinde pre-flight onayı **yok**. |
| `ANAYASA.md` | ⚠️ | CRM kodunda `DateTime.Now` / `throw new Exception` yok; ancak build kırık olduğu için tam uyum doğrulanamaz. |
| `DOMAIN_MODEL.md` | ⚠️ | Plan §5 entity şeması ile uygulama kısmen uyumsuz (aşağıda). |
| `EVENT_BUS.md` | ❌ | Event adlandırma ve eksik event tipleri uyumsuz. |
| `SECURITY_AUTHORIZATION.md` | ❌ | Plan §8 permission set'inin %27'si tanımlı. |

**Sonuç:** Pre-flight dokümantasyonu Agent 1 çıktısında eksik; kod tabanı pre-flight sonrası tutarlı teslim edilmemiş.

---

## Build & Test (Doğrulama)

**FAIL**

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | ✅ Başarılı |
| `dotnet build Emare.sln` | ❌ **9 hata** — `Emare.Platform.Domain` derlenemiyor |
| `dotnet test Emare.sln` | ❌ Domain/Persistence test projeleri derlenemediği için CRM testleri **çalışmadı** |

### Derleme hataları (özet)

`CrmAccount.cs` — property adı `TaxNumber`, value object sınıfı `TaxNumber` ile **gölgeleme (shadowing)**:

```
CS0120: 'CrmAccount.TaxNumber' statik olmayan alanı ... nesne başvurusu gerekiyor
CS1501: 'Create' yöntemi için hiçbir tekrar yükleme 1 bağımsız değişken almaz
CS1061: 'string' bir 'IsFailure' tanımı içermiyor  (TaxNumber.Create çözümlenemiyor)
```

Satır 87 ve 146 (`Create` / `Update` içinde `TaxNumber.Create(...)`).

### Test sonucu (gerçek)

| Proje | Durum | Not |
|-------|--------|-----|
| `Emare.BuildingBlocks.Tests` | ✅ 8/8 | CRM dışı |
| `Emare.Platform.Domain.Tests` | ❌ Derlenemedi | 18 CRM testi eski entity API'sine bağlı |
| `Emare.Platform.Persistence.Tests` | ❌ Derlenemedi | 5 CRM testi eski entity API'sine bağlı |
| `Emare.Platform.API.Tests` | ✅ 47/47 | Önceki build artifact ile `--no-build` veya kısmi koşu |

**Agent 1 iddiası:** 98/98 passed — **QA tarafından reddedildi** (2026-06-28 bağımsız koşu).

---

## Kontrol Matrisi

| # | Kontrol | Sonuç | Kanıt |
|---|---------|--------|-------|
| 1 | Pre-flight yapılmış mı? | ❌ | `TASK_013_REPORT.md` pre-flight checklist içermiyor |
| 2 | ANAYASA ihlali | ⚠️ | CRM path'te `DateTime.Now` / `throw new Exception` yok; `DateTime.SpecifyKind` UTC düzeltmesi var (`CrmActivity`, `CrmProposal`, `CrmOpportunity`). Build kırık. |
| 3 | DDD aggregate sınırları | ❌ | Plan: `CrmContact` → `CrmAccount` alt entity; `CrmProposalItem` → `CrmProposal` alt entity. Uygulama: **6 tipin tamamı** `BaseAuditableEntity` / `AggregateRoot`. `CrmProposalItem` **yok**. |
| 4 | TenantId her CRM entity'de | ✅ (tasarım) | 6 entity `Create(..., Guid tenantId, ...)` + `Guid.Empty` guard. Build geçse doğrulanabilir. |
| 5 | Soft delete / audit / concurrency | ⚠️ | `BaseAuditableEntity` → `ISoftDelete`, `IAuditable`, `IConcurrencyTracked`. EF config'lerde `RowVersion` + SQLite/Postgres ayrımı mevcut. Persistence testleri **derlenmediği** için runtime doğrulama yapılamadı. |
| 6 | Event isimleri `EVENT_BUS.md` | ❌ | Spec: `CrmAccountCreated`, `CrmProposalApproved`. Kod: `CrmAccountCreatedDomainEvent`, `*DomainEvent` suffix. `CrmContactCreated`, `CrmTagCreated`, `CrmProposalStatusChanged` **tanımlı değil**; testler bunları bekliyor, entity'ler farklı davranıyor. |
| 7 | Permission / Control Tower | ❌ | Plan §8: 11 permission. Kod: yalnızca `CRM.Account.Read`, `CRM.Account.Write`, `CRM.Proposal.Approve`. API/CQRS yok → Control Tower widget'ları beslenemez. |
| 8 | EF indexes | ⚠️ Kısmi | Güncel config'ler tenant bileşik index içeriyor (`TenantId+AccountCode` unique, `TenantId+ProposalNumber` unique vb.). Testler çalışmadığı için index davranışı doğrulanmadı. |
| 9 | Cross-context FK | ✅ | Güncel EF config'ler navigation `HasForeignKey` kullanmıyor; yalnızca `CrmAccountId` / `CrmOpportunityId` logical GUID + index. Cross-bounded-context FK yok. |
| 10 | `DateTime.Now` | ✅ | `src/Platform/**/Crm/**` ve CRM config/test path'lerinde bulunamadı |
| 11 | `throw new Exception` | ✅ | CRM Platform kodunda bulunamadı |
| 12 | Testler anlamlı mı? | ❌ | Testler **eski domain modeline** yazılmış; mevcut entity'lerle uyumsuz — derlenemiyor, anlamlılık değerlendirilemez |

---

## Domain ↔ Persistence ↔ Test Uyumsuzlukları

Kod tabanı **yarım refactor** durumunda: entity ve bir kısım EF config güncellenmiş; testler ve Agent 1 raporu eski modele referans veriyor.

| Alan | Mevcut entity | Test / eski beklenti |
|------|---------------|----------------------|
| `CrmAccount.Create` | `(tenantId, name, accountCode, ...)` zorunlu | `(tenantId, name, email, phone, website, address, industry)` — `accountCode` yok |
| `CrmAccount` property | `Name`, `AccountCode`, `Country`, `City` | `Website`, `Address`, `Industry` |
| `CrmContact` | `FullName`, `CrmAccountId`, `IsPrimary` | `FirstName`, `LastName`, `AccountId`; domain event bekleniyor |
| `CrmTag` | `Color`; domain event **yok** | `ColorCode`; `CrmTagCreatedDomainEvent`; hex validasyonu |
| `CrmProposal` | `ProposalNumber`, `Amount`, `Currency`; `Sent`/`Approved` event | `Title`, `Value`, `DiscountRate`, `NetValue`, `UpdateFinancials`; `CrmProposalStatusChangedDomainEvent` |
| `CrmOpportunity` | `CrmAccountId` | `AccountId`; `contactId` parametresi |
| `CrmActivity` | `ActivityType`, `ActivityDate`; status enum **yok** | `Type`, `DueDate`, `CrmActivityStatus.Pending`, `AccountId` |

---

## Plan Kapsamı Gap Analizi (`TASK_013_CRM_FOUNDATION_PLAN.md`)

| Plan maddesi | Durum |
|--------------|--------|
| 6 core entity + `CrmProposalItem` | ❌ `CrmProposalItem` eksik |
| `NpsScore`, `Segment`, `CompanyName`, `IsPrimaryContact` vb. | ❌ Eksik veya farklı isimlendirme |
| CQRS handlers | ❌ Yok |
| API controllers + `[Authorize]` | ❌ Yok |
| PostgreSQL migration | ❌ Yok (SQLite in-memory test hedeflenmiş ama testler derlenmiyor) |
| CEO/Sales Control Tower query'leri | ❌ Yok |
| Outbox entegrasyon testi | ⚠️ Test dosyası var; **derlenemedi** |

---

## Olumlu Bulgular (tamamlanırsa korunmalı)

1. **Multi-tenant factory guard:** Tüm CRM `Create` metotlarında `tenantId == Guid.Empty` kontrolü.
2. **Result pattern:** Domain hataları `Result.Failure` + `Error.Validation` ile dönüyor; exception fırlatılmıyor.
3. **Value object kullanımı:** `EmailAddress`, `PhoneNumber`, `Money` (niyet doğru; `TaxNumber` shadowing bug'ı düzeltilmeli).
4. **UTC DateTime:** `SpecifyKind(..., Utc)` kullanımı PostgreSQL `timestamptz` kuralına uygun niyet taşıyor.
5. **EF logical FK:** Güncel config'ler cross-aggregate navigation FK kurmuyor; tenant bileşik index'ler planla uyumlu.
6. **Domain events (kısmi):** `CrmAccount`, `CrmOpportunity`, `CrmProposal`, `CrmActivity` create/update event'leri tanımlı; outbox pipeline Task 008A ile uyumlu olabilir (build geçince retest gerekir).

---

## Agent 1 Raporu Çapraz Doğrulama

| `TASK_013_REPORT.md` iddiası | QA sonucu |
|------------------------------|-----------|
| Build 0 hata | ❌ 9 hata |
| 98/98 test | ❌ CRM test projeleri derlenmiyor |
| 18 CRM domain + 5 persistence test | ❌ Test kaynak kodu entity API ile uyumsuz |
| Technical debt: Yok | ❌ Entity/config/test drift + `TaxNumber` bug |
| Risks: Yok | ❌ Build kırıklığı sprint blocker |

---

## Blocker'lar (Agent 1 — yeniden teslim öncesi)

1. **`TaxNumber` shadowing** — `CrmAccount.TaxNumber` property vs `TaxNumber` value object; alias veya fully-qualified çözüm.
2. **Tek domain modeli seç** — entity, EF config ve testleri aynı API/property set'ine hizala.
3. **Testleri derlet ve koştur** — `dotnet build Emare.sln` + `dotnet test Emare.sln` gerçekten yeşil olmalı.
4. **Event sözleşmesi** — `EVENT_BUS.md` ile hizala; eksik event tiplerini ekle veya test beklentilerini güncelle.
5. **`CrmProposalItem`** — plan zorunlu entity; ekle veya plan revizyonu dokümante et.
6. **Permission set** — plan §8'deki 11 CRM permission'ı `Permissions.cs`'e ekle (API Task 014'e kadar en azından tanımlı olmalı).
7. **Pre-flight checklist** — Agent 1 raporuna `AGENTS.md` § PRE-FLIGHT onayı ekle.

---

## Önerilen Yeniden QA Koşulu

Aşağıdakiler sağlandığında **CONDITIONAL PASS** veya **PASS** için yeniden review:

```bash
dotnet restore Emare.sln
dotnet build Emare.sln    # 0 error
dotnet test Emare.sln     # tüm projeler dahil CRM testleri geçmeli
```

Ek kabul: entity/config/test drift yok; `CrmProposalItem` veya plan exception dokümante; event adları `EVENT_BUS.md` ile mapping tablosu; permission stub'ları tam.

---

## QA Metadata

| Alan | Değer |
|------|--------|
| Private repo path | `/Users/emre/Elyafgroup` |
| Public repo path | `/Users/emre/yeni-versiyon-gecis` |
| Branch (public) | `gece-otonom` |
| Önceki QA | `QA_TASK_013_CRM.md` (ilk slice — superseded by this report) |
| Kod değişikliği | Yok (QA only) |
