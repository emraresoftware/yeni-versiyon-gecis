# 🛡️ EMA_GUARDIAN_DESIGN.md (Ema Guardian Resmi Tasarım Kılavuzu)

Bu doküman, EAOS platformunun resmi görsel kimliği olarak seçilen **Guardian (Koruyucu)** tasarım dilinin 3D modelleme, render, materyal ve animasyon standartlarını dondurur. Diğer tasarımlar iptal edilmiştir. [EMA_FOUNDATION.md](EMA_FOUNDATION.md) belgesine doğrudan bağlıdır.

---

## 1. Silüet ve Oranlar (Silhouette & Proportions)
* **Tanınabilirlik:** Ema, en düşük çözünürlükte veya sadece gölge silüetiyle bile ilk bakışta ayırt edilebilir olmalıdır.
* **Kapüşon (Hood):** Gizemli, siber-koruyucu havayı destekleyen entegre kapüşon yapısı modelin ana karakteridir.
* **Karakter Oranları:** Estetik bir stilizasyon için **küçük gövde, büyük kafa** oranı (chibi/stylized proportion) kullanılacaktır.
* **Ayak Tasarımı:** Karakterin ayakları olmayacaktır.
* **Süzülme:** Karakter, altındaki **altın enerji halkası** üzerinde yerçekimsiz şekilde süzülecektir.

---

## 2. Renk Sistemi (Color Palette)
Ema'nın 3D shader ve kaplamalarında sadece şu 4 kurumsal renk kullanılacaktır:
* **Midnight Black (Gece Siyahı):** Ana gövde ve kapüşon kumaşında (%70 ağırlık).
* **Soft Gold (Yumuşak Altın):** Enerji halkası ve bağlantı eklemlerindeki detaylar.
* **Warm White (Sıcak Beyaz):** Yüz maskesinin yansıttığı ana ışık.
* **Deep Blue Accent (Derin Mavi):** Düşünme veya işlem anlarında auranın yaydığı ikincil renk.

---

## 3. Materyal Standartları (Materials)
* **Nanofiber Kumaş:** Ceket ve kapüşon yüzeyinde mikroskobik dokulu, ışığı emen mat nanofiber kumaş hissi (Fabric Shader).
* **Fırçalanmış Metal (Brushed Metal):** Enerji halkası mekaniklerinde parlamayan, fırçalanmış koyu altın/pirinç detaylar.
* **Işık Geçirgen Yüz:** Yüz maskesi, arkadan gelen LED/ışık verisini yumuşatarak yansıtan yarı-mat opal cam hissi (Subsurface Scattering).
* **Mat Yüzeyler:** Parlak, ucuz hissettiren plastik veya yüksek yansımalı (glossy) malzemeler kesinlikle yasaktır.

---

## 4. Yüz ve Mimik Tasarımı (Face & Expression)
* **Minimalizm:** Ema'nın insan yüzü (burun, kulak, dudak) olmayacaktır.
* **Gözler:** Yüz maskesinin içinden süzülen iki adet stilize ışık çizgisi/halkası şeklinde olacaktır.
* **Ağız:** Ağız kesinlikle görünmeyecektir.
* **Duygu İletişimi:** Tüm duygusal ifadeler göz ışıklarının kısıklığı, rengi ve yüzeydeki mikro ışık dalgalanmalarıyla (subtle emission pulses) aktarılacaktır.

---

## 5. Enerji Halkası ve Süzülme Mekaniği
* **Yürüme Yasağı:** Ema asla adımlayarak yürümeyecektir.
* **Hızlanma:** Karakter hareket ettiğinde altındaki altın enerji halkası genişler ve ışık şiddeti artar.
* **Düşünme Hızı:** Karakter düşünme (`thinking`) moduna geçtiğinde, halka kendi ekseni etrafında yavaşça dönmeye başlar.

---

## 6. Animasyon Kuralları (Animation Standards)
* **Yumuşak Geçiş (Soft Easing):** Tüm hareketlerde `EaseInOut` eğrileri kullanılmalı, ani ivmelenmelerden kaçınılmalıdır.
* **Sessiz Hareket:** Karakterin süzülüşü ve el jestleri son derece akıcı, gürültüsüz ve premium bir süzülme hissi uyandırmalıdır.

---

## 7. Marka Tutarlılığı (Brand Consistency)
* Ema, mobil telefonda da, büyük Kiosk ekranlarında da aynı silüet ve renk kodlarıyla görünmelidir.
* Ekran çözünürlüğüne göre ölçek (scale) değişebilir ancak karakterin anayasal kimliği ve oranları asla değiştirilemez.
