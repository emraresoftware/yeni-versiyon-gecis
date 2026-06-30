# 💳 03_WALLET_SYSTEM.md (Cüzdan ve Bakiye Yönetim Mimarisi)

Tüm kiracı ve kullanıcı cüzdanlarının şifrelenmesi, transferleri ve güvenliği ile ilgili standartları içerir.

---

## 1. Cüzdan Güvenliği
* **Non-Custodial Option:** İsteyen kiracılar kendi özel anahtarlarını (private keys) yerel donanımlarında saklayarak cüzdanlarını kendileri yönetebilir.
* **Şifreli Saklama (DB Mode):** EAOS üzerinde barındırılan cüzdan anahtarları **AES-256-GCM** ve HSM (Hardware Security Module) entegrasyonu ile şifrelenir.

---

## 2. API Entegrasyonları
* Cüzdan bakiyesi sorgulama, transfer onaylama ve imzalama (signing) işlemleri `SECURITY_CONSTITUTION.md` standartlarına uygun olarak mTLS ve JWT doğrulamasıyla yapılır.
