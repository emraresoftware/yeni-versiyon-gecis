# 🛡️ EMA_PROTOTYPE_GUIDE.md (Ema Guardian Prototiplendirme Rehberi)

Bu doküman, `EAOS_Unity_Client` altındaki ilk çalışan **Ema Guardian Prototipi**'nin mimarisini, C# scriptlerini ve test parametrelerini açıklar. [EMA_GUARDIAN_DESIGN.md](EMA_GUARDIAN_DESIGN.md) tasarım anayasasına doğrudan bağlıdır.

---

## 1. Proje Dosyaları ve Yollar (Paths)

* 📂 **Scripts:** `/Users/emre/Elyafgroup/EAOS_Unity_Client/Assets/EAOS/Scripts/`
  * [`EMAController.cs`](file:///Users/emre/Elyafgroup/EAOS_Unity_Client/Assets/EAOS/Scripts/EMAController.cs): Ema'nın Y eksenindeki yumuşak süzülmesini, enerji halkasının durum bazlı rotasyonunu/ölçeğini ve aura ışık rengi geçişlerini yönetir.
  * [`EMAWebSocketMock.cs`](file:///Users/emre/Elyafgroup/EAOS_Unity_Client/Assets/EAOS/Scripts/EMAWebSocketMock.cs): Web arayüzü veya companion sunucusu kapalıyken Unity editörü üzerinde durum simülasyonu ve el-ışık test paneli (OnGUI) sunar.
* 📂 **Prefab:** `/Users/emre/Elyafgroup/EAOS_Unity_Client/Assets/EAOS/Prefabs/`
  * [`EMA_Placeholder.prefab`](file:///Users/emre/Elyafgroup/EAOS_Unity_Client/Assets/EAOS/Prefabs/EMA_Placeholder.prefab): Stilize model hiyerarşisi için iskelet YAML tanımı.
* 📂 **Scene:** `/Users/emre/Elyafgroup/EAOS_Unity_Client/Assets/EAOS/Scenes/`
  * [`EMA_Room.unity`](file:///Users/emre/Elyafgroup/EAOS_Unity_Client/Assets/EAOS/Scenes/EMA_Room.unity): Ema'nın test edildiği karanlık, loş stüdyo ortamı.

---

## 2. Durum (State) Görsel Parametreleri

Durum geçişleri sırasında `EMAController.cs` tarafından otomatik yürütülen kurallar:

1. **Idle (Boşta):** Koyu mavi aura, yavaş süzülme, yavaş dönen halka.
2. **Listen (Dinleme):** Soft Gold (Kehribar) aura ışığı, hafif eğik baş.
3. **Think (Düşünme):** Turkuaz aura, 120 derece hızla dönen enerji halkası, %110 genişleyen halka ölçeği.
4. **Speak (Konuşma):** Parlak Turkuaz aura, 80 derece dönen halka, %120 geniş ölçekli halka.
5. **Celebrate (Onay):** Zümrüt Yeşili aura parlaması.
6. **Error (Hata):** Soft Kırmızı aura parlaması.

---

## 3. Çalıştırma ve Test Adımları
1. Unity 6 LTS editöründe `Assets/EAOS/Scenes/EMA_Room.unity` sahnesini açın.
2. `EMA_Placeholder` objesine `EMAController` ve `EMAWebSocketMock` scriptlerini atayın.
3. Sahnedeki nesneleri (aura ışığı, altın halka transform) script alanlarına sürükleyip bırakın.
4. **Play** butonuna bastığınızda:
   * Karakterin yerçekimsiz süzülme hareketi başlar.
   * Ekranın sol üst köşesinde çıkan GUI paneli (Trigger LISTEN, SPEAK vb.) ile durumları canlı olarak değiştirebilir, anayasal ışık ve hareket tepkilerini anlık doğrulayabilirsiniz.
