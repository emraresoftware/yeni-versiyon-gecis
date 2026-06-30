# 🎙️ VOICE_CONSTITUTION.md (EAOS Ses Sistemi Anayasası)

Bu anayasa, EAOS platformunun tüm sesli iletişim servisleri için uyulması gereken zorunlu standartları tanımlar. Ana [CONSTITUTION.md](../CONSTITUTION.md) belgesinin I. ve II. maddelerine doğrudan bağlıdır.

---

## 1. Voice Core Prensipleri
* **Bağımsızlık:** Ses Çekirdeği (Voice Core), platformdaki veritabanı veya web arayüzleri çöktüğünde dahi çalışmaya devam edecek şekilde izole edilmelidir.
* **Akıcılık Önceliği:** Görüşme sırasında sesin kesilmesi veya asistanın duraksaması kesinlikle kabul edilemez. Sistem her zaman insan konuşma ritmini taklit etmeye odaklanmalıdır.

---

## 2. Low Latency (Düşük Gecikme) Kuralları
* **Ses Yolu Optimizasyonu:** Ses verisi işlem zincirinde en fazla 3 katmandan geçebilir: 
  `Asterisk (SIP/PSTN) -> standalone-voice-bridge -> Provider API (WebSocket)`.
* **Maksimum Gecikme Limitleri:**
  * SIP El Sıkışması: < 150ms
  * First Audio Output Latency (İlk Ses Çıkışı): < 400ms
  * Interruption Latency (Araya Girildiğinde Ses Kesme): < 150ms
* **Sıfır Bloklama:** Ses akışı (Audio Path) üzerinde çalışan döngüde senkron (blocking) API veya veritabanı sorgusu yapılamaz. Tüm yan süreçler asenkron olarak `asyncio.create_task` ile arka planda yürütülür.

---

## 3. Session Sticky (Oturum Sabitleme)
* **Arama Başı Seçim:** Sağlayıcı (Provider) seçimi sadece çağrının başlangıcında (INVITE anında) yapılır.
* **Geçiş Yasağı:** Arama başladıktan sonra, görüşme boyunca sağlayıcı kesinlikle değiştirilemez. 
* **Bağlantı Kopması:** WebSocket bağlantısı koptuğunda, aynı sağlayıcıya `reconnect_cooldown` süresince 3 kez tekrar bağlanma denenir. Başarısız olunursa arama sonlandırılır (failover yeni aramalar içindir).

---

## 4. Provider Abstraction (Sağlayıcı Soyutlama)
* **Protokol Standardı:** Her sağlayıcı `VoiceProvider` ve `VoiceSession` protokolünü implemente etmelidir.
* **Geriye Dönük Uyumluluk:** Yeni sağlayıcı adaptörleri eklenirken, ses köprüsünün arama döngüsü (`receive_from_gemini` / `write_to_asterisk`) değiştirilmeyecektir.

---

## 5. Circuit Breaker (Hata Devre Kesici)
Her sağlayıcı adaptörü için durum kontrolü `circuit_breaker.py` üzerinden izlenir:
* **CLOSED (Normal):** Sağlayıcı aktif ve sağlıklı.
* **OPEN (Kesik):** Ardışık 3 hata alındığında sağlayıcı devresi 30 saniye boyunca `OPEN` konumuna geçer ve yönlendirme dışı kalır.
* **HALF_OPEN (Yarı Açık):** 30 saniyelik beklemenin ardından gelen ilk çağrıda sağlayıcı test edilir. Başarılı ise `CLOSED`, başarısız ise katlanarak artan süreyle `OPEN` konumuna döner.

---

## 6. Audio Codec Standardı
* **Giriş/Çıkış Formatı:** Asterisk AudioSocket standardı olan **Raw PCM, Mono, 8000Hz, 16-bit signed little-endian (s16le)** formatı zorunludur.
* **Resampling (Yeniden Örnekleme):** Sağlayıcılar 16kHz veya 24kHz çalışıyorsa, dönüştürme işlemi anti-aliasing filtreleri (`audioop.ratecv` veya eşdeğeri) ile CPU'yu yormayacak şekilde asenkron tamponlarda (buffers) yapılmalıdır.

---

## 7. Failover ve Rollback Protokolü
* **Dinamik Fallback:** Arama kurulurken birincil sağlayıcı `OPEN` durumundaysa, sistem 15ms içinde otomatik olarak ikincil sağlıklı sağlayıcıyı (`secondary_provider`) seçer.
* **Rollback Switch:** Yeni yönlendirme yapısı üretime alındığında `VOICE_PROVIDER_ABSTRACTION_ENABLED` flag'i ile kontrol edilir. Flag `false` ise sistem doğrudan dondurulmuş tekil Gemini bağlantısına geri döner.

---

## 8. Üretim Kuralları (Production Rules)
1. Barge-in RMS eşiği (varsayılan 3200) ve güvenlik zaman aşımı (12s) değerleri dinamik olarak güncellense bile, çağrı esnasında asla dondurulan limitlerin dışına çıkamaz.
2. API çağrıları için en fazla 1500ms timeout uygulanmalıdır. Timeout durumunda çağrı kesilmeden "Sistemlerimde geçici bir yavaşlık var" mesajıyla devam edilmelidir.
