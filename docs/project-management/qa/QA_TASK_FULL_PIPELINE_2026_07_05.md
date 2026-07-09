# QA Review — Full Pipeline Check

**Task:** TASK_FINISHED Full Pipeline  
**Date:** 2026-07-05  
**Reviewer:** Agent 2 (QA Intelligence — Antigravity)  
**Scope:** Tüm proje — Backend (.NET 8 / EmareTicket.sln), Frontend (Next.js / web/), Testler, Mimari, Güvenlik  
**Kısıt:** Kod değiştirilmedi, commit yapılmadı.

---

## Build

### dotnet build EmareTicket.sln -c Release

❌ **FAIL** — 3 derleme hatası

| Dosya | Hata | Açıklama |
|-------|------|----------|
| `src/EmareTicket.Application/Abstractions/Mail/IEmareMailProvisioner.cs:22` | CS0118 | `Tenant` bir namespace olarak çözümleniyor (`EmareTicket.Application.Abstractions.Tenant`), `EmareTicket.Domain.Entities.Tenant` entity sınıfına erişilemiyor |
| `src/EmareTicket.Application/Abstractions/Mail/IEmareMailProvisioner.cs:25` | CS0118 | Aynı namespace/class çakışması |
| `src/EmareTicket.Application/Abstractions/Mail/IEmareMailProvisioner.cs:31` | CS0118 | Aynı namespace/class çakışması |

**Kök neden:** `EmareTicket.Application.Abstractions.Tenant` namespace'i, `using EmareTicket.Domain.Entities;` ile gelen `Tenant` class'ını gölgeliyor. Çözüm: `IEmareMailProvisioner.cs` içinde `Tenant` yerine `EmareTicket.Domain.Entities.Tenant` tam nitelikli ad kullanılmalı veya namespace yeniden adlandırılmalı.

### npm run build (Next.js / web/)

❌ **FAIL** — Parsing hatası

**Kök neden:** 4 dosyada **çözülmemiş Git merge conflict** marker'ları var:

| Dosya | Durum |
|-------|-------|
| `web/src/app/layout.tsx` | `<<<<<<<` / `=======` / `>>>>>>>` marker |
| `web/src/lib/api/client.ts` | Merge conflict marker |
| `web/src/app/(dashboard)/settings/mascot/page.tsx` | Merge conflict marker |
| `web/src/app/(auth)/login/login.css` | Merge conflict marker |

> ⚠️ **KRİTİK:** Bu merge conflict'ler derhal çözülmeli. Staging deploy engellidir.

---

## Tests

### dotnet test EmareTicket.sln

❌ **SKIP** — Build başarısız olduğu için testler çalıştırılamadı.

> EmareTicket.Application projesinin derleme hatası tüm bağımlı projeleri (API, Infrastructure, Persistence, Tests) blokluyor.

### Vitest (Frontend)

⚠️ **MEVCUT DEĞİL** — `web/package.json`'da Vitest/Jest konfigürasyonu yok. Frontend unit test altyapısı kurulmamış.

### Smoke Test

❌ **SKIP** — Build'ler başarısız olduğu için smoke test yapılamadı.

---

## Lint (ESLint)

⚠️ **2 hata, 803 uyarı**

| Kategori | Sayı | Detay |
|----------|------|-------|
| Hata | 2 | Bilinmeyen (merge conflict dosyalarından kaynaklı olabilir) |
| `@typescript-eslint/no-explicit-any` | ~793 | `project-control-tower.ts`, `api-types.ts` vb. |
| `@typescript-eslint/no-unused-vars` | ~10 | `useAuthStore.ts` vb. |

---

## 300 Satır Kuralı

⚠️ **ÇOK SAYIDA İHLAL**

### Backend (Migrations hariç, >300 satır)

| Dosya | Satır |
|-------|-------|
| `WhatsAppWebhookProcessor.cs` | 3,309 |
| `AiActionService.cs` | 2,930 |
| `VoiceBridgeService.cs` | 1,961 |
| `AgentHub.cs` | 1,441 |
| `Program.cs` | 1,259 |
| `Repositories.cs` | 1,189 |
| `SuperAdminTenantsController.cs` | 1,114 |
| `VoiceCallController.cs` | 1,016 |
| `ResellerTenantsController.cs` | 955 |
| `CallsController.cs` | 914 |
| `EntityConfigurations.cs` | 913 |
| `ImapPollerBackgroundService.cs` | 867 |
| `GeminiLiveSession.cs` | 814 |
| `AsteriskManagerTelephonyService.cs` | 782 |
| `WhatsAppQrBridgeService.cs` | 740 |
| `GetCrmQueries.cs` | 715 |
| `ChatSettingsController.cs` | 695 |
| `EmareAIService.cs` | 682 |
| `TenantAdminController.cs` | 636 |
| _(ve daha fazla...)_ | — |

### Frontend (>300 satır)

| Dosya | Satır |
|-------|-------|
| `demo-agent/page.tsx` | 3,447 |
| `mockData.ts` (control tower) | 3,445 |
| `mockData.ts` (dashboard) | 3,436 |
| `ScenarioCanvas.tsx` | 3,094 |
| `call-center/page.tsx` | 2,405 |
| `LoginPageClient.tsx` | 1,514 |
| `tr.ts` / `en.ts` / `zh.ts` (locales) | ~1,470 |

> **Yorum:** Locale dosyaları hariç, page component'leri ve service class'ları ciddi şekilde bölünme gerektiriyor.

---

## Forbidden Files

| Kontrol | Sonuç |
|---------|-------|
| `.env` dosyası src altında | ⚠️ `src/EmareTicket.API/.env` mevcut — .gitignore'da olmalı |
| Hardcoded password | ✅ Bulunmadı |
| Hardcoded connection string | ✅ Bulunmadı |
| `.pem` / `.key` / `.pfx` dosyası | ✅ Bulunmadı |
| Çözülmemiş merge conflict | ❌ 4 dosyada mevcut (yukarıda listelendi) |

---

## Clean Architecture

| Kural | Sonuç |
|-------|-------|
| Domain katmanı dışa bağımsız mı? | ✅ Evet — `EmareTicket.Domain` sadece kendi `Common` namespace'ini kullanıyor |
| Infrastructure sızıntısı var mı? | ✅ Hayır — Application katmanında DbContext doğrudan kullanılmıyor |
| Controller DbContext kullanıyor mu? | ✅ Hayır — Repository/Service pattern uygulanmış |
| CQRS (MediatR) uygulanıyor mu? | ✅ Evet — Application katmanında Queries/Commands ayrımı var |

**Namespace çakışması uyarısı:** `EmareTicket.Application.Abstractions.Tenant` namespace adı, `EmareTicket.Domain.Entities.Tenant` entity ile isim çakışması yaratıyor. Bu Clean Architecture ihlali değil ama adlandırma standart hatası.

---

## DDD Compliance

| Kural | Sonuç |
|-------|-------|
| AggregateRoot / Entity sınırları | ✅ `BaseEntity`, `AuditableEntity` doğru kullanılmış |
| Domain Event kullanımı | ⚠️ Sınırlı — daha fazla domain event beklenir |
| Repository sadece aggregate kökü | ✅ Repository pattern uygulanmış |
| Application vs Domain ayrımı | ✅ Katman ayrımı net |

---

## Security

| Kontrol | Sonuç |
|---------|-------|
| `DateTime.Now` kullanımı | ✅ Bulunmadı — tüm projede `DateTime.UtcNow` kullanılıyor |
| `throw new Exception` (raw) | ✅ Bulunmadı — özel exception tipleri (`DeploymentException` vb.) kullanılıyor |
| Hardcoded Secret | ✅ Bulunmadı |
| Hardcoded Connection String | ✅ Bulunmadı |
| Hardcoded Tenant ID | ✅ Bulunmadı |
| `[Authorize]` / `[AllowAnonymous]` | ✅ Yaygın şekilde uygulanmış |
| `[AllowAnonymous]` suistimali | ⚠️ `DevRequestsController.Worker.cs` — 3 worker endpoint'i `[AllowAnonymous]`, ağ güvenliği doğrulanmalı |
| `SectorsController` — 4 endpoint AllowAnonymous | ⚠️ Public data endpoint olabilir ama doğrulanmalı |

---

## Tenant Isolation

| Kontrol | Sonuç |
|---------|-------|
| Global Query Filter | ✅ `AppDbContext.OnModelCreating` — `ITenantEntity` için otomatik `TenantId == CurrentTenantId` filtresi |
| SaveChanges auto-assign | ✅ `SetTenantIdOnNewEntities()` — yeni entity'lere otomatik TenantId atanıyor |
| Manual filter uygulamaları | ✅ Repository seviyesinde ek `Where(x => x.TenantId == tenantId)` kontrolleri var |
| Filter bypass | ⚠️ `IsFilterDisabled` — SuperAdmin rolünde bypass ediliyor (tasarım gereği ama dikkatli kullanılmalı) |

---

## Permission / Authorization

| Kontrol | Sonuç |
|---------|-------|
| Controller seviyesi `[Authorize]` | ✅ Büyük çoğunlukta uygulanmış |
| Role-based access | ✅ SuperAdmin, TenantAdmin, Agent rolleri mevcut |
| Impersonation koruması | ✅ TOKEN doğrulaması mevcut (Security Rules 09) |

---

## Mock Kontrolü

| Kontrol | Sonuç |
|---------|-------|
| Mock framework tutarlılığı | ✅ Tüm testlerde **NSubstitute** kullanılıyor — tek framework |
| Mock veri (frontend) | ⚠️ 2 büyük `mockData.ts` dosyası mevcut (~3,400 satır her biri) — production'da kullanılmadığı doğrulanmalı |
| Moq kullanımı | ✅ Yok — temiz |

---

## White Label Compliance

| Kontrol | Sonuç |
|---------|-------|
| "Emare" hardcoded in UI | ✅ Frontend `src/` altında hardcoded "Emare" string yok |
| BrandProvider kullanımı | ✅ Dinamik brand yükleme mevcut |
| Dynamic favicon/title | ✅ Platform constitution kurallarına uygun |

---

## Critical Issues

| # | Seviye | Sorun | Etki |
|---|--------|-------|------|
| 1 | 🔴 CRITICAL | **dotnet build FAIL** — `IEmareMailProvisioner.cs` namespace/class çakışması (3 hata) | Backend derlenmiyor, tüm testler bloklu |
| 2 | 🔴 CRITICAL | **npm run build FAIL** — 4 dosyada çözülmemiş merge conflict | Frontend deploy imkansız |
| 3 | 🟡 HIGH | **Vitest/Jest yok** — Frontend unit test altyapısı kurulmamış | Test coverage belirsiz |
| 4 | 🟡 HIGH | **300 satır kuralı** — 20+ backend dosya, 5+ frontend dosya ihlal ediyor | Bakım ve okunabilirlik sorunu |
| 5 | 🟡 MEDIUM | **ESLint 803 uyarı** — çoğunlukla `any` type kullanımı | Type safety zayıf |

---

## Suggestions

1. **Acil:** `IEmareMailProvisioner.cs` içinde `Tenant` tipini `EmareTicket.Domain.Entities.Tenant` olarak tam nitelikli yaz — VEYA `Abstractions/Tenant` namespace'ini `Abstractions/TenantServices` olarak yeniden adlandır.
2. **Acil:** 4 dosyadaki merge conflict'leri çöz ve `npm run build` başarılı olana kadar staging deploy'u durdur.
3. **Sprint planı:** `WhatsAppWebhookProcessor.cs` (3,309 satır), `AiActionService.cs` (2,930 satır) ve `demo-agent/page.tsx` (3,447 satır) dosyalarını alt modüllere böl.
4. **Altyapı:** Frontend için Vitest + React Testing Library kurulumu yapılmalı.
5. **Type Safety:** `any` kullanımlarını kademeli olarak azalt, özellikle `project-control-tower.ts` ve `api-types.ts`.

---

## Final Verdict

# ❌ QA_FAIL

**Gerekçe:**
- Backend build başarısız (3 derleme hatası)
- Frontend build başarısız (4 çözülmemiş merge conflict)
- Testler çalıştırılamadı (build bağımlılığı)
- Smoke test yapılamadı

**Sonraki adım:** Agent 1'e hotfix atanmalı — öncelikle merge conflict'lerin çözülmesi ve namespace çakışmasının giderilmesi gerekiyor. Build yeşil olduktan sonra QA tekrar tetiklenecek.
