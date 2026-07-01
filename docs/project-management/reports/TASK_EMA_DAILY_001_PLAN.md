# Implementation Plan - TASK-EMA-DAILY-001 Benchmark & Profiling

Ema Desktop Assistant'ı günlük kullanıma hazır bir masaüstü asistanı seviyesine getirmek amacıyla performans (CPU, RAM, Startup), kararlılık (WebSocket kopması, crash) ve sürdürülebilirlik (bellek sızıntısı, uzun süreli açık kalma) metriklerini ölçümleyip raporlama.

## Proposed Benchmark Methodology

### 1. Startup Süresi Ölçümü
- Uygulama başlatılırken `EmareMacAssistantApp.swift` veya `AppState.swift` initialization aşamasında `CFAbsoluteTimeGetCurrent()` ile zaman damgası alınarak ölçülür veya CLI üzerinden `time` aracı ile uygulamanın ayağa kalkış süresi ölçülür.

### 2. İlk Konuşmaya Kadar Geçen Süre
- Uygulama açılıp `connect()` çağrıldıktan WebSocket üzerinden `ready` mesajının alınması ve ilk ses karesinin capture edilip ilk asistan ses paketinin geldiği ana kadar geçen süre (Time to First Voice/Conversation) loglanarak milisaniye cinsinden ölçülecektir.

### 3. CPU & RAM Kullanımı Profilleme
- Uygulama çalışırken macOS yerel `ps` ve `top` komutları kullanılarak süreç (`ProcessID`) bazında CPU yüzdesi ve Resident Memory (RSS) / Virtual Memory boyutu izlenecektir.
- CPU/RAM durumunu her saniye sorgulayıp CSV'ye yazacak bir Python veya Shell profiling script'i (`profile_ema.py`) oluşturulacaktır.

### 4. WebSocket Kopma Testi
- WebSocket bağlantısı aktifken yerel ağ geçici olarak kesilerek veya WebSocket oturumu zorla sonlandırılarak (re-connect timer testi) Ema'nın exponential backoff (`1s → 2s → 4s → 8s`) re-connect döngüsü ve ses motorunun crash olmadan iyileşmesi doğrulanacaktır.

### 5. Uzun Süreli Açık Kalma (8 Saat Simülasyonu)
- Uygulamanın 8 saat boyunca kesintisiz açık kalması ve arka plan thread/queue birikmesi yaşanmaması testi için, yapay yük (mock messages/pings) gönderen bir test simülatörüyle (WebSocket client mock) 8 saatlik ağ ve mesajlaşma yükü simüle edilerek sistem durumu izlenecektir.

### 6. 100 Konuşma (Conversation Load) Testi
- Uygulamaya ardı ardına 100 sesli veya yazılı girdi gönderilerek asistanın yanıt verme sürelerindeki sapmalar ve queue kararlılığı ölçülecektir.

### 7. Memory Leak & Crash Analizi
- Uzun süreli yük sonrası RAM tüketimindeki artış eğrisi izlenerek `malloc` veya `deinit` çağrılarındaki kaçaklar (özellikle AudioBuffer dönüştürme ve WebSocket dinleme döngülerinde) tespit edilecektir.

---

## Proposed Changes

### [New] [profile_ema.py](file:///Users/emre/Elyafgroup/gemini-live-standalone/macos-assistant/scratch/profile_ema.py)
Uygulama sürecinin CPU ve RAM tüketimini, dosya tanımlayıcı (file descriptor) sayılarını izleyecek ve otomatik olarak 100 konuşma yükü simüle edecek test script'i.

### [New] [benchmark_results.md](file:///Users/emre/Elyafgroup/gemini-live-standalone/macos-assistant/scratch/benchmark_results.md)
Tüm ölçüm sonuçlarını, grafik verilerini (ASCII/Markdown formatında), bellek tüketim eğrisini ve kararlılık yorumlarını içeren kapsamlı denetim raporu.

---

## Verification Plan

### Automated Benchmarks
- Profiling script'inin `EmareMacAssistant` binary'sini çalıştırarak CPU ve RAM tüketim loglarını toplaması:
  ```bash
  python3 scratch/profile_ema.py --app-path dist/EmareMacAssistant.app/Contents/MacOS/EmareMacAssistant --duration 300
  ```

### Manual Verification
- Cihaz seçicilerinin ve mikrofon izin iptal senaryolarının UI üzerinden manuel olarak tetiklenmesi ve hata durumlarındaki davranışların gözlenmesi.
