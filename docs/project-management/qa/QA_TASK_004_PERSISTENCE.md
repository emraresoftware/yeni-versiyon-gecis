# QA Review — Task 004 Persistence

**Reviewer:** Agent 2 (QA / Test / Review)  
**Date:** 2026-06-27  
**Scope:** `Emare.Platform.Persistence` — DbContext, EF configurations, interceptors, `EfRepository`, `UnitOfWork`, persistence tests  
**Method:** `dotnet restore/build/test`, kaynak inceleme, Task 001–003 QA bulguları ile karşılaştırma  
**Kısıt:** Kod değiştirilmedi, commit/push yapılmadı.

---

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | ✅ Başarılı |
| `dotnet build Emare.sln` | ✅ Başarılı — **0 hata**, **4 uyarı** (CA1000, BuildingBlocks Results) |
| Süre | ~3.6 sn |

**Derlenen persistence bileşenleri:** `EmareDbContext`, 7 entity configuration, 2 interceptor, `EfRepository<>`, `UnitOfWork`, `PersistenceDependencyInjection`.

---

## Test Result

| Test projesi | Geçen | Başarısız | Toplam |
|--------------|-------|-----------|--------|
| `Emare.BuildingBlocks.Tests` | 8 | 0 | 8 |
| `Emare.Platform.Domain.Tests` | 10 | 0 | 10 |
| `Emare.Platform.Persistence.Tests` | 10 | 0 | 10 |
| `Emare.Platform.API.Tests` | 0 | 0 | 0 (test yok) |
| **Emare.sln toplam** | **28** | **0** | **28** |

**Genel sonuç:** ✅ Tüm testler geçti.

### Persistence test kapsamı (10 test)

| Test | Doğrulanan davranış |
|------|---------------------|
| `DbContext_CanBeCreated` | Context oluşturma |
| `Tenant_CanBeSaved` | Temel persist |
| `Tenant_Slug_ShouldBeUnique` | Unique index |
| `ApplicationUser_Email_ShouldBeUniquePerTenant` | Composite unique index |
| `SaveChanges_ShouldSetCreatedAtInUtc` | Audit interceptor — CreatedAt UTC |
| `SaveChanges_ShouldSetUpdatedAtInUtc_OnModify` | Audit interceptor — UpdatedAt UTC |
| `SoftDelete_ShouldNotPerformPhysicalDelete` | Soft delete + query filter |
| `AuditLog_ShouldNotBeSoftDeleted_AndShouldThrowIfDeletedOrModified` | AuditLog immutability (Remove) |
| `UnitOfWork_SaveChangesAsync_ShouldWork` | UoW |
| `EfRepository_AddAndGet_ShouldWork` | Generic repository |

**Altyapı:** Testler **SQLite in-memory** (`Microsoft.EntityFrameworkCore.Sqlite 8.0.11`) kullanıyor; PostgreSQL provider production’da (`Npgsql.EntityFrameworkCore.PostgreSQL 8.0.11`).

---

## Architecture Findings

| Kural | Bulgu |
|-------|--------|
| Controller → DbContext | ✅ API katmanında DbContext kullanımı yok (`Program.cs` hâlâ WeatherForecast şablonu) |
| Persistence → Domain | ⚠️ csproj yalnızca `Application` referans alıyor; entity erişimi transitive — doğrudan `Domain` referansı tercih edilir |
| Repository → AggregateRoot | ✅ **Task 001–003 bulgusu giderildi:** `BaseAuditableEntity : AggregateRoot` |
| API → Persistence DI | ❌ `AddPersistence()` henüz `Program.cs`’e bağlanmamış |

**Katman değerlendirmesi:** Persistence modülü izole ve test edilebilir; Application/Infrastructure/API entegrasyonu sonraki task’a bırakılmış.

---

## Persistence Findings

### EmareDbContext

- 7 `DbSet` tanımlı (Tenant, ApplicationUser, Role, Permission, UserRole, RolePermission, AuditLog).
- Configuration’lar assembly scan ile yükleniyor (`ApplyConfigurationsFromAssembly`).
- Interceptor’lar constructor injection + `OnConfiguring` ile ekleniyor.
- **`ITenantProvider` entegrasyonu yok** — global tenant filter uygulanmıyor.

### Entity configurations (7/7)

| Entity | Tablo | Soft-delete filter | Unique index | RowVersion |
|--------|-------|-------------------|--------------|------------|
| Tenant | Tenants | `!IsDeleted` | Slug | Provider-split ✅ |
| ApplicationUser | ApplicationUsers | `!IsDeleted` | (TenantId, Email) | Provider-split ✅ |
| Role | Roles | `!IsDeleted` | (TenantId, Code) | Provider-split ✅ |
| Permission | Permissions | `!IsDeleted` | Code | Provider-split ✅ |
| UserRole | UserRoles | `!IsDeleted` | (TenantId, UserId, RoleId) | Provider-split ✅ |
| RolePermission | RolePermissions | `!IsDeleted` | (TenantId, RoleId, PermissionId) | Provider-split ✅ |
| AuditLog | AuditLogs | **Yok** (immutable) | — | Provider-split ✅ |

**Task 001–003 eksik config bulgusu:** ✅ Giderildi (UserRole, RolePermission, AuditLog eklendi).

### Audit interceptor (`AuditableEntitySaveChangesInterceptor`)

- `IDateTimeProvider.UtcNow` ve `ICurrentUser.Id` kullanıyor — ✅ `DateTime.Now` yok.
- Added → `CreatedAt`, `CreatedBy`; Modified → `UpdatedAt`, `UpdatedBy`.
- `CancellationToken` async override’da iletiliyor.

### Soft delete interceptor (`SoftDeleteSaveChangesInterceptor`)

- `Remove` → fiziksel silme yerine `IsDeleted`, `DeletedAt`, `DeletedBy` set ediliyor — ✅
- `AuditLog` için `Deleted` ve `Modified` state’te `InvalidOperationException` — ✅ immutability koruması
- **Eksik:** AuditLog **property değişikliği** (Modified) test edilmiyor; yalnızca `Remove` senaryosu var.

### Generic repository (`EfRepository<T>`)

- Kısıt: `where TAggregateRoot : AggregateRoot` — entity hiyerarşisi ile uyumlu.
- `Delete` → `Remove` (soft delete interceptor devreye girer) — ✅
- `Update` → `DbContext.Update(entity)` (tüm alanları modified işaretleyebilir — bilinen EF pattern, şimdilik kabul edilebilir).
- Aggregate dışı entity kabul etmiyor — ✅ derleme zamanı güvencesi.

### UnitOfWork

- Minimal, doğru: `SaveChangesAsync` → `_dbContext.SaveChangesAsync(ct)`.

### PersistenceDependencyInjection

- `AddDbContext` + Npgsql connection string.
- `IUnitOfWork`, `IRepository<>` kayıtlı.
- **Eksik:** `ICurrentUser`, `IDateTimeProvider`, `ITenantProvider` kaydı yok → runtime’da interceptor’lar çözülemez (Infrastructure task’ına bağlı).

### Migrations

- `src/Platform/Persistence/Migrations/` **boş** — EF migration üretilmemiş; PostgreSQL şema doğrulaması yapılmamış.

---

## PostgreSQL Compatibility Risks

| Risk | Açıklama | Şiddet |
|------|----------|--------|
| **SQLite vs Npgsql test gap** | Tüm persistence testleri SQLite in-memory; production Npgsql | Medium |
| **RowVersion / `IsRowVersion()`** | Config’ler provider’a göre split: SQLite → `IsConcurrencyToken()` + default `byte[]`; PostgreSQL → `IsRowVersion()`. **`xmin` / Npgsql concurrency davranışı hiç test edilmiyor** | Medium |
| **Concurrency conflict senaryosu yok** | Optimistic concurrency exception testi yok | Medium |
| **`timestamptz` Kind** | Interceptor UTC kullanıyor — ✅ Npgsql uyumlu olmalı; ancak PostgreSQL integration testi yok | Low |
| **Permission `TenantId = Guid.Empty`** | Global permission modeli; tenant filter eklendiğinde kaybolma riski devam ediyor | Medium |

**Not:** SQLite testlerinde `Relational:ProviderName` annotation ile doğru config dalı seçiliyor — provider-split pattern bilinçli ve doğru uygulanmış. Ancak bu, PostgreSQL’deki gerçek `xmin`/row-version semantiğini **kanıtlamaz**.

---

## Test Coverage Gaps

| Eksik senaryo | Öncelik |
|---------------|---------|
| TenantId global query filter (cross-tenant sızıntı) | High |
| AuditLog **Modify** (property update) immutability | Medium |
| Role, Permission, UserRole, RolePermission persist + unique constraint | Medium |
| Repository `Delete` → soft delete (repository üzerinden) | Low |
| Optimistic concurrency (`DbUpdateConcurrencyException`) | Medium |
| PostgreSQL / Testcontainers integration test | High |
| EF migration apply + schema snapshot | High |
| `AddPersistence` DI end-to-end (ICurrentUser mock/stub ile) | Medium |
| Permission global (`TenantId = Empty`) filter istisnası | Medium |

---

## Critical Issues

| # | Konu | Öncelik | Durum |
|---|------|---------|-------|
| C1 | **TenantId global query filter hâlâ yok** — yalnızca `!IsDeleted` | 🔴 High | Open (Task 001–003’ten devam) |
| C2 | **EF migration yok** — PostgreSQL şema ve `IsRowVersion()` mapping doğrulanmadı | 🔴 High | Open |
| C3 | **Persistence testleri SQLite-only** — Npgsql/xmin davranışı temsil edilmiyor | 🟠 Medium | Open |
| C4 | **`AddPersistence` + provider kayıtları API’ye bağlı değil** | 🟠 Medium | Open |
| C5 | **`DateTime.Now`** API template’inde (Persistence dışı ama solution içinde) | 🟡 Low | Open |

### Çözülen (Task 001–003 → 004)

| # | Konu | Durum |
|---|------|-------|
| R-002 (önceki) | `BaseAuditableEntity : AggregateRoot` — repository uyumu | ✅ Resolved |
| R-005 (önceki) | Eksik EF config (UserRole, RolePermission, AuditLog) | ✅ Resolved |
| R-004 (kısmi) | Persistence placeholder test | ✅ Anlamlı 10 test eklendi |

---

## Suggestions

1. **Tenant filter (bloklayıcı):** `EmareDbContext` veya configuration extension ile `IHasTenant` entity’lere `TenantId == _tenantProvider.TenantId` filter; `Permission` (`Guid.Empty`) ve `Tenant` için ADR istisnası.
2. **İlk migration:** `dotnet ef migrations add InitialPlatform` (Persistence startup) — PostgreSQL’de `RowVersion`/`xmin` kolon tipini doğrula.
3. **Testcontainers PostgreSQL:** En az 1 integration test suite (soft delete + unique + concurrency) SQLite’a ek olarak.
4. **Concurrency testi:** Aynı entity’yi iki context’te güncelle → `DbUpdateConcurrencyException` beklentisi.
5. **AuditLog modify testi:** Property set + `SaveChanges` → exception.
6. **DI tamamlama:** `AddPersistence` içinde veya Infrastructure extension’da `ICurrentUser` / `IDateTimeProvider` kaydı; API `Program.cs` wiring.
7. **Provider-split sadeleştirme:** Ortak `ConfigureRowVersion()` extension ile tekrarlayan if/else bloklarını azalt (Agent 1 işi — borç kaydı).
8. **Npgsql concurrency:** Dokümantasyona göre `UseXminAsConcurrencyToken()` veya `uint xmin` property değerlendir — `byte[]` + `IsRowVersion()` PostgreSQL’de beklenen davranışı vermeyebilir.

---

## Final Verdict

**🟡 CONDITIONAL PASS — Task 004 Persistence hedeflerinin büyük kısmı karşılandı, production-ready değil**

**Gerekçe:**
- ✅ Build/test yeşil; persistence modülü anlamlı integration-style unit testlere kavuştu (10 test).
- ✅ Soft delete, audit UTC, AuditLog immutability (delete), unique index, repository/UoW çalışıyor.
- ✅ Task 001–003’teki eksik EF config ve AggregateRoot uyumsuzluğu giderildi.
- ❌ **TenantId izolasyon filter’ı** hâlâ yok — güvenlik açısından bloklayıcı.
- ❌ Migration ve PostgreSQL doğrulaması yok — concurrency mapping belirsiz.
- ⚠️ SQLite testleri provider-split sayesinde yapılandırma dalını doğrular; Npgsql runtime davranışını kanıtlamaz.

**Önerilen gate (Task 005):** C1 (tenant filter) + C2 (ilk migration + PostgreSQL smoke test) kapatılmadan Application handler’ları persistence’a bağlanmasın.

---

*Bu rapor yalnızca analiz amaçlıdır. Kod, commit, push veya branch işlemi yapılmamıştır.*
