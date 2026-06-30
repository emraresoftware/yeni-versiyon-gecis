# 🎮 09_UNITY_BLUEPRINT.md (Unity Companion Kurulum Şablonu)

Bu kılavuz, kiracının akıllı ekran ve Kiosk cihazlarına kurulacak olan Unity 3D URP asistan uygulamasının yapılandırma adımlarını içerir.

---

## 1. Donanım ve Sahne Ayarları
* Hedef cihaz çözünürlüğü ve ekran kartı gücüne göre URP grafik profili (Low, Medium, High) seçilir.
* Kiosk donanımının ses çıkışları test edilerek `AudioSource` atamaları yapılır.

---

## 2. API Gateway Bağlantısı
* Unity projesindeki `EAOSUnityConnector.cs` dosyasında, kiracının özel AI Gateway URL'si ve API Token'ı yapılandırılır.
