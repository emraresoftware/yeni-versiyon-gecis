# 🎨 02_EMA_VISUAL_GUIDE.md (Görsel ve Işık Tasarım Rehberi)

Ema'nın 3D modellerinin, materyallerinin ve ışıklandırma parametrelerinin standartlarını tanımlar.

---

## 1. Görsel Tasarım Standartları
* **URP Uyumluluğu:** 3D model, Unity URP shader'ları ile optimize edilmiş düşük poligon (low-poly) veya stilize orta poligon (mid-poly) yapısında olmalıdır.
* **Göz Teması (LookAt):** Karakterin gözleri ve baş yönü, her zaman sahnedeki aktif kameraya veya kiosk kullanıcısına doğru kilitlenmelidir.

---

## 2. Işık ve Renk Davranışları
Karakterin etrafındaki yumuşak ışık çemberi (aura/rim light) durumunu yansıtır:
* **Mavi / Turkuaz:** Normal durum, işlem yapma.
* **Yumuşak Sarı:** Kullanıcıyı dinleme (`listening`) modu.
* **Yeşil:** Başarılı işlem tamamlama teyidi.
* **Soft Kırmızı:** Hata veya bağlantı kaybı durumu.
