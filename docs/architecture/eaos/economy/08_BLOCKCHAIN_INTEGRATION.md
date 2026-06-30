# 🔗 08_BLOCKCHAIN_INTEGRATION.md (Çoklu Blokzincir Entegrasyonu)

EAOS platformunun farklı blokzincir ağlarıyla (EVM, Solana vb.) nasıl konuşacağını ve cüzdan adaptör mimarisini belirler.

---

## 1. Çoklu Blockchain Desteği (Multi-Chain Abstraction)
* Sistem tek bir blokzincire bağımlı değildir. Ortak bir `BlockchainAdapter` arayüzü ile çalışır.
* Desteklenen ilk ağlar: **Ethereum/Arbitrum (EVM)** (Akıllı kontratlar ve lisanslar için) ve **Solana** (Yüksek hızlı, düşük ücretli mikro ödemeler ve token transferleri için).

---

## 2. İşlem Onay ve Konsensüs Entegrasyonu
* Ajanların zincir üzerinde işlem yapabilmesi için işlemin öncelikle `Permission Guard` ve `Safe Adapter` tarafından doğrulanarak imzalanması gerekir. Yetkisiz veya maskelenmemiş hiçbir ham veri zincire yazılamaz.
