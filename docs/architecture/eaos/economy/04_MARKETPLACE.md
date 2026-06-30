# 🛍️ 04_MARKETPLACE.md (Pazar Yeri Finansal Standartları)

Eklenti, hizmet ve yapay zeka taslaklarının satıldığı pazar yeri (Marketplace) ödeme ve komisyon kurallarını belirler.

---

## 1. Wallet Entegrasyonu ve Ödemeler
* Marketplace üzerindeki tüm satın alma işlemleri doğrudan platform cüzdanı üzerinden token veya fiat karşılığı akıllı kontratlar (smart contracts) ile yürütülür.
* **Escrow (Güvence Hesabı):** Satın alınan eklentinin lisans ücreti, eklenti kiracının sistemine kurulup `MODULE_CERTIFICATION.md` kurallarına göre onaylanana kadar güvence havuzunda (escrow) bekletilir.

---

## 2. Dağıtıcı ve Geliştirici Payları
* Marketplace satışlarından platform %15 komisyon alır, kalan %85 geliştiricinin cüzdanına anında asenkron olarak aktarılır.
