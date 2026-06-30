# 📂 EAOS Unity Proje Yapısı (UNITY_PROJECT_STRUCTURE)

Bu doküman, `EAOS_Unity_Client` isimli 3D URP Unity projesinin dizin iskeletini ve temel C# scriptlerinin rollerini tanımlar. [UNITY_STARTER_PLAN.md](UNITY_STARTER_PLAN.md) belgesine doğrudan bağlıdır.

---

## 1. Dizin Yapısı (Project Folder Layout)

Unity 6 LTS projesinin ana iskeleti `Assets/EAOS/` altında dondurulmuştur:

* 📂 **Assets/EAOS/Scripts/**: C# controller ve ağ sınıfları.
* 📂 **Assets/EAOS/Prefabs/**: 3D asistan (avatar) ve akıllı arayüz prefab'leri.
* 📂 **Assets/EAOS/Scenes/**: 3D canlandırma ve dijital ikiz sahneleri (`EAOS_Digital_Operations_Center.unity`).
* 📂 **Assets/EAOS/Materials/**: URP uyumlu materyaller.
* 📂 **Assets/EAOS/Avatars/**: FBX modelleri ve Rig ayarları.
* 📂 **Assets/EAOS/Networking/**: gRPC ve WebSocket kütüphaneleri.

---

## 2. Temel C# Sınıfları ve Sorumlulukları

### 1. `EAOSUnityConnector.cs`
* **Görevi:** Unity istemcisinin EAOS AI Gateway ile olan iletişimini yönetir.
* **Kural:** Telefon ses köprüsüne doğrudan bağlanmaz. REST POST veya WebSocket üzerinden mock API kullanarak asenkron veri çeker.

### 2. `EAOSAvatarController.cs`
* **Görevi:** Ajanın duygu durumu verisini (JSON) animasyon tetikleyicilerine (Animator Triggers) çevirerek 3D karakteri hareket ettirir.

### 3. `EAOSLipSyncController.cs`
* **Görevi:** Gelen ses dalgalarından ve viseme (ağız hareketi) verilerinden yola çıkarak avatarın ağız blendshape'lerini asenkron bükerek sesle senkronize dudak hareketi üretir.

### 4. `EAOSSceneSyncController.cs`
* **Görevi:** Dijital İkiz sahnelerindeki ışıklar, sensörler ve kapılar gibi interaktif nesnelerin durumunu AI ajan komutlarıyla senkronize günceller.
