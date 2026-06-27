# QA Review — Task 007 Authorization / Permission Engine

**Reviewer:** Agent 2  
**Date:** 2026-06-27  
**Scope:** Emare BOS (`Emare.sln`) — Authorization / Permission Engine  
**Method:** `dotnet restore/build/test`, kaynak inceleme, `SECURITY_AUTHORIZATION.md` / `SECURITY_ARCHITECTURE.md` / `API_STANDARDLARI.md` karşılaştırması  
**Kısıt:** Kod değiştirilmedi, commit yapılmadı.

**Referanslar okundu:**
- `Yeni versiyon geçiş/SECURITY_AUTHORIZATION.md`
- `Yeni versiyon geçiş/SECURITY_ARCHITECTURE.md`
- `Yeni versiyon geçiş/API_STANDARDLARI.md`
- `docs/project-management/reports/TASK_007_REPORT.md` — **bulunamadı**

---

## Build Result

**PASS**

| Komut | Sonuç |
|-------|--------|
| `dotnet restore Emare.sln` | Başarılı |
| `dotnet build Emare.sln` | **0 hata**, 4 uyarı (CA1000, BuildingBlocks Results) |

---

## Test Result

**PASS** (Task 007 authorization testleri yok; mevcut suite yeşil)

| Proje | Geçen | Başarısız | Toplam |
|-------|-------|-----------|--------|
| `Emare.BuildingBlocks.Tests` | 8 | 0 | 8 |
| `Emare.Platform.Domain.Tests` | 10 | 0 | 10 |
| `Emare.Platform.Persistence.Tests` | 13 | 0 | 13 |
| `Emare.Platform.API.Tests` | 19 | 0 | 19 |
| **Toplam** | **50** | **0** | **50** |

---

## Security Findings

| Kontrol | Sonuç | Not |
|---------|--------|-----|
| `DateTime.Now` (Platform) | ✅ | `src/Platform` içinde kullanım yok |
| `throw new Exception` (Platform) | ✅ | Doğrudan kullanım yok |
| Hardcoded JWT secret (dev fallback) | ⚠️ | `Program.cs` — production'da env zorunlu olmalı (Task 006 borcu) |
| Hardcoded tenant/brand | ✅ | Platform auth akışında yok |
| Tenant claim kaynağı | ✅ | `TenantProvider` JWT `tenant_id` okur |
| Permission enforcement | ❌ | JWT'ye permission yazılıyor; **doğrulama katmanı yok** — claim manipülasyonu teorik risk (imza geçerliyse client forge edemez, fakat sunucu tarafı policy yok) |

---

## Authorization Findings

Task 007 kapsamında aranan bileşenler — **hiçbiri `src/Platform` altında uygulanmamış**:

| Bileşen | Beklenen | Bulgu |
|---------|----------|--------|
| Permission constants | `Permissions.*` veya eşdeğer merkezi sınıf | ❌ Yok |
| Role constants | `Roles.SystemAdmin` vb. | ❌ Yok — yalnızca domain `Role.Create` PascalCase regex |
| `HasPermissionAttribute` | API declarative kontrol | ❌ Yok (`Application/Authorization/.gitkeep` boş) |
| `PermissionRequirement` | ASP.NET Core authorization | ❌ Yok |
| Authorization handler | `IAuthorizationHandler` | ❌ Yok |
| Policy provider | Dynamic permission policies | ❌ Yok |
| `UserPermissionService` | DB/claim birleşik çözümleme | ❌ Yok |
| `AddAuthorization` policies | `Program.cs` | ❌ Yalnızca `UseAuthorization()`; policy kaydı yok |

### Mevcut durum (Task 006 kalıntısı)

- **Login:** Rol/permission DB'den okunup JWT'ye ekleniyor (`JwtTokenService` — `roles`, `permissions` claim'leri).
- **Register:** Token boş rol/permission ile üretiliyor — beklenen bootstrap davranışı olabilir, ancak sonrasında endpoint koruması yok.
- **`/api/auth/me`:** `[Authorize]` var; yetkisiz istek **401** (`AuthTests.Me_WithoutToken_ShouldReturn401`) — doğru.
- **`GetCurrentUserAsync`:** `Permissions` alanı **`Array.Empty<string>()`** — JWT'deki permission claim'leri surface edilmiyor.
- **`CurrentUserProvider`:** Rol okur; **permission claim okumaz**.
- **`LoginCommand`:** `ListAsync()` ile tüm `UserRole` / `Role` / `RolePermission` / `Permission` çekilip bellekte filtreleniyor — tenant-scoped değil, ölçeklenebilirlik ve izolasyon riski (Task 004A tenant filter bağlamında).

### SECURITY_AUTHORIZATION.md uyumu

| Standart | Uyum |
|----------|------|
| Permission format `Module.Resource.Action` | ✅ Domain `Permission.Create` regex ile uyumlu |
| Kilitlenen roller (`SystemAdmin`, `TenantAdmin`, …) | ❌ Merkezi role constants / seed yok |
| Permission matrix (CRM.*, AI.*, System.*) | ❌ Constants + seed + enforcement yok |
| Controller `[Authorize(Permissions…)]` | ❌ Uygulanmamış |
| SystemAdmin / TenantAdmin sınırları | ❌ Değerlendirilemedi — motor yok |

### SystemAdmin / TenantAdmin

- **SystemAdmin aşırı genişlik:** Uygulanmış bypass yok; **herhangi bir admin rolü de tanımlanmamış**.
- **TenantAdmin tenant dışı:** Authorization handler olmadığı için **tenant-scoped permission denetimi yok**; yalnızca persistence tenant filter (004A) devreye girer.

### 401 / 403 ayrımı

| Senaryo | Mevcut | Beklenen (API_STANDARDLARI) |
|---------|--------|------------------------------|
| Token yok | 401 (`/api/auth/me`) | ✅ |
| Token var, permission yok | — | 403 Forbidden |
| Permission attribute yok | Koruma yok | Declarative 403 |

**403 senaryosu test edilmiyor** — permission engine olmadığı için mümkün değil.

### Controller içi authorization logic

- `AuthController` — yalnızca `[Authorize]` on `me`; inline permission logic yok ✅
- Korunacak business controller'lar henüz yok

---

## AI Permission Findings

`SECURITY_AUTHORIZATION.md` AI izinleri: `AI.Copilot.Use`, `AI.Agent.Execute`, `AI.Agent.Configure`, `AI.Prompt.Manage`, `AI.Memory.Read/Write`, `AI.Audit.Read`

| Kontrol | Sonuç |
|---------|--------|
| AI permission constants | ❌ Yok |
| AI özel bypass yolu | ❌ Yok (engine genel olarak yok) |
| AI → DbContext doğrudan erişim engeli | N/A Platform'da AI modülü yok |
| AIOrchestrator rol sınırı | ❌ Seed/handler yok |

**Sonuç:** AI permission'ları ne korunuyor ne bypass ediliyor — **hiç uygulanmamış**.

---

## Middleware Findings

`Program.cs` pipeline sırası:

```text
Swagger → CorrelationIdMiddleware → ExceptionHandlingMiddleware → UseHttpsRedirection
→ UseAuthentication → UseAuthorization → MapControllers
```

| Kontrol | Sonuç |
|---------|--------|
| Authentication before Authorization | ✅ |
| Exception middleware auth öncesi | ✅ (unhandled → 500 ApiResponse) |
| Authorization policies registered | ❌ |
| ProblemDetails (403/401 RFC) | ⚠️ JWT bearer default + AuthController BadRequest; permission 403 yok |

---

## Test Coverage Gaps

**Task 007 için test yok.**

Eksik senaryolar (SECURITY_AUTHORIZATION + Task 007 hedefi):

- Permission constant ↔ matrix uyumu
- `HasPermission` / policy handler — granted vs denied
- SystemAdmin vs TenantAdmin scope
- TenantAdmin başka tenant verisine erişemez (auth + persistence birlikte)
- AI permission ayrımı (`AI.Agent.Execute` vs `AI.Copilot.Use`)
- 401 vs 403 ayrımı
- JWT'de permission claim varken `/me` DTO'da permission listesi
- Register vs Login permission farkı
- Permission bypass (anonymous, empty claim, wrong tenant)

Mevcut auth testleri (`AuthTests.cs`) Task 006 kapsamında; authorization engine'i kapsamaz.

---

## Critical Issues

1. **C1 — Task 007 teslim edilmemiş:** `TASK_007_REPORT.md` repository'de yok; Permission engine bileşenlerinin tamamı eksik (constants, attribute, requirement, handler, policy provider, `UserPermissionService`).
2. **C2 — Permission enforcement gap:** JWT'ye permission yazılıyor ancak API/Application katmanında **doğrulama yok** — SECURITY_AUTHORIZATION §6 ihlali.
3. **C3 — Merkezi permission/role catalog yok:** Matrix'teki onlarca permission ve 12 rol kodda sabitlenmemiş; seed stratejisi yok.
4. **C4 — DoD / Mandatory Protocol ihlali:** Task Report + QA olmadan task kapatılamaz; Agent 1 çıktısı eksik.
5. **C5 — Authorization test suite sıfır:** Release gate için yetersiz.

---

## Suggestions

1. Agent 1: `TASK_007_REPORT.md` + `Application/Authorization/` altında constants, `PermissionRequirement`, `PermissionAuthorizationHandler`, `HasPermissionAttribute`, `UserPermissionService`, `Program.cs` policy registration.
2. `ICurrentUser` veya dedicated `IPermissionResolver` ile permission claim/DB çözümlemesi; `/me` DTO'da gerçek permission listesi.
3. `LoginCommand` — tenant-scoped repository sorguları; `ListAsync()` anti-pattern kaldırılmalı.
4. Seed: `SECURITY_AUTHORIZATION.md` matrix'ten system permissions + default role mappings.
5. `Permission` global (`Guid.Empty`) + tenant filter istisnası (R-010) authorization seed ile birlikte ADR.
6. Test projesi: `AuthorizationTests` — 401/403, SystemAdmin, TenantAdmin, AI permissions.
7. `API_STANDARDLARI.md`: Forbidden → 403 mapping permission middleware/filter ile doğrulanmalı.

---

## Final Verdict

# FAIL

**Gerekçe:** Task 007 Authorization / Permission Engine **repository'de uygulanmamış**; `TASK_007_REPORT.md` yok. Build/test yeşil olsa da bu Task 006 authentication kalıntısıdır — permission constants, authorization handler, policy provider, `UserPermissionService` ve authorization testleri **sıfır**. SECURITY_AUTHORIZATION.md declarative controller kontrolü ve permission matrix karşılanmıyor. Architect Review ve sonraki task için **Agent 1 tam teslim gerekir**.

---

*Risk çapraz referans: R-010 (global permission), yeni — R-012 önerilir: "Platform authorization engine missing (Task 007)"*
