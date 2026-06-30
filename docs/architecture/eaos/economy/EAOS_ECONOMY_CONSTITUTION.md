# 🪙 EAOS_ECONOMY_CONSTITUTION.md (EAOS Ekonomi Anayasası)

Bu anayasa, **Emare AI Operating System** ekosisteminin finansal ve ekonomik kurallarını belirleyen en üst düzey referans belgesidir. Platformun modüler yapısına uygun olarak, token'ı bir yatırım aracı değil, tamamen bir **hizmet faydası (utility)** olarak konumlandırır. [CONSTITUTION.md](../CONSTITUTION.md) ve [01_ECONOMY_FOUNDATION.md](01_ECONOMY_FOUNDATION.md) belgelerine doğrudan bağlıdır.

---

## 1. Vision (Vizyon)
EAOS Ekonomi vizyonu; işletmelerin otonom yapay zeka operasyonlarını, küresel ve merkeziyetsiz bir değer takas katmanı üzerinden, sıfır sürtünme ve milisaniyelik mikro ödemelerle ölçeklendirebilmesini sağlamaktır.

---

## 2. Economy Principles (Ekonomi İlkeleri)
* **Yatırım Aracı Değildir:** EAOS yerel token'ı kesinlikle spekülatif bir yatırım aracı olarak tanımlanamaz ve pazarlanamaz. Öncelik her zaman gerçek dünya kullanımıdır (utility-first).
* **Token Olmadan Çalışabilme (Non-mandatory):** Platformun temel işlevleri (CRM, ERP, çağrı karşılama) token olmadan da geleneksel lisans ve fiat para birimleriyle tam kapasite çalışabilir.
* **Katma Değer Odaklılık:** Token, sadece ek özellikler, gelişmiş video işleme, API entegrasyon pazarı ve üçüncü taraf eklenti lisansları için kullanılır.
* **Vendor Lock-in Karşıtlığı:** Ödeme altyapısı hiçbir sağlayıcıya (stripe, bankalar, belirli blokzincir) bağımlı değildir; modüler adaptörlerle çalışır.

---

## 3. Wallet Architecture (Cüzdan Mimarisi)
* Tüm platformlarda (Desktop, Web, Unity, Mobile) ortak kriptografik anahtar (ECDSA/Ed25519) standartlarını kullanan, tekil veya çoklu yetkilendirmeyi (Multi-sig) destekleyen ortak bir `Universal Wallet` arayüzü zorunludur.

---

## 4. Credit System (Kredi Sistemi)
* Kullanıcılar fiat para birimleri veya token ile "AI Kredisi" satın alabilirler. 
* Kredi sistemi, platform içi AI hesaplama maliyetlerini (token girdi/çıktı) ve ses/video sentezleme milisaniyelerini birleştiren standart bir iç para birimi gibi çalışır.

---

## 5. Token Utility (Token Faydası)
Token'ın platformdaki 3 ana görevi:
1. **Gas Fee (İşlem Ücreti):** Ajanların otonom workflow çalıştırma ücretlerinin ödenmesi.
2. **Access (Erişim):** Gelişmiş multi-agent koordinasyon odalarına ve premium araçlara erişim hakkı.
3. **Staking:** Eklenti pazarında yayıncı olmak ve API güvenliğini doğrulamak için teminat sağlama.

---

## 6. Marketplace Economy (Pazar Yeri Ekonomisi)
* Üçüncü taraf geliştiriciler eklentilerini satarken akıllı kontrat lisanslama modelini kullanır.
* Satış gelirlerinin %85'i geliştiriciye, %15'i ise platform hazinesine aktarılarak ekosistem fonu olarak değerlendirilir.

---

## 7. Partner Program (İş Ortaklığı Programı)
* Sistem entegratörleri ve danışmanlık ajansları (The Agency), kiracıları platforma kazandırdıkça ve onların sistemlerini optimize ettikçe havuzdan komisyon/ödül almaya hak kazanırlar.

---

## 8. Creator Economy (Geliştirici Ekonomisi)
* Ajanların en çok kullandığı ve en yüksek başarı oranına sahip olan araçları (tools) yazan bağımsız geliştiriciler, kullanım başına mikro-telif ödemeleri (micro-royalties) alırlar.

---

## 9. AI Usage Credits (Yapay Zeka Tüketimi)
* API istekleri anlık olarak `Usage Meter` tarafından token ve milisaniye bazında hesaplanır, Safe Adapter onayıyla bakiye tablosundan asenkron düşülür.

---

## 10. Video Credits (Video Sentezleme Kredileri)
* HeyGen/Tavus gibi video API sağlayıcılarının render maliyetleri saniye bazlı olarak kiracının video kredilerinden düşülür.

---

## 11. Licensing (Lisanslama Standartları)
* Lisans hakları akıllı kontratlar ile güvence altına alınır.
* İnternet kopmalarında lisans kontrolü local cache (Redis) üzerinden 72 saate kadar tolere edilir.

---

## 12. Governance (Gelecek Yönetişim Planı)
* Gelecekte, platformun parametreleri (örn: komisyon oranları, eklenti onay kuralları) token sahiplerinin oylamalarıyla (DAO/Decentralized Governance) güncellenecektir.

---

## 13. Compliance & Risk (Uyum ve Risk Yönetimi)
* Tüm ekonomik transferler ve cüzdan işlemleri yerel mali mevzuatlara, AML (Kara Para Aklamayı Önleme) standartlarına ve KVKK kurallarına tam uyumlu olmak zorundadır.

---

## 14. Multi-chain Strategy (Çoklu Zincir Stratejisi)
* EAOS lisansları ve DAO oylamaları Arbitrum/EVM ağında tutulurken; gerçek zamanlı asistan mikro-ödemeleri düşük işlem ücreti ve yüksek hız nedeniyle Solana ağında yürütülecektir.

---

## 15. Roadmap (Yol Haritası)
* **Sürüm 1 (2026):** Local Credit Ledger (Fiat ve kredi kartıyla bakiye yükleme).
* **Sürüm 2 (2027):** EVM & Solana Cüzdan Entegrasyonu ve Token Utility Lansmanı.
* **Sürüm 3 (2028):** Decentralized Marketplace ve Escrow Akıllı Kontrat Geçişi.
