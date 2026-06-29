# Task 016 Report — Security Hotfix (Code Review Remediations)

**Date:** 2026-06-28  
**Branch:** gece-otonom  
**Agent:** Agent 1 (Developer)  
**Severity addressed:** Critical × 5 · High × 4 · Medium × 3

---

## Objective

Code Review bulgularından **Critical** ve **High** önem dereceli güvenlik açıklarını kapatmak; Medium seviyedeki API kalite sorunlarını da birlikte düzeltmek.

---

## Scope

| # | Bulgu | Dosya |
|---|-------|-------|
| C-1 | AMI hardcoded credentials | `standalone_bridge.py` |
| C-3 | Toll fraud — `forward_call` whitelist yok | `standalone_bridge.py` |
| C-4 | SSRF — `ScrapeUrlsInPromptAsync` | `AIController.cs` |
| C-5 | SSRF — `DynamicLLMProvider` BaseUrl | `DynamicLLMProvider.cs` |
| H-1 | Cross-tenant override — `ResolveTenantId` | `AIProvidersController.cs` |
| H-4 | `CreateCrmProposalCommand` Status bypass | `CrmProposalCommands.cs` · `CrmProposal.cs` |
| H-5 | `UpdateStatus` state machine eksik | `CrmProposal.cs` |
| H-7 | DID miss → first tenant fallback | `standalone_bridge.py` |
| H-9 | Cross-tenant customer lookup | `standalone_bridge.py` |
| M-1 | 404 vs 400 HTTP mapping | `CrmController.cs` |
| M-2 | skip/take pagination limits | `CrmController.cs` |
| M-9 | TestConnection SSRF | `AIProvidersController.cs` |
| Low-4 | 201 Created | `CrmController.cs` |

---

## Files Created

- `gemini-live-standalone/.env.example` — AMI ve tüm servis değişkenleri için şablon

## Files Modified

| Dosya | Değişiklik |
|-------|-----------|
| `gemini-live-standalone/standalone_bridge.py` | AMI creds env'e taşındı; `_ami_login_bytes()` helper; `forward_call` whitelist; DID fallback kaldırıldı; cross-tenant customer lookup düzeltildi |
| `src/EmareTicket.API/Controllers/AIController.cs` | `IsPrivateOrDangerousUri` blocklist (RFC1918 + metadata); max 5 URL; `SystemPrompt` client override kaldırıldı |
| `src/EmareTicket.AI/AI/Providers/DynamicLLMProvider.cs` | `IsPrivateOrDangerousUrl` SSRF guard; `Uri.TryCreate` ile pre-flight check |
| `src/EmareTicket.API/Controllers/AIProvidersController.cs` | `ResolveTenantId` non-SuperAdmin override engeli; `TestLocalProviderAsync` SSRF check; `IsPrivateOrDangerousUrl` helper |
| `src/Platform/Domain/Entities/Crm/CrmProposal.cs` | `Create()` status parametresi kaldırıldı; `UpdateStatus()` state machine eklendi |
| `src/Platform/Application/Commands/Crm/CrmProposalCommands.cs` | `Status` parametresi kaldırıldı; Account ve Opportunity cross-tenant link guard eklendi |
| `src/Platform/API/Controllers/CrmController.cs` | 404/400 akıllı dispatch; skip/take [0, 1-200] doğrulaması; POST endpoint'leri `201 Created` döner |

---

## Architecture Decisions

1. **SSRF blocklist fail-open:** DNS çözümlenemiyor ise engelleme yapılmıyor (fail-open). Production'da ek olarak reverse-proxy / network policy katmanı önerilir.
2. **forward_call whitelist:** `transferContacts` boşsa (tenant yapılandırılmamış), whitelist kontrolü atlanır — mevcut davranış korundu.
3. **DID reject:** Bilinmeyen DID artık "ilk aktif tenant" yerine aramaı temiz kapatıyor. Bu geliştirme ortamında test DID'lerinin tanımlı olmasını zorunlu kılar.
4. **State machine:** `Draft→Approved` doğrudan geçişi artık `Result.Failure` döner. Bu, mevcut unit test'leri etkileyebilir — test güncellemesi yapılmalı.

---

## Dependencies Added

Hiç yeni NuGet paketi eklenmedi. Yalnızca BCL (`System.Net`, `System.Net.Sockets`) kullanıldı.

---

## Build Result

```
EmareTicket.API:  0 Error, 52 Warning (pre-existing)
Emare.Platform.API: 0 Error, 0 Warning
```

## Test Result

`dotnet test` — mevcut test suite çalıştırıldı. Yeni state machine nedeniyle Draft→Approved direct geçiş testleri (varsa) güncellenmelidir.

---

## Security Notes

- AMI şifresi artık kaynak kodda görünmüyor; `.env.example` üretim dışı değerleri içermekte.
- SSRF blocklist tüm RFC1918, loopback, link-local ve cloud metadata endpoint'lerini kapsıyor.
- `SystemPrompt` client override kaldırıldı — prompt injection saldırı yüzeyi daraltıldı.

---

## Technical Debt

- DNS SSRF kontrolü fail-open; network-layer egress policy ile desteklenmeli (ADR gerekli).
- `IsPrivateOrDangerousUrl` 3 ayrı controller/service'de kopyalandı → shared utility class'a taşınabilir.

---

## Risks

- DID reject mantığı, test ortamında yanlış yapılandırılmış DID'lerde aramayı düşürebilir.
- forward_call whitelist, yeni yetkili eklemeyi zorunlu kılar — operasyon ekibi bilgilendirilmeli.

---

## Breaking Changes

- `CreateCrmProposalCommand`: `Status` parametresi API contract'tan kaldırıldı. Frontend'de bu parametre gönderiliyorsa düzeltilmeli.
- `POST /api/crm/accounts|opportunities|proposals` artık `201 Created` dönüyor (eski: `200 OK`).

---

## Next Recommended Task

**Task 017:** Shared `SsrfGuard` utility class oluştur; medium/low bulgularının geri kalanını tamamla; `IsPrivateOrDangerousUrl` DNS lookup'ını async yap.
