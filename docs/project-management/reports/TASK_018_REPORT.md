# Task 018 Report — Voice Bridge: asyncpg → HTTP API Refactoring

## Objective
`standalone_bridge.py` içindeki tüm doğrudan PostgreSQL bağlantılarını (asyncpg) kaldırarak
Python ses köprüsünü C# API katmanı üzerinden güvenli HTTP isteklerine taşımak.

## Scope
- C# `VoiceBridgeController` + `VoiceBridgeService` + `IVoiceBridgeService` oluşturuldu
- `VoiceBridgeAuthMiddleware` (`X-Voice-Bridge-Key` header koruması) eklendi
- Python `bridge_api_client.py` HTTP istemci katmanı yazıldı
- `standalone_bridge.py` içindeki 8 asyncpg fonksiyon HTTP'ye yönlendirildi
- `compose.yml` + `.env.example` yapılandırması güncellendi

## Files Created
| Dosya | Açıklama |
|-------|----------|
| `src/EmareTicket.API/Controllers/VoiceBridgeController.cs` | 8 endpoint REST controller |
| `src/EmareTicket.API/Services/IVoiceBridgeService.cs` | Servis interface |
| `src/EmareTicket.API/Services/VoiceBridgeService.cs` | EF Core + iş mantığı implementasyonu |
| `src/EmareTicket.API/Middleware/VoiceBridgeAuthMiddleware.cs` | X-Voice-Bridge-Key auth middleware |
| `gemini-live-standalone/bridge_api_client.py` | Python HTTP istemci (retry, fallback) |

## Files Modified
| Dosya | Değişiklik |
|-------|-----------|
| `gemini-live-standalone/standalone_bridge.py` | import asyncpg kaldırıldı; 8 DB fonksiyon API'ye yönlendirildi |
| `gemini-live-standalone/compose.yml` | DB_* yerine EMARE_API_URL + EMARE_SERVICE_KEY |
| `gemini-live-standalone/.env.example` | Aynı şekilde güncellendi |
| `src/EmareTicket.API/Program.cs` | Middleware + servis DI kaydı |

## Architecture Decisions
1. **Tek yönlü bağımlılık:** Python bridge artık PostgreSQL'e doğrudan bağlanmıyor.
2. **X-Voice-Bridge-Key auth:** JWT gerektirmez, static service key.
3. **Backward compatibility:** db_pool global None stub olarak bırakıldı.
4. **VoiceTicketSummary rename:** DTO çakışması için Voice prefix eklendi.
5. **EF LINQ fix:** Stage string mapping client-side anonymous type + projection.
6. **Retry + fallback:** 3 retry + exponential backoff + local JSON fallback.

## Build Result
- EmareTicket.API: 0 hata, 0 uyarı ✅
- Python syntax: bridge_api_client.py + standalone_bridge.py PASS ✅

## Test Result
- Emare.Platform.API.Tests: 52 test — 0 başarısız ✅
- Test projesindeki CreateCrmProposalCommand.Status hatası önceden var (Task 018 dışı)

## Security Notes
- DB kimlik bilgileri artık Python köprüsünde tutulmuyor
- VOICE_BRIDGE_SERVICE_KEY .gitignore korumalı .env'den okunuyor
- VoiceBridgeAuthMiddleware boş/yanlış key → 401

## Technical Debt
- asyncpg paketi requirements.txt'ten kaldırılmalı (ayrı task)
- Test projelerindeki CreateCrmProposalCommand.Status hatası (önceden var, Task 018 dışı)

## Breaking Changes
- DB_HOST/PORT/NAME/USER/PASSWORD env var'lar artık kullanılmıyor
- Sunucuya EMARE_API_URL + VOICE_BRIDGE_SERVICE_KEY eklenmeli

## Next Recommended Task
- asyncpg paketini requirements.txt'ten kaldır
- VOICE_BRIDGE_SERVICE_KEY üretim .env dosyalarına ekle
- Test projelerindeki pre-existing hatayı düzelt
