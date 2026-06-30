# 📜 07_LICENSE_SYSTEM.md (Lisans ve Akıllı Kontrat Standartları)

Modüllerin ve eklentilerin lisans doğrulama süreçlerini ve çevrimdışı çalışma kurallarını tanımlar.

---

## 1. Akıllı Kontrat Tabanlı Lisanslama
* Pazar yerinden alınan her modülün lisans hakkı, kiracının cüzdan adresiyle ilişkilendirilmiş bir akıllı kontrat (Smart Contract License) olarak zincir (blockchain) üzerine yazılır.

---

## 2. Çevrimdışı (Offline) Çalışma Toleransı
* İnternet veya blokzincir erişimi geçici olarak koptuğunda, lisans kontrolü local cache (Redis) üzerinden en fazla **72 saat** süreyle tolere edilir. Bu sürenin sonunda bağlantı sağlanamazsa, modül kendini güvenli kısıtlı moda alır.
