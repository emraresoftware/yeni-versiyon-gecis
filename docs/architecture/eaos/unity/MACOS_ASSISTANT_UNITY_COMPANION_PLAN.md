# 💻 macOS Assistant Unity Companion Plan (Görsel Katman Entegrasyon Planı)

Bu plan, mevcut Swift tabanlı native **Emare macOS Assistant** uygulaması ile 3D Unity motorunun bir arada çalışarak, sesli görüşmeyi Swift tarafında yönettiği, görsel ve animasyon katmanını ise Unity'nin üstlendiği **Companion (Eşlikçi)** mimarisini tanımlar. [CONSTITUTION.md](../CONSTITUTION.md) Faz 2 ve [UNITY_CONSTITUTION.md](../constitutions/UNITY_CONSTITUTION.md) kurallarına doğrudan bağlıdır.

---

## 1. Mevcut macOS Assistant Mimarisi
* **UI & State:** SwiftUI (`ContentView` & `AppState`).
* **Audio Engine:** `AVAudioEngine` ile ham mikrofon sesini toplama ve ElevenLabs'ten gelen sesi oynatma.
* **ElevenLabs Connection:** Doğrudan ElevenLabs ConvAI WebSocket uç noktasına güvenli bağlantı.
* **Barge-in:** Ses dalgalanmalarına ve ElevenLabs kesme (interruption) sinyallerine göre asistanın sesini anında durdurma.

---

## 2. Unity Companion Rolü (Görsel Katman)
* **🔒 İzolasyon Kuralı:** Unity hiçbir şekilde ElevenLabs'e, veritabanına veya telefon ses köprüsüne doğrudan bağlanmaz. Mikrofon donanımını açmaz.
* **Sorumluluk:** Unity sadece **görsel bir katmandır**. Swift uygulamasından WebSocket üzerinden gelen anlık durum (state), metin dökümü (transcript) ve ses genliği (audio amplitude) verilerini okuyarak 3D avatar animasyonunu ve lip-sync hareketlerini tetikler.

---

## 3. SwiftUI ↔ Unity Haberleşme Seçenekleri

| Seçenek | Gecikme (Latency) | Güvenlik / Sandbox | Unity Entegrasyon Kolaylığı | Karar |
|---|---|---|---|---|
| **A. Local WebSocket (Port 8097)** | < 3ms | Sandbox uyumlu, kolay geçiş. | Çok Kolay (Native C# WebSocket). | **ÖNERİLEN (SEÇİLDİ)** |
| **B. Unix Domain Sockets** | < 1ms | İzin yönetimi gerekir. | Orta (C# soket wrapper). | Fallback |
| **C. Named Pipes / Shared Memory**| < 1ms | Sandbox kısıtlamaları var. | Zor. | Elendi |

* **Karar Gerekçesi:** Swift uygulaması arka planda `Network.framework` ile yerel bir WebSocket Sunucusu (localhost:8097) başlatır. Unity istemcisi bu sunucuya bağlanır. Hem düşük gecikme sağlanır hem de Apple App Sandbox kurallarına tam uyum sağlanır.

---

## 4. Avatar State Mapping (Durum Eşleme)

Swift tarafındaki `AppState` değişiklikleri, Unity'ye JSON paketleri halinde gönderilir ve 3D karaktere eşlenir:

| Swift AppState | Unity State | Unity 3D Avatar Davranışı |
|---|---|---|
| `idle` | `Idle` | Nefes alma, göz kırpma, hafif vücut salınımı. |
| `connecting` | `Connecting` | Etrafa bakınma, hafif meraklı bekleyiş. |
| `listening` | `Listening` | Kafasını hafifçe öne eğme, odaklanma animasyonu. |
| `thinking` | `Thinking` | Eli çeneye götürme, düşünme animasyonu. |
| `speaking` | `Speaking` | Konuşma jestleri, lip-sync aktif. |
| `interrupted` | `Interrupted` | Şaşırma/duraksama, konuşma ve ağız hareketinin anında durması. |
| `error` | `Error` | Üzgün/özür dileyen jest, kırmızı durum göstergesi. |

---

## 5. Entegrasyon Aşamaları (Integration Phases)

### 🚀 Phase 1: Swift AppState → Unity Avatar State (Durum Senkronizasyonu)
* **Swift Görevi:** `AppState` her değiştiğinde (örn: `listening` -> `speaking`) lokal WebSocket sunucusu üzerinden Unity'ye durum paketi gönderir: `{"type": "state", "value": "speaking"}`.
* **Unity Görevi:** `EAOSUnityConnector.cs` paketi alır, `EAOSAvatarController.cs` betiğini tetikleyerek animator üzerindeki trigger'ı aktif eder.

### 🚀 Phase 2: Transcript → Unity Chat Bubble (Yazılı Balonlar)
* **Swift Görevi:** ElevenLabs'ten gelen transcript paketlerini okur ve anında Unity'ye paslar: `{"type": "transcript", "role": "assistant", "text": "Merhaba Ahmet Bey..."}`.
* **Unity Görevi:** Karakterin üzerinde veya ekranın altında yer alan 3D/2D konuşma balonunu günceller.

### 🚀 Phase 3: Audio Amplitude → Lip-Sync (Dudak Senkronizasyonu)
* **Swift Görevi:** Hoparlöre ses basılırken, anlık RMS ses genliğini (amplitude) hesaplar (her 20ms'de bir) ve Unity'ye gönderir: `{"type": "amplitude", "value": 0.75}`.
* **Unity Görevi:** `EAOSLipSyncController.cs` gelen genlik değerine göre karakterin ağız blendshape ağırlığını (`weight`) anlık olarak büker. Ek bir ses sentezine gerek kalmadan sıfır gecikmeli lip-sync gerçekleşir.

---

## 6. MVP Kontrol Listesi (Checklist)

* [ ] Swift uygulamasında localhost:8097 portunda WebSocket Server aktifleştirilmesi.
* [ ] Unity `EAOSUnityConnector` sınıfının bu sunucuya bağlanması.
* [ ] Durum geçişlerinin (idle -> listening -> speaking) 3D model üzerinde animasyon tetiklemesi.
* [ ] Ses genliği (`amplitude`) paketlerinin Unity ağız blendshape'ini oynattığının doğrulanması.
* [ ] Araya girme (Barge-in) anında Unity animasyonunun ve ses genliği akışının anında sıfırlandığının (interrupted) teyit edilmesi.
