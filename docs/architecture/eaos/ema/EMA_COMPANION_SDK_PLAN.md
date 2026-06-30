# 📦 EMA_COMPANION_SDK_PLAN.md (Ema Companion SDK Yol Haritası)

Bu plan, Ema'nın tüm hedef platformlarda (macOS, Windows, Linux, Web, Unity, Vision Pro, Mobile) aynı kimlik, zeka ve görsel standartlarla çalışmasını sağlayacak olan **Ema Companion SDK** yapısını tanımlar.

---

## 1. SDK Hedef Platformlar ve Dağıtım
SDK, her platform için optimize edilmiş yerel kütüphaneler (wrapper'lar) barındıran ortak bir C++ Core veya Rust Core olarak tasarlanır:
* **Desktop (macOS/Win/Linux):** C# (WPF/WinForms) ve Swift (SwiftUI) bağlayıcıları.
* **Web (Webchat Widget):** WebGL ve WebAssembly (WASM) tabanlı hafif tarayıcı kütüphanesi.
* **Unity & Vision Pro:** Unity C# SDK paketi.
* **Mobile (iOS/Android):** Kotlin/Swift native kütüphaneleri.

---

## 2. Ortak Davranış Kuralları (Universal Behaviors)
* **Senkronize State:** SDK, hangi platformda çalışırsa çalışsın `EMA_MOVEMENT_SYSTEM.md` içindeki durum makinesi kurallarına tam olarak uyar.
* **Hafıza Taşınabilirliği:** Kullanıcının Ema ile olan konuşma bağlamı ve öğrenilen alışkanlıkları, platformlar arasında bulut hafıza servisleri (`Memory Service`) üzerinden şifreli olarak taşınır.
* **Ses ve Lip-Sync Senkronizasyonu:** Tüm platformlar, ses dalgasını okuyarak fonem eşleme algoritmalarını yerel cihazın CPU'sunu yormayacak şekilde çalıştırır.
