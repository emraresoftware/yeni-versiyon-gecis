# 🏃 03_EMA_ANIMATION_GUIDE.md (Animasyon Standartları Kılavuzu)

Bu kılavuz, Ema'nın 3D hareket akışkanlığı, kemik rig standartları ve geçiş yumuşaklıklarını belirler.

---

## 1. Akışkanlık Kuralları
* Animasyonlar arası geçişler (transitions) Unity Animator Blend Trees kullanılarak en az **0.25 saniyelik** yumuşak sönümlemelerle (damping) yapılmalıdır. Ani, keskin ve robotik duruş geçişleri yasaktır.
* Karakterin rig yapısı standart **Humanoid** şablonuna tam uyumlu olmalıdır.

---

## 2. Mikro Animasyonlar (Idle Additives)
* Ema tamamen sabit duramaz. Konuşmadığı anlarda dahi göz kırpma, nefes alma ve hafif ağırlık merkezini değiştirme (sway) gibi ikincil animasyonlar arka planda sürekli çalışmalıdır.
