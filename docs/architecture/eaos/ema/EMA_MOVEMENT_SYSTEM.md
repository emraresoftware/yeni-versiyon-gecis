# 🏃 EMA_MOVEMENT_SYSTEM.md (Ema Hareket ve Durum Makinesi)

Bu doküman, Ema'nın tüm platformlarda uygulayacağı Durum Makinesi (State Machine) animasyon, göz, el ve ışık kurallarını dondurur.

---

## Durum Makinesi (State Machine) Parametreleri

| State | Animasyon Davranışı | Göz Davranışı | El Davranışı | Işık Modu (Aura) | Ses Efekti |
|---|---|---|---|---|---|
| **Idle** | Hafif nefes alma, sway. | Kamera LookAt kilitli. | Gövde yanında serbest. | Sabit Koyu Mavi | Sessiz |
| **Wake** | Uyanma, dikleşme. | Kamerayı bulma, odaklanma. | Hafif selamlama jesti. | Turkuaz Parlama | Soft bip tonu |
| **Listen** | Kafa hafif eğik. | Göz kırpma aktif. | Parmaklar birleşik/dinlemede.| Sarı / Kehribar | Sessiz |
| **Think** | Kafa hafif yana yatık. | Göz kısıklığı %15. | Eli çeneye götürme. | Dönen Mavi Aura | Derin vum sesi |
| **Speak** | Konuşma blend tree. | Kameraya odaklanma. | Anlatım jestleri (lip-sync).| Parlak Turkuaz | Ses çıkışı aktif |
| **Celebrate**| Tebrik duruşu, dikleşme. | Gülümseme aktif. | Hafif başparmak yukarı. | Zümrüt Yeşili | Başarı melodisi |
| **Notify** | Kullanıcıya yönelme. | Gözler bildirim kartında. | Bildirimi işaret etme. | Parlak Mavi | Bildirim tonu |
| **Sleep** | Eğilme, sönümlenme. | Gözler kapalı. | Kucağa çekilmiş eller. | Çok Koyu Mavi | Sönümlenen ton |
| **Error** | Üzgün duruş. | Gözler hafif aşağıda. | İki el önde birleşik. | Yumuşak Kırmızı | Hata uyarı tonu |
