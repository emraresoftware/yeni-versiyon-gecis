# Task 030 Report

## Objective

1. Canlı destek widget script'inin (`embed.js`) Nginx ters vekili arkasında çalışırken karşılaştığı sonsuz yönlendirme (too many redirects) hatasının giderilmesi.
2. Özel senaryo akışı (visual flow scenario) ile arama yapıldığında, standart senaryonun çalıştırılması hatasının giderilerek özel akışın devreye alınması.

## Scope

- `src/EmareTicket.API` (Program.cs, CallsController.cs, VoiceCallController.cs, VoiceBridgeService.cs)
- `gemini-live-standalone` (standalone_bridge.py)

## Files Created

- Yok.

## Files Modified

- `src/EmareTicket.API/Program.cs`
- `src/EmareTicket.API/Controllers/CallsController.cs`
- `src/EmareTicket.API/Controllers/VoiceCallController.cs`
- `src/EmareTicket.API/Services/VoiceBridgeService.cs`
- `src/EmareTicket.API/Controllers/VoiceScenariosController.cs`
- `web/src/app/layout.tsx`
- `gemini-live-standalone/standalone_bridge.py`

## Architecture Decisions

- Kestrel sunucusunun Nginx ters vekil sunucusu arkasında çalıştığı prod ortamlarında, SSL sonlandırma ve HTTPS yönlendirmesi Nginx düzeyinde yapıldığından, dotnet seviyesindeki mükerrer `app.UseHttpsRedirection()` yönlendirmesi devre dışı bırakılmıştır.
- Sesli asistan arama süreçlerinde özel senaryo (visual scenario) kullanımı tespit edildiğinde, Gemini Live (ses akışı) modu devre dışı bırakılarak turn-by-turn senaryo motorunun (`VoiceScenarioEngine`) çalışabilmesi için standart API/dialog modunun işletilmesi zorunlu kılınmıştır.
- Standalone Python ses köprüsü (Asterisk AudioSocket) Gemini Live akış modunda çalıştığı için, görsel akış düğümleri dotnet API tarafında `CompileScenarioGraphToPrompt` aracılığıyla Gemini'ın anlayacağı talimatlar bütününe (System Prompt) derlenip ses köprüsüne beslenmektedir.
- Python tarafındaki `get_localized_demo_scenario` metodunun, görsel senaryo GUID'lerini tespit ettiğinde dotnet API tarafından derlenmiş olan özel sistem prompt'unu ve karşılama metnini ezerek standart şablonlara düşmesi engellenmiş, görsel akışın derlenmiş prompt'unun korunması sağlanmıştır.
- Görsel akıştaki ilk `speak` düğümünden okunan karşılama metni, asenkron olarak santral karşılama ayarı (`greetingText`) içerisine enjekte edilerek Python köprüsünün doğru karşılama cümlesiyle başlaması sağlanmıştır.
- Next.js frontend ana şablonunda (`layout.tsx`) bulunan canlı destek widget script adresi (`embed.js`), platform genelinde `ticket.emarecloud.tr` adresi kullanımdan kaldırıldığı için relative URL'e çevrilerek dinamikleştirilmiş ve yönlendirme (redirect loop) hatası giderilmiştir.
- Yapay zeka ile ses senaryosu üretilirken (`Create` / `Update` aşamalarında) gelen açıklama metinlerinin (description) veritabanı schema limiti olan 1000 karakteri aşması durumunda oluşan 500 hatalarını engellemek için, açıklama uzunluğu API controller seviyesinde otomatik olarak kırpılarak (truncate) veritabanı tutarlılığı korunmuştur.

## Dependencies Added

- Yok.

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet build EmareTicket.sln` | PASS |

## Test Result

| Komut | Sonuç |
|-------|--------|
| `dotnet test EmareTicket.sln` | PASS — 331/331 geçti |

## Performance Notes

- Arama başlangıcındaki karşılama metninin (greeting text) TTS sentezlemesi, özel senaryo başlangıç düğümünden dinamik olarak okunarak zil çalma esnasında asenkron (`PrebuildAsync`) olarak üretilmekte ve latency (gecikme) minimum düzeyde tutulmaktadır.

## Security Notes

- Yönlendirme ve senkronizasyon ayarları çoklu kiracılı (multi-tenant) veritabanı kurallarına uygun olarak tenant düzeyinde işletilmektedir.

## Technical Debt

- Yok — bkz. debt/TECHNICAL_DEBT.md

## Risks

- Yok — bkz. risks/RISK_REGISTER.md

## Known Limitations

- Yok.

## Breaking Changes

- Yok.

## Next Recommended Task

- Senaryo motoru aksiyonlarının entegrasyon connector testleri ile doğrulanması.
