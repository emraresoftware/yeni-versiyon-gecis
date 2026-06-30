# 💻 06_EMA_DESKTOP_ASSISTANT.md (Masaüstü Davranış Standartları)

Bu kılavuz, macOS, Windows ve Linux işletim sistemlerinde arka planda çalışan Ema masaüstü asistanının çalışma kurallarını dondurur.

---

## 1. Arka Plan ve HUD Davranışları
* Ema masaüstünde yarı-şeffaf, penceresiz veya widget formunda ekranın sağ/sol köşesinde yer alabilir.
* Kullanıcı işlem yapmadığında kaynak tüketimini azaltmak için animasyon kare hızı (FPS) otomatik olarak **15 FPS** seviyesine düşürülür. Konuşma başladığında **60 FPS**'e geri döner.

---

## 2. Kısayollar ve Bildirimler (Triggers)
* **Kısayol:** Kullanıcı `Cmd+Space` veya `Ctrl+Space` tuş kombinasyonlarıyla Ema'yı anında uyandırıp dinleme moduna geçirebilir.
* **Ekran Üstü Bildirim (HUD):** Ema, arka planda bir olay (örn: yeni bilet atandı) tespit ettiğinde ekranın üstünde yumuşak bir bildirim kartı açar ve hafif bir ses tonuyla kullanıcıyı bilgilendirir.
