# QA Verify — Hotfix Task 004A Tenant Global Query Filter

**Reviewer:** Agent 2 (QA / Test / Review)  
**Date:** 2026-06-22  
**Scope:** Hotfix 004A — `EmareDbContext` global tenant query filter, auth etkisi, system entity istisnaları, Persistence DI, test kapsamı  
**Method:** `dotnet restore/build/test`, kaynak inceleme, Task 004 QA (C1) ile karşılaştırma  
**Kısıt:** Kod değiştirilmedi, commit/push yapılmadı.

---

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | ✅ Başarılı |
| `dotnet build Emare.sln` | ❌ **Başarısız — 5 derleme hatası** |
| `dotnet test Emare.sln` | ❌ Çalıştırılamadı (build gate) |

### Derleme hataları

| Dosya | Hata | Açıklama |
|-------|------|----------|
| `PersistenceTests.cs:291–292` | CS1503 | `AuditLog.Create` imzası yanlış (`userId` eksik; argüman sırası hatalı) |
| `ApiInfrastructureTests.cs:193` | CS0246 | `IRepository<Tenant>` testinde `Tenant` için `using` / tam ad eksik |

**Not:** Önceki (stale) derleme ile kısmi API test koşusu yapıldı: **17 geçti / 2 başarısız** (aşağıda). Güncel kaynak ağacında solution build geçmediği için tam test matrisi doğrulanamadı.

---

## Test Result (mevcut durum)

| Test projesi | Derleme | Koşum | Not |
|--------------|---------|-------|-----|
| `Emare.BuildingBlocks.Tests` | ✅ | — | Build gate nedeniyle test çalıştırılmadı |
| `Emare.Platform.Domain.Tests` | ✅ | — | — |
| `Emare.Platform.Persistence.Tests` | ❌ | — | 3 yeni multi-tenancy testi eklendi; derlenmiyor |
| `Emare.Platform.API.Tests` | ❌ | 17✅ / 2❌ (stale) | Stale assembly ile kısmi koşu |
| **Emare.sln toplam** | ❌ | — | **Gate FAIL** |

### Stale API test başarısızlıkları (tenant filter regresyonu)

| Test | Beklenen | Gerçekleşen | Kök neden (analiz) |
|------|----------|-------------|---------------------|
| `Login_ValidCredentials_ShouldReturnToken` | 200 + token | Login başarısız | `TenantProvider.TenantId == Guid.Empty` (JWT yok); `ApplicationUsers` global filter kullanıcıyı gizliyor |
| `Register_DuplicateEmail_InSameTenant_ShouldReturnBadRequest` | 400 `User.DuplicateEmail` | 500 | Duplicate check filter yüzünden mevcut kullanıcıyı göremiyor → INSERT → SQLite UNIQUE ihlali |

---

## Hotfix 004A — Kod İncelemesi

### Uygulanan değişiklik (`EmareDbContext`)

`ITenantProvider` constructor injection eklendi. `OnModelCreating` içinde `ApplyGlobalQueryFilters` reflection ile entity tiplerine göre filtre uyguluyor:

| Entity grubu | Soft delete filter | Tenant filter |
|--------------|------------------|---------------|
| `Tenant` | ✅ `!IsDeleted` | ❌ İstisna (doğru) |
| `AuditLog` | ❌ İstisna (immutable) | ✅ `TenantId == provider` |
| Diğer `IHasTenant` + `ISoftDelete` | ✅ | ✅ |
| Yalnızca `IHasTenant` | — | ✅ |

Kaynak: `src/Platform/Persistence/DbContext/EmareDbContext.cs` — `ApplyGlobalQueryFilters`, `ApplySoftDeleteAndTenantFilter`, `ApplyTenantFilter`.

**Olumlu:** Task 004 C1 bulgusuna yönelik merkezi filter mekanizması eklendi; `Tenant` registry sorguları tenant filtresinden muaf; `AuditLog` soft-delete filtresi uygulanmıyor (interceptor immutability korunuyor).

**Eksik / riskli:** `Permission` için istisna yok — global permission modeli (`TenantId = Guid.Empty`) filtrelenince oturum açık tenant bağlamında kaybolur (R-010).

---

## Doğrulama Kontrol Listesi

### 1. Tenant global query filter gerçekten çalışıyor mu?

| Durum | Bulgu |
|-------|--------|
| 🟡 Kısmen | Filter kodu mevcut ve mantıklı. **Derlenen persistence testleri koşulamadı.** `MultiTenancy_TenantIsolation_ShouldWork` eklendi (henüz derlenmiyor). Stale API testlerinde login/register regresyonu filter’ın auth akışıyla uyumsuz olduğunu gösteriyor. |

### 2. Tenant yokken data leak oluyor mu?

| Durum | Bulgu |
|-------|--------|
| ✅ Fail-safe (okuma) | `TenantProvider` claim yoksa `Guid.Empty` döner. Filter: `TenantId == Guid.Empty` → normal tenant verisi **okunmaz**. `MultiTenancy_TenantProviderEmpty_ShouldReturnEmpty` bu davranışı hedefliyor (derlenmedi). |
| ⚠️ Yan etki | Auth/register/login gibi **tenant claim’siz** HTTP isteklerinde mevcut tenant verisine erişim de kesilir — işlevsel regresyon, güvenlik açığı değil. |

### 3. AuditLog soft delete olmadan tenant filtreli okunuyor mu?

| Durum | Bulgu |
|-------|--------|
| 🟡 Tasarım OK, test FAIL | `AuditLog` dalında yalnızca `ApplyTenantFilter` çağrılıyor; soft-delete filter yok. Interceptor `Remove`/modify’de exception atmaya devam ediyor. **`MultiTenancy_AuditLog_ShouldBeFilteredByTenant` derlenmiyor** (`AuditLog.Create` argüman hatası). |

### 4. Tenant filter `Tenant` ve `Permission` gibi system entity’leri yanlış bozuyor mu?

| Entity | Durum | Bulgu |
|--------|-------|--------|
| `Tenant` | ✅ | Tenant filtresinden muaf; slug lookup mümkün. |
| `Permission` | ❌ | **İstisna yok.** `TenantId = Guid.Empty` olan global permission’lar, oturumlu tenant bağlamında (`TenantId != Empty`) sorgularda **görünmez**. `LoginCommand` permission listesi etkilenir. |

### 5. API tarafında Persistence DI gerçekten bağlanmış mı?

| Durum | Bulgu |
|-------|--------|
| ✅ | `Program.cs`: `AddPersistence(builder.Configuration)` mevcut. `PersistenceDependencyInjection`: `EmareDbContext`, interceptors, `IUnitOfWork`, `IRepository<>` kayıtlı. |

### 6. Repository/UnitOfWork API test container’da resolve ediliyor mu?

| Durum | Bulgu |
|-------|--------|
| 🟡 | `PersistenceDI_ShouldBeRegisterable` DbContext + UoW + `IRepository<Tenant>` assert ediyor; **`Tenant` tipi çözümlenemiyor (CS0246)** — test derlenmiyor. Stale koşuda DbContext/UoW resolve testleri geçmişti. |

---

## Ek Bulgular

### Per-entity `HasQueryFilter` (configuration)

`Configurations/*.cs` dosyalarında hâlâ `HasQueryFilter(e => !e.IsDeleted)` var. Global filter `ApplyConfigurationsFromAssembly` **sonrasında** uygulandığı için pratikte üzerine yazılıyor; ancak çift tanım bakım karmaşası yaratıyor (dead config).

### Auth akışı vs global filter (bloklayıcı)

`RegisterUserCommand` / `LoginCommand` tenant claim olmadan repository üzerinden `ApplicationUser` okur. Filter `TenantId == Guid.Empty` olduğunda:

- Duplicate email kontrolü çalışmaz → 500
- Login kullanıcı bulamaz → invalid credentials

**Beklenen hotfix tamamlayıcıları:** unauthenticated auth handler’larda `IgnoreQueryFilters()` veya scoped tenant override; veya filter’da “tenant unresolved → filter disabled” stratejisi (EmareTicket `AppDbContext.IsFilterDisabled` benzeri).

### `LoginCommand` bellek içi filtreleme

`ListAsync()` ile tüm `UserRole` / `Role` / `Permission` çekilip bellekte filtreleniyor — global filter tenant claim varken daraltır, claim yokken auth kırılır; claim varken de performans riski devam eder (Task 004 notu).

---

## Task 004 C1 / Risk Register

| Kayıt | Task 004 | Hotfix 004A sonrası |
|-------|----------|---------------------|
| C1 — Global tenant filter | ❌ Açık | 🟡 Kod var, auth regresyonu + test gate FAIL |
| R-001 | Open | **Open** — tam kapanmadı |
| R-010 — Permission `Guid.Empty` | Open | **Open** — istisna uygulanmadı |

---

## Final Verdict

# ❌ Fail

**Gerekçe:**

1. **`dotnet build Emare.sln` geçmiyor** — hotfix testleri tamamlanmamış.
2. **`dotnet test Emare.sln` çalıştırılamıyor** — QA gate ihlali.
3. **Auth regresyonu** — login ve duplicate-register senaryoları tenant filter ile kırılıyor (stale test kanıtı).
4. **`Permission` system entity istisnası eksik** — global permission modeli bozuluyor.
5. Tenant isolation ve AuditLog tenant filter **otomatik testlerle doğrulanamadı** (derleme hatası).

**Hotfix’i Pass yapmak için minimum:**

1. Test derleme hatalarını düzelt (`AuditLog.Create` imzası, `Tenant` using).
2. Auth/register/login için tenant-unresolved bypass stratejisi (ADR + kod).
3. `Permission` için `TenantId == Guid.Empty || TenantId == provider.TenantId` (veya eşdeğer ADR istisnası).
4. `dotnet test Emare.sln` — tüm projeler yeşil.
5. Persistence’da tenant isolation + empty tenant + AuditLog tenant filter testlerinin koştuğunu doğrula.

---

## Referanslar

- Önceki: [`QA_TASK_004_PERSISTENCE.md`](./QA_TASK_004_PERSISTENCE.md) — C1 tenant filter eksikliği
- Önceki: [`QA_TASK_005_COMPOSITION_ROOT.md`](./QA_TASK_005_COMPOSITION_ROOT.md) — Persistence DI wiring
- Risk: [`../risks/RISK_REGISTER.md`](../risks/RISK_REGISTER.md) — R-001, R-010
- Kaynak: `src/Platform/Persistence/DbContext/EmareDbContext.cs`
