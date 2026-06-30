# 🎮 07_EMA_UNITY_GUIDE.md (Unity Entegrasyon Rehberi)

Ema'nın 3D model ve animasyonlarının Unity 6 LTS ve 3D URP projelerine nasıl dahil edileceğini tanımlar.

---

## 1. 3D Karakter Yapılandırması
* Model standart Unity **Humanoid Rig** yapısında olmalıdır.
* Göz hareketleri için `Eye LookAt` kısıtlayıcıları (constraints) kamera konumuna bağlanmalıdır.

---

## 2. Blendshape ve Ağız Hareketleri (Lip-Sync)
* Avatar mesh'i üzerinde ağız hareketleri için en az 5 temel fonem blendshape'i (`A`, `E`, `O`, `I`, `U`) bulunmalıdır.
* `EAOSLipSyncController.cs` betiği, WebSocket'ten gelen RMS genlik verilerine göre bu blendshape ağırlıklarını anlık günceller.
