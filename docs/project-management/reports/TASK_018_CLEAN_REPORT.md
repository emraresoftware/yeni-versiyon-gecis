# Task 018 Clean Report — Voice Bridge asyncpg Removal

**Date:** 2026-06-28  
**Branch:** gece-otonom  
**Agent:** Agent 1 (Developer)  
**Mission:** `MISSION_002_TELEPHONY_MODERNIZATION`  
**Depends on:** `TASK_018_VOICE_BRIDGE_REFACTOR` (DONE)

---

## Objective

Production voice bridge runtime'dan `asyncpg` bağımlılığını kaldırmak; kalan doğrudan DB erişimlerini HTTP API üzerinden tamamlamak.

---

## Scope

| # | Madde | Durum |
| - | ----- | ----- |
| 1 | `requirements.txt` → `asyncpg` kaldır, `aiohttp` ekle | ✅ |
| 2 | Dev scriptler için `requirements-dev.txt` | ✅ |
| 3 | Inbound call bootstrap → HTTP `call-session` | ✅ |
| 4 | Trunk / caller lookup → HTTP endpoints | ✅ |
| 5 | `tenant_gemini_key.py` → asyncpg kaldır | ✅ |
| 6 | Docker image → `bridge_api_client.py` COPY | ✅ |

**Kapsam dışı (bilinçli):** `db_*.py`, `scenario_runner.py` gibi ops scriptleri hâlâ `asyncpg` kullanır — yalnızca `requirements-dev.txt` ile lokal kurulum.

---

## Files Created

| Dosya | Açıklama |
| ----- | -------- |
| `gemini-live-standalone/requirements-dev.txt` | Dev/ops scriptleri için `asyncpg` |

---

## Files Modified

| Dosya | Değişiklik |
| ----- | ---------- |
| `gemini-live-standalone/requirements.txt` | `asyncpg` çıkarıldı; `aiohttp>=3.9.0` eklendi |
| `gemini-live-standalone/Dockerfile.bridge` | `bridge_api_client.py` image'a eklendi |
| `gemini-live-standalone/bridge_api_client.py` | `resolve_call_session`, `get_primary_trunk`, `lookup_caller` |
| `gemini-live-standalone/standalone_bridge.py` | Tüm `db_pool`/asyncpg yolları HTTP'ye taşındı |
| `gemini-live-standalone/tenant_gemini_key.py` | Yalnızca AES encrypt/decrypt; asyncpg kaldırıldı |
| `src/EmareTicket.API/Controllers/VoiceBridgeController.cs` | 3 yeni endpoint + DTO'lar |
| `src/EmareTicket.API/Services/IVoiceBridgeService.cs` | Yeni servis metotları |
| `src/EmareTicket.API/Services/VoiceBridgeService.cs` | Call session bootstrap, trunk, caller lookup |

---

## Architecture Decisions

1. **Tek HTTP bootstrap:** Inbound arama başlangıcı `GET /api/voice-bridge/call-session` ile tenant, müşteri, Gemini key, demo senaryo ve trunk bilgisini tek seferde çözer.
2. **Gemini key sunucuda decrypt:** Python artık `ENCRYPTION_KEY` ile DB'den key çözmez; API döner.
3. **Dev/prod ayrımı:** Production Docker image `asyncpg` içermez; ops scriptleri `requirements-dev.txt` kullanır.
4. **Güvenlik:** Bilinmeyen DID → `accepted: false`; hardcoded fallback tenant kaldırıldı.

---

## Build Result

```
dotnet build EmareTicket.sln → 0 hata
python -m py_compile standalone_bridge.py bridge_api_client.py tenant_gemini_key.py → OK
```

---

## Test Result

```
dotnet test EmareTicket.sln → 308/308 geçti (~944 ms)
```

---

## Security Notes

- Python bridge artık production'da PostgreSQL credential veya `asyncpg` taşımıyor.
- Gemini API key yalnızca `X-Voice-Bridge-Key` korumalı internal endpoint üzerinden iletilir.

---

## Technical Debt

- Ops scriptleri (`db_*.py`, `scenario_runner.py`) HTTP'ye taşınmadı — düşük öncelik, dev-only.
- `README_INTEGRATION.md` / `AGENTS.md` (gemini-live) asyncpg referansları güncellenmeli (ayrı docs task).

---

## Breaking Changes

- Production bridge container rebuild gerektirir (`docker compose up -d --build`).
- `EMARE_API_URL` + `VOICE_BRIDGE_SERVICE_KEY` zorunlu (Task 018 ile aynı).

---

## Handoff

- **Agent 2:** `TASK_018_CLEAN_QA` — `QA_TASK_018_CLEAN.md`
- **Agent 0:** TASK_QUEUE status güncelleme

---

## Next Recommended Task

`TASK_SALES_ORDER_API` (TASK_015 QA tamamlandığında)
