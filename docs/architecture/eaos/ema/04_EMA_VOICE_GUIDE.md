# 🗣️ 04_EMA_VOICE_GUIDE.md (Ses ve Sentezleme Standartları)

Bu kılavuz, Ema'nın tüm platformlarda kullanacağı ses sentezleme (TTS) stabilite ve tonlama ayarlarını belirler.

---

## 1. Ses Profil Ayarları
* **Model:** ElevenLabs `eleven_turbo_v2_5` (VoIP/realtime aramalar için) veya `eleven_multilingual_v2` (hazır anonslar için).
* **Ses Karakteri:** Sakin, orta tonlu, güven veren kurumsal bir Türkçe kadın sesi.
* **Ses Parametreleri (ElevenLabs Console):**
  * Stability (Stabilite): **%75** (Tonlama tutarlılığı için).
  * Clarity / Similarity (Netlik): **%85** (Farklı kelimelerde bozulmayı engellemek için).
  * Style Exaggeration (Tarz Abartısı): **%0** (Tamamen nötr ve kurumsal kalması için).

---

## 2. Telaffuz Sözlüğü (Pronunciation Dictionaries)
* "SipTrunks", "CRM", "ERP" gibi sektörel terimlerin Türkçe telaffuzlarının (örn: "si-pi-trank", "si-ar-em") asistan tarafından doğru okunabilmesi için ElevenLabs üzerinde ortak bir telaffuz sözlüğü (phoneme mapping) sürüm kontrollü olarak tutulur.
