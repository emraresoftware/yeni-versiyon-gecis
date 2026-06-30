# 🤖 06_AI_CREDIT_SYSTEM.md (AI Kredi Tüketim Standartları)

Yapay zeka servislerinin token ve kredi karşılıklarını, anlık bakiye denetimlerini ve limit aşım kurallarını belirler.

---

## 1. Kredi Tüketim Katsayıları (Usage Ratios)
Her yapay zeka eylemi için `Usage Meter` tarafından ölçülen katsayılar:
* **Gemini Live Girdi:** 1000 token = 1 Kredi
* **Gemini Live Çıktı:** 1000 token = 3 Kredi
* **ElevenLabs TTS:** 1000 karakter = 2 Kredi
* **Realtime Video:** 1 saniye = 5 Kredi

---

## 2. Anlık Bakiye Denetimi (Balance Check)
* `AI Gateway`, her istek başında cüzdan servisinden onay alır. Bakiye yetersiz ise istek doğrudan `402 Payment Required` ile reddedilir veya kiracı ayarlarına göre ücretsiz fallback (lokal model) moduna yönlendirilir.
