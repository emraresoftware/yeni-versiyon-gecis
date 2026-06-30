# 🎭 05_EMA_EMOTION_ENGINE.md (Duygu Motoru Tasarımı)

Bu belge, Ema'nın metin ve ses tonundaki duygu durumlarını yüz mimiklerine (Blendshapes) ve vücut diline dönüştüren motor kurallarını tanımlar.

---

## 1. Duygu Geçiş Şeması (Emotion Mapping)
Ema, o anki konuşma durumuna göre `Animator` parametrelerini ve yüz blendshape ağırlıklarını günceller:

* **Neutral (Nötr):** Blendshape ağırlıkları sıfır. Standart kurumsal bakış.
* **Attentive (Dinleme):** Kaşlar hafif kalkık, kafa 3 derece öne eğik.
* **Thoughtful (Düşünme):** Göz kısıklığı %15, bakış hafif yukarıda.
* **Empathetic (Üzgün/Anlayışlı):** Kaş uçları yukarıda, dudak kenarları %10 aşağıda.
* **Cheerful (Gülümseme):** Dudak kenarları (smile blendshape) %40 yukarıda, göz çevresi yumuşak.

---

## 2. Lip-Sync Senkronizasyonu (Fonem Eşleme)
* Ses oynatılırken ElevenLabs'ten veya ses motorundan gelen ses genliği (Amplitude) anlık olarak ağız açıklığı blendshape ağırlığına (0 - 100) dönüştürülerek dudak senkronizasyonu sağlanır.
