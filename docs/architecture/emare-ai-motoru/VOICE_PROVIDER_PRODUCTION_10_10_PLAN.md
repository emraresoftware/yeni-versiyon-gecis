# 🎙️ VOICE PROVIDER PRODUCTION 10/10 PLAN

Bu plan, **Emare AI Voice Bridge** altyapısını tek bir sağlayıcıya bağımlı olmaktan çıkarıp, birden fazla sağlayıcıyı (Gemini Live, OpenAI Realtime vb.) sıfır kesinti, dinamik puanlama ve hata koruması (circuit breaker) ile yönetebilen **10/10 üretim kalitesinde** bir Ses Sağlayıcı Soyutlama Katmanına dönüştürmek amacıyla hazırlanmıştır.

---

## 1. Voice Core Isolation (Ses Çekirdeği İzolasyonu)

* **Bağımsız Çalışma:** Python ses köprüsü (`standalone-voice-bridge`) ana C# API'sinden ve diğer tüm mikrosistemlerden (Unity, Video, ERP, CRM) tamamen izole çalışacaktır.
* **Gevşek Bağlılık (Hard-dependency Kaldırılması):** 
  * Arama başında API'ye gidip veri alamaması (timeout veya servis çökmesi) durumunda, ses köprüsü aramayı reddetmeyecek; yerel veya dondurulmuş ayarlarla (`SEALED_SETTINGS.md`) ve varsayılan Gemini API key ile aramayı açacaktır.
  * Müşteri adı veritabanından çözülemezse, çağrıya *"Merhaba"* veya *"Acarcell'e hoş geldiniz"* gibi genel bir şablonla başlanacaktır.
* **Çevrimdışı Mod (Fallback):** Merkezi Event Bus veya veri tabanı çökerse, asistan araç çağırma (tool call) yeteneğini geçici olarak devre dışı bırakıp sadece konuşma akışını sürdürecektir.

---

## 2. Provider Scoring (Sağlayıcı Puanlama Modeli)

Her sağlayıcı (`provider`) için arama başında dinamik bir ağırlıklı puan hesaplanır:

$$\text{Score} = (W_l \times S_{latency}) + (W_e \times S_{error}) + (W_a \times S_{avail}) + (W_c \times S_{cost}) + S_{policy}$$

### Metrik Kriterleri:
* **`latency_ms`:** Son 10 WebSocket ping süresinin hareketli ortalaması. Gecikme arttıkça puan düşer.
* **`error_rate`:** Son 100 işlemdeki hata yüzdesi. Hata oranı yükseldikçe puan sert şekilde düşer.
* **`availability`:** Sağlayıcının anlık ayakta olma durumu (Uptime / Health check sonucu).
* **`reconnect_count`:** Son 1 saat içindeki WebSocket bağlantı kopma ve tekrar bağlanma sayısı.
* **`realtime_rtt`:** Ses paketlerinin gidiş-dönüş süresi.
* **`tenant_policy`:** Kiracının o sağlayıcı için belirlediği öncelik katsayısı (Acar Telekom için Gemini = +50, OpenAI = 0 vb.).
* **`cost_weight`:** Sağlayıcının birim fiyat katsayısı (Düşük maliyetli sağlayıcıya pozitif puan).
* **`region`:** Sağlayıcı sunucusunun konumu (Türkiye'ye en yakın lokasyona ek puan).
* **`last_failure`:** Son hatadan bu yana geçen süre. Eğer son 5 dakikada hata alındıysa geçici ceza puanı verilir.

---

## 3. Circuit Breaker (Hata Devre Kesici)

Her sağlayıcı bağımsız bir durum makinesine (`state model`) sahiptir:

```
        3 Ardışık Hata
     ┌───────────────────► OPEN ────────────────────┐
     │                      │                       │
     │                      │ Cooldown Süresi       │
   CLOSED                   │ (~30 Saniye)          │
     ▲                      ▼                       ▼
     │                 HALF_OPEN ◄──────────────────┘
     │                      │
     └──────────────────────┘
         Başarılı Sağlık Testi
```

### Durum Kuralları:
1. **`CLOSED` (Normal):** Trafik bu sağlayıcıya serbestçe akar.
2. **`OPEN` (Kesik):** Sağlayıcıda arka arkaya **3 hata** alındığında devre `OPEN` konumuna geçer. Bu sağlayıcı puanlama dışı bırakılır ve yeni çağrılar buna yönlendirilmez.
3. **`HALF_OPEN` (Yarı Açık):** `OPEN` konumuna geçtikten 30 saniye sonra devre kendini dener. Gelen ilk yeni çağrıyı veya asenkron ping testini bu sağlayıcıya gönderir.
   * **Başarılı olursa:** Tekrar `CLOSED` konumuna döner ve tam trafiğe açılır.
   * **Hata verirse:** Anında `OPEN` konumuna geri döner ve bekleme süresi katlanarak (60s, 120s) artar.

---

## 4. Session Sticky Rule (Oturum Sabitleme Kuralı)

* **Çağrı Başında Sabitleme:** Sağlayıcı seçimi sadece çağrının kurulma anında (`SIP INVITE / AudioSocket TCP` bağlantısı geldiğinde) yapılır.
* **Geçiş Yasağı:** Arama başladıktan sonra, konuşma esnasında kesinlikle sağlayıcı değiştirilmez. Hatta kalma esnasında oluşabilecek ufak kopmalarda aynı sağlayıcı ile `reconnect` denenir.
* **Fallback Sınırı:** Hata alan bir sağlayıcıdan diğerine geçiş (failover), sadece **yeni gelen çağrılar** için uygulanır. Aktif aramadaki müşteri bu geçiş hissini ve ses karakteri değişimini yaşamaz.

---

## 5. Low Latency Rule (Düşük Gecikme Kuralları)

* **Kısa Ses Yolu:** Ses paketleri hiçbir aracı mikroservise uğramadan doğrudan şu yolu izleyecektir:
  `Asterisk (PCM 8kHz) ──► standalone-voice-bridge (PCM 16kHz) ──► AI Provider (WebSocket)`
* **Gereksiz Bağımlılıkların Engellenmesi:** Gerçek zamanlı ses akışı sırasında Event Bus, Workflow Engine, log analizörleri gibi katmanlar ses hattını bloke edemez. Tüm bu işlemler asenkron olarak arka plana (`asyncio.create_task`) atılır.
* **Araç Çalıştırma (Tool Execution) Koruması:** Ajan bir araç çağırdığında (örn: bilet sorgulama), API'ye 1500ms limitli asenkron bir `timeout` uygulanır. Süre aşılırsa "Şu an sisteme ulaşamıyorum" yanıtı verilir, ses kanalı kilitlenmez.

---

## 6. Provider Adapter Interface (Standart Arayüz)

Tüm gerçek zamanlı sağlayıcı adaptörleri aşağıdaki standart arayüzü (`Protocol`) birebir uygulamalıdır:

```python
class VoiceSession(Protocol):
    async def connect(self, model: str, config: dict) -> VoiceSession:
        """Gerçek zamanlı bağlantı açar."""
        ...
    async def send_realtime_input(self, audio: bytes) -> None:
        """Mikrofon sesini ham pcm olarak gönderir."""
        ...
    async def send(self, input: Any, end_of_turn: bool = True) -> None:
        """Yazılı komut veya yönlendirme mesajı gönderir."""
        ...
    async def send_client_content(self, turns: Any, turn_complete: bool = True) -> None:
        """Kullanıcı turn içeriği gönderir."""
        ...
    def receive(self) -> AsyncIterator[Any]:
        """Sağlayıcı yanıtlarını yield eden asenkron akış."""
        ...
    async def close(self) -> None:
        """Bağlantıyı kapatır."""
        ...
    async def health_check(self) -> bool:
        """Sağlayıcının anlık erişilebilirliğini doğrular."""
        ...
```

---

## 7. Tenant Voice Policy (Kiracı Ses Politikası)

Her tenant için DB veya JSON üzerinden tanımlanabilecek esnek ses kuralları şablonu:

```json
{
  "tenant_id": "505b2e47-62df-417f-ad98-8115b3206e2b",
  "voice_policy": {
    "primary_provider": "gemini",
    "secondary_provider": "openai",
    "max_latency_ms": 350,
    "preferred_region": "eu-central-1",
    "allow_fallback": true,
    "cost_priority": false,
    "quality_priority": true
  }
}
```

---

## 8. Observability (İzlenebilirlik)

Arama bittiğinde veya canlı izleme paneline gönderilmek üzere aşağıdaki metrikler OpenTelemetry standartlarında loglanır:

1. **`selected_provider`**: O aramada seçilen sağlayıcı (gemini / openai).
2. **`provider_score`**: Sağlayıcının arama başındaki toplam puanı.
3. **`connection_latency_ms`**: WebSocket el sıkışma (handshake) süresi.
4. **`first_audio_latency_ms`**: Arama başladıktan sonra sağlayıcıdan gelen ilk ses chunk'ının ulaşma süresi.
5. **`interruption_latency_ms`**: Barge-in kesme sinyalinin sağlayıcıya iletilip asistan sesinin durdurulma süresi.
6. **`tool_latency_ms`**: Ajanın kullandığı fonksiyonların (API çağrılarının) yanıtlanma süresi.
7. **`provider_errors`**: Arama sırasında sağlayıcının fırlattığı hata logları.
8. **`call_duration`**: Toplam çağrı süresi.
9. **`disconnect_reason`**: Bağlantı kopma nedeni (hangup / provider-error / timeout).

---

## 9. Safe Rollback (Güvenli Geri Dönüş ve Feature Flag)

Yeni adaptör katmanının üretime alınması sırasında yaşanabilecek her türlü olumsuzluğa karşı **Feature Flag** ve **Rollback** mekanizması kurulur:

* **Feature Flag:** Ortam değişkeni (env) üzerinden kontrol edilir:
  `VOICE_PROVIDER_ABSTRACTION_ENABLED=true` (varsayılan: `false`)
* **Rollback Davranışı:**
  * Eğer `VOICE_PROVIDER_ABSTRACTION_ENABLED` değeri `false` ise, ses köprüsü yeni yönlendiriciyi (`VoiceProviderManager`) tamamen atlar.
  * Doğrudan eski, stabil çalışan, tekil Gemini GenAI SDK bağlantısına (`client.aio.live.connect`) geri döner.
  * Bu sayede yeni kod üzerinde hata çıksa bile sunucuyu durdurmadan tek bir env parametresiyle saniyeler içinde eski sürüme geri dönülebilir.

---

## 10. Implementation Checklist (Geliştirme Yol Haritası)

### 📋 Phase 1: Dokümantasyon (Tamamlandı)
* [x] `VOICE_PROVIDER_PRODUCTION_10_10_PLAN.md` oluşturulması ve mimarinin dondurulması.

### 📋 Phase 2: Circuit Breaker Sınıfı
* [ ] `circuit_breaker.py` modülünün yazılması.
* [ ] CLOSED, OPEN, HALF_OPEN durumlarının ve cooldown sayaçlarının implementasyonu.

### 📋 Phase 3: Provider Scoring Sınıfı
* [ ] `provider_scorer.py` yazılması.
* [ ] Ping ve hata oranına göre dinamik puanlama algoritmasının kurulması.

### 📋 Phase 4: Health Check Sistemi
* [ ] Sağlayıcılara arka planda 30 saniyede bir hafif ping atan asenkron background task eklenmesi.

### 📋 Phase 5: Feature Flag Entegrasyonu
* `standalone_bridge.py` içinde `VOICE_PROVIDER_ABSTRACTION_ENABLED` flag kontrolünün eklenmesi.

### 📋 Phase 6: Staging Testleri
* [ ] Staging sunucusunda (`85`) gölge arama testlerinin yapılması.
* [ ] Hata simülasyonu yapılarak circuit breaker'ın trafiği kestiğinin izlenmesi.

### 📋 Phase 7: Production Kontrollü Geçiş
* [ ] Prod sunucularında feature flag aktif edilerek kademeli devreye alım.
* [ ] OpenTelemetry ve log analizlerinin canlıda izlenmesi.
