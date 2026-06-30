# 🎮 EAOS Unity Başlangıç Planı (Unity Starter Plan)

Bu plan, **Emare AI Operating System** yapay zeka ajanlarının 3D dünyalar, akıllı Kiosklar ve dijital sunucu (avatar) ortamlarıyla konuşmasını sağlayacak Unity entegrasyonunun ilk aşama planıdır. [CONSTITUTION.md](../CONSTITUTION.md) Faz 2 hedefleri ve [UNITY_CONSTITUTION.md](../constitutions/UNITY_CONSTITUTION.md) kurallarına doğrudan bağlıdır.

---

## 1. Değişmez Sınırlar ve Bağlantı Mimarisi

* **🔒 Ses Köprüsü Koruması:** Üretim ortamında çalışan telefon ses sistemi (`standalone-voice-bridge`) bu entegrasyondan tamamen bağımsızdır ve koduna dokunulmayacaktır.
* **🔒 İzolasyon:** Unity istemcisi ses sistemine doğrudan soket bağlantısı kuramaz. 
* **Haberleşme Hattı:** Unity, tüm veri alışverişini sadece **EAOS AI Gateway / Safe Adapter** üzerinden gerçekleştirir:
  `Unity Client (gRPC/WSS) ──► AI Gateway ──► Safe Adapter ──► Agent Coordinator`

---

## 2. Unity Proje Standartları

Unity tarafındaki tüm geliştirmeler aşağıdaki standartlara sıkı sıkıya uymak zorundadır:

* **Engine Version:** **Unity 6 LTS**
* **Render Pipeline:** **3D Universal Render Pipeline (URP)** (Mobil ve Kiosk cihazlarda yüksek performans için).
* **Git LFS (Large File Storage):** 3D Modeller, FBX animasyonları ve büyük ses dosyaları için Git LFS aktif edilmelidir.
* **Proje Dizin Yapısı:**
  ```
  Assets/EAOS/
  ├── Scripts/      # C# Connector ve animasyon kodları (örn: EAOSUnityConnector.cs)
  ├── Prefabs/      # 3D Avatar ve Kiosk prefab'leri
  ├── Scenes/       # Canlı sahneler (örn: EAOS_Digital_Operations_Center.unity)
  ├── Materials/    # URP materyalleri ve shader'lar
  ├── Avatars/      # 3D Karakter modelleri ve rig'ler
  └── Networking/   # WebSocket/gRPC ağ kütüphaneleri
  ```

---

## 3. Hedef Demo Yol Haritası

### 🎯 Demo 1: Emare AI Avatar + Metin Sohbeti (Text Chat UI)
* **Senaryo:** Kullanıcı Unity arayüzündeki metin kutusuna mesaj yazar, asistan 3D ekranda yazılı olarak cevap verir.
* **Akış:** Unity `EAOSUnityConnector.cs` üzerinden REST POST ile AI Gateway'e istek atar. Gelen JSON yanıtı arayüzdeki chat bubble içine yazılır. Ajanın duygu metadata'sına (örn: `explaining`) göre avatar basit bir el-kol hareketi animasyonu oynatır.

### 🎯 Demo 2: AI Avatar Ses ve Dudak Senkronizasyonu (Lip-Sync)
* **Senaryo:** Asistanın yazılı yanıtının yanında ses dosyası (WAV) ve kelime zamanlamaları (word timestamps) da Unity'ye gelir.
* **Akış:** 
  * AI Gateway, ElevenLabs veya yerel tts üzerinden sesi sentezler, WAV byte dizisini ve altyazı zamanlamalarını JSON içinde döner.
  * Unity sesi `AudioSource` üzerinden oynatırken, C# betiği gelen fonem (viseme) verilerine göre 3D avatarın ağız blendshape'lerini gerçek zamanlı olarak büker (Lip-sync).

### 🎯 Demo 3: Digital Operations Center Sahnesi (Dijital İkiz Kiosk)
* **Senaryo:** `EAOS_Digital_Operations_Center.unity` sahnesinde fabrikanın veya ofisin 3D modeli yer alır.
* **Akış:** Ajan "Depodaki sıcaklık kaç derece?" sorusunu aldığında Unity connector API üzerinden sahnedeki sıcaklık sensörü objesinin değerini okuyup ajana iletir. Ajan "Işıkları yak" dediğinde Unity sahnesindeki 3D ışık kaynağı aktifleşir.

---

## 4. İlk C# Connector Tasarımı (`EAOSUnityConnector.cs`)

Bağlayıcı sınıf, Unity tarafında `MonoBehaviour` olarak tanımlanır ve şunları içerir:
* **`Connect()`**: AI Gateway WebSocket uç noktasına güvenli bağlantı açar.
* **`SendPrompt(string text)`**: Kullanıcı girdisini asenkron olarak gönderir.
* **`OnMessageReceived(string json)`**: Gelen metin, ses ve animasyon komutlarını işleyip ilgili alt sınıflara (lip-sync, animasyon tetikleyici) dağıtır.
