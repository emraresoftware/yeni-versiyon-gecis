# 🎮 UNITY_CONSTITUTION.md (EAOS Unity Entegrasyon Anayasası)

Bu anayasa, EAOS yapay zeka ajanlarının 3D dünyalar, Kiosklar ve Dijital İkiz (Digital Twin) uygulamalarıyla konuşmasını sağlayan Unity Game Engine bağlantı standartlarını belirler. [CONSTITUTION.md](../CONSTITUTION.md) Madde I.4 ve Faz 2 hedeflerine doğrudan bağlıdır.

---

## 1. Unity Runtime & Digital Twin
* EAOS, fiziksel tesislerin, fabrikaların veya mağazaların 3D durum verilerini (dijital ikiz) okuyarak ajanlara bağlam (context) olarak sunabilir.
* Unity istemcileri, sahnedeki objelerin durum değişikliklerini EAOS API'lerine gerçek zamanlı gRPC veya WebSocket streams ile bildirmelidir.

---

## 2. AI Avatar & Animasyon Yönetimi
* **Duygu Durumu (Emotional State):** Ajanın ürettiği yanıtın yanında dönen duygu ve jest verileri (örn: `neutral`, `happy`, `explaining`) standart bir JSON/Protobuf şeması ile Unity'ye iletilmelidir.
* **Blendshapes & Lip-Sync:** Gerçek zamanlı konuşmada, ses dalgaları (audio amplitude/frequencies) veya fonem (phoneme) verileri eşzamanlı olarak Unity'ye gönderilerek karakterin dudak hareketleri (lip-sync) 3D blendshape'ler aracılığıyla milisaniyelik hassasiyetle oynatılmalıdır.

---

## 3. Ses ve Sahne Senkronizasyonu (Voice & Scene Sync)
* **Gecikme Limiti:** Ajan konuşmaya başladığı an ile Unity karakterinin konuşma animasyonunun başlaması arasındaki gecikme **< 100ms** olmalıdır.
* **Durum Senkronizasyonu:** Ajan "Işıkları kapatıyorum" dediğinde, Unity sahnesindeki ışık objesi ile veritabanındaki durum eşzamanlı olarak (Scene Sync) güncellenmelidir.

---

## 4. Performans ve Optimizasyon
* **Hafif Ağ Paketleri:** Protokol paketleri büyük JSON'lar yerine hafif, serialize edilmiş **Protobuf** formatında olmalıdır.
* **Frame Rate Koruma:** Unity tarafındaki haberleşme kodları ana render thread'ini (Main Thread) bloke etmemeli, asenkron `Coroutines` veya `C# Tasks` (UniTask) ile background thread'lerde çalışmalıdır.
