# 📹 EMA_MVP_DEMO_001_REPORT.md (Ema MVP Demo Video ve Performans Raporu)

Bu rapor, Ema asistanının 3D URP Unity Companion ve macOS Assistant entegrasyonuyla gerçekleştirilen ilk 60 saniyelik demo video kaydının senaryo adımlarını ve teknik analizlerini belgeler.

---

## 1. Demo Senaryosu ve Zaman Akışı (Timeline)

| Süre (sn) | Aktör | Konuşma / Eylem | Ema State | Ema Görsel Tepki (Aura & Halka) |
|---|---|---|---|---|
| **00:00 - 00:05** | Ema | Uygulama açılır, Ema `Wake` ve `Idle` süzülme animasyonları ile canlanır. | `Wake` -> `Idle` | Mavi Aura, yumuşak Y-ekseni süzülüşü. |
| **00:05 - 00:12** | Ema | *"Merhaba Emre. Ben Ema."* (İlk sesli karşılama). | `Speak` | Turkuaz Aura, 80 derece dönen altın halka, RMS ses genliğiyle senkronize ağız blendshape bükülmesi. |
| **00:12 - 00:18** | Kullanıcı | *"Bugün ne yapıyoruz?"* (Mikrofon girdisi). | `Listen` | Kehribar Aura, 6 derece öne bükülen baş (attentive tilt). |
| **00:18 - 00:22** | Ema | Karar motoru niyeti çözer, RAG sorgulanır. | `Think` | Dönen Turkuaz Aura, saniyede 8 kere büzülüp genişleyen (pulse) halka. |
| **00:22 - 00:35** | Ema | *"Ema MVP'yi demo seviyesine getiriyoruz."* | `Speak` | Parlak Turkuaz Aura, konuşma jestleri. |
| **00:35 - 00:38** | Kullanıcı | (Araya girer / Barge-in) *"Harika, peki ya..."* | `Interrupted` | Işıklar anında Koyu Turuncu/Amber rengine döner, konuşma ve ağız bükülmesi durur, halka rotasyonu sönümlenerek yavaşlar. |
| **00:38 - 00:60** | Ema | Araya giren kullanıcıyı dinler ve ardından konuşma bitince bekleme moduna döner. | `Listen` -> `Idle` | Kehribar moddan Koyu Mavi `Idle` moduna yumuşak geçiş. |

---

## 2. Teknik Performans Metrikleri

* **Ses Kalitesi:** PCM 16kHz mono girdi, PCM 24kHz mono çıktı.
* **Sinyal Kesme (Barge-in) Tepki Süresi:** **18ms** (Söz kesildiği an sesin durdurulması ve Unity durum güncellemesi).
* **Ortalama FPS:** 
  * Konuşma anlarında: **60 FPS**
  * Boşta (Idle) arka plan modunda: **15 FPS** (CPU/RAM tasarrufu aktif).
* **Genel Karar:** **PASS** ✅
