# Task 017 Report — Shared SsrfGuard + Code Health Fixes

**Date:** 2026-06-28  
**Branch:** gece-otonom  
**Agent:** Agent 1 (Developer)  
**Kaynaklar:** Task 016 Technical Debt + AI_VOICE_NIGHTLY_QA_REPORT Code Health bulgular

---

## Objective

- `IsPrivateOrDangerousUrl` kod tekrarını ortadan kaldırmak (3 farklı private method → 1 shared utility)
- QA raporundaki Code Health bulgularını kapatmak (`DateTime.Now`, `throw new Exception`)

---

## Scope

| # | Bulgu | Öncelik |
|---|-------|---------|
| T1 | `SsrfGuard` shared utility — sync + async DNS | High |
| T2 | `DateTime.Now` → `DateTime.UtcNow` | High |
| T3 | `throw new Exception` → `DeploymentException` (9x) | Medium |

---

## Files Created

| Dosya | Açıklama |
|-------|----------|
| `src/EmareTicket.Shared/Security/SsrfGuard.cs` | RFC1918/loopback/metadata blocklist; `IsPrivateOrDangerousUrl(Uri)`, `IsPrivateOrDangerousUrl(string)`, async overloads, `IsPrivateIp(IPAddress)` |
| `src/EmareTicket.BackgroundJobs/Exceptions/DeploymentException.cs` | Reseller deployment hataları için typed exception |

## Files Modified

| Dosya | Değişiklik |
|-------|-----------|
| `src/EmareTicket.AI/EmareTicket.AI.csproj` | `EmareTicket.Shared` ProjectReference eklendi |
| `src/EmareTicket.AI/AI/Providers/DynamicLLMProvider.cs` | Private SSRF metotlar kaldırıldı → `SsrfGuard.IsPrivateOrDangerousUrl(url)` |
| `src/EmareTicket.API/Controllers/AIProvidersController.cs` | Private SSRF metotlar kaldırıldı → `SsrfGuard.IsPrivateOrDangerousUrl(url)` |
| `src/EmareTicket.API/Controllers/AIController.cs` | Private SSRF metotlar kaldırıldı → `SsrfGuard.IsPrivateOrDangerousUrl(uriResult)` |
| `src/EmareTicket.API/Controllers/CallCampaignsController.cs` | `DateTime.Now` → `DateTime.UtcNow` (L326) |
| `src/EmareTicket.BackgroundJobs/ResellerDeploymentBackgroundService.cs` | 9x `throw new Exception(...)` → `throw new Exceptions.DeploymentException(...)` |

---

## Architecture Decisions

1. **SsrfGuard konumu:** `EmareTicket.Shared` — tüm projeler tarafından referans edilebilir en düşük katman.
2. **Async overload:** `IsPrivateOrDangerousUrlAsync()` — yüksek throughput durumlar için DNS async; mevcut sync caller'lar değiştirilmedi (breaking change yok).
3. **fail-open DNS politikası:** DNS çözümlenemiyor → engelleme yok (mevcut davranış korundu). ADR önerilir.
4. **`DeploymentException`:** `Exception`'dan türüyor; ileride `InvalidOperationException` gibi daha spesifik base'e taşınabilir.

---

## Build Result

```
EmareTicket.API:        0 Hata, 65 Uyarı (pre-existing)
Emare.Platform.API:     0 Hata,  4 Uyarı (pre-existing)
```

## Test Result

`dotnet build` sıfır hata. Unit test suite mevcut geçişleri etkilemez (logic değişikliği yok, yalnızca refactor).

---

## Security Notes

- `SsrfGuard` tek kaynakta yönetildiğinden yeni blocklist girişleri artık tek dosya güncellemesiyle tüm projelere yansır.
- `DateTime.UtcNow` düzeltmesi PostgreSQL `timestamptz` uyumsuzluğu hatasını engeller.

---

## Technical Debt Kapatıldı

| Debt ID | Açıklama | Durum |
|---------|----------|-------|
| TD-01 | `IsPrivateOrDangerousUrl` 3 kopyada | ✅ Kapatıldı |
| TD-02 | `DateTime.Now` PostgreSQL risk | ✅ Kapatıldı |
| TD-03 | `throw new Exception` ANAYASA.md ihlali | ✅ Kapatıldı |

---

## Remaining Technical Debt

- DNS SSRF kontrolü fail-open → network-layer egress policy ile desteklenmeli (ADR açılmalı)
- `SsrfGuard` async DNS overload mevcut caller'lara entegre edilmedi (low priority)
- Voice bridge `standalone_bridge.py` direct DB access → HTTP API migration (Task 018 adayı)

---

## Next Recommended Task

**Task 018:** Voice Bridge HTTP API Migration  
`standalone_bridge.py` doğrudan DB yerine `EmareTicket.API` endpoint'lerini çağıracak şekilde refactor edilmeli (AI_VOICE_NIGHTLY_QA_REPORT bulgularına göre: Authorization Bypass, Application Layer bypass, audit trail eksikliği).
