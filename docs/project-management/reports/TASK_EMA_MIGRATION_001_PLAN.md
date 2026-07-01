# Implementation Plan - TASK-EMA-MIGRATION-001-REVISION

Ema Desktop Assistant ve Voice Bridge yapısının, monolit depodan ayrıştırılarak **iki farklı bağımsız repository** halinde konumlandırılması için güncellenmiş geçiş ve mimari ayrıştırma planı.

## 1. Yeni Hedef Repository Yapısı

Mevcut monolit depodan ayrıştırılacak kodlar iki bağımsız repository'ye dağıtılacaktır:

### A. Repository 1: `emare-voice-runtime` (Voice Core / Ses Altyapısı)
Asterisk PBX entegrasyonu, ses köprüsü ve telefon hatları için bağımsız ses çalışma zamanı (Voice Core) bileşenlerini barındırır.
- `gemini-live-standalone/standalone_bridge.py`
- `gemini-live-standalone/asterisk_config/`
- `gemini-live-standalone/compose.yml`
- `gemini-live-standalone/voice_provider.py`
- `gemini-live-standalone/gemini_live_adapter.py`
- `gemini-live-standalone/audio_injector.py`, `gemini-live-standalone/call_room.py`
- `gemini-live-standalone/room_brain.py` (Multi-agent supervisor ve teacher modülleri)

### B. Repository 2: `ema-companion` (Ema Companion / Dijital Çalışma Arkadaşı)
macOS masaüstü asistanı arayüzü, yerel Ema karar beyni ve Unity/Dokümantasyon entegrasyon dosyalarını barındırır.
- `gemini-live-standalone/macos-assistant/` (Swift Client projesi ve paketleme betikleri)
- `gemini-live-standalone/ema_brain.py` (Karar veren ve planlayan Ema beyni)
- `gemini-live-standalone/test_ema_brain.py` (EmaBrain test dosyası)
- `EAOS_Unity_Client/` (Unity Companion dosyaları)
- Ema ile ilgili tüm kullanıcı/entegrasyon dokümantasyonu (`docs/` ve workspace belgeleri)

---

## 2. Taşınmayacak Dosyalar
Ana monolit depoda (`emaredestek/emaredestek`) kalacak dosyalar:
- `.NET 8` Clean Architecture C# API kaynak kodları (`src/` altındaki tüm projeler)
- `Next.js 16` Frontend web dashboard projesi (`web/` dizini)

---

## 3. Bağlantı ve İletişim Protokolü
Ayrışma sonrasında bileşenler arası iletişim şu şekilde yürütülecektir:
- `macos-assistant` client'ı, kullanıcının seçimine göre doğrudan ElevenLabs bulut sunucusuna veya yerel `emare-voice-runtime` bünyesinde koşan `assistant_gateway.py` WebSocket kapısına (`ws://localhost:8096`) bağlanabilecektir.
- `ema_brain.py` ve `test_ema_brain.py` bağımsız masaüstü companion bileşeni olarak yerel makinede veya istemciyle birlikte koşturulacaktır.

---

## 4. Geçiş Sırası (Migration Sequence)
1. GitHub üzerinde `emare-voice-runtime` ve `ema-companion` adlarında iki ayrı private repository oluşturulması.
2. `emare-voice-runtime` deposuna sadece Voice Core kaynak dosyalarının (standalone_bridge, asterisk_config, compose.yml, vb.) kopyalanması.
3. `ema-companion` deposuna macOS asistan projesinin, `ema_brain.py` ve `test_ema_brain.py` dosyalarının, Unity dosyalarının ve Ema dokümanlarının kopyalanması.
4. Her iki depoda bağımsız derleme (`swift build` ve docker build) testlerinin yapılması.
5. Deploy betiklerinin iki ayrı repoya göre split edilmesi.
6. Canlı ortam onaylarının ardından monolit depodaki eski dizinlerin silinmesi.
