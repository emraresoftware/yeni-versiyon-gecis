# 🔒 SECURITY_CONSTITUTION.md (EAOS Güvenlik Anayasası)

Bu anayasa, EAOS platformunun tamamında geçerli olan siber güvenlik kurallarını, kimlik doğrulama standartlarını ve acil durum müdahale planlarını içerir. [CONSTITUTION.md](../CONSTITUTION.md) Madde I.2 ve Madde IV.3'e doğrudan bağlıdır.

---

## 1. RBAC (Rol Tabanlı Erişim Kontrolü)
* **En Az Yetki İlkesi (Least Privilege):** Hiçbir kullanıcı veya ajan, görevinin gerektirdiğinden daha fazla yetkiye sahip olamaz.
* **Rol Hiyerarşisi:** SuperAdmin, TenantAdmin, Operator ve Agent rolleri ve bunlara bağlı izin matrisleri (`Permissions`) veritabanında saklanır ve her API isteğinde doğrulanır.

---

## 2. OAuth ve JWT Standartları
* **Token Güvenliği:** Kimlik doğrulamada JWT (JSON Web Tokens) kullanılır.
  * Access Token ömrü: En fazla 15 dakika.
  * Refresh Token ömrü: En fazla 7 gün (sadece HTTP-Only Cookie içinde saklanabilir).
* **Şifreleme:** JWT imzalamada güvenli algoritmalar (örn: HS256 veya RS256) ve minimum 32 karakterli `JWT_SECRET_KEY` kullanılmalıdır.

---

## 3. API Keys ve Secrets Management (Sırların Yönetimi)
* **Sırların Korunması:** API anahtarları, DB şifreleri ve özel anahtarlar kesinlikle kod tabanına veya git depolarına commit edilemez. Hepsi `.env` dosyalarında ve sunucu ortam değişkenlerinde saklanmalıdır.
* **Ajan API Anahtarları:** Kiracıların entegrasyon anahtarları DB'de şifreli saklanır ve sadece runtime'da çözülerek kullanılır.

---

## 4. Zero Trust (Sıfır Güven Yaklaşımı)
* Sistem içindeki hiçbir servis birbirine "varsayılan olarak güvenli" kabul edilmez.
* Mikroservisler arası gRPC çağrılarında veya ses köprüsünün API isteklerinde mutlaka `EMARE_SERVICE_KEY` başlığı (header) üzerinden karşılıklı token doğrulaması (mTLS veya Bearer) yapılmalıdır.

---

## 5. MFA (Çok Faktörlü Kimlik Doğrulama)
* Yönetici (SuperAdmin/TenantAdmin) girişlerinde ve kritik işlemler öncesinde SMS OTP veya Authenticator App (TOTP) tabanlı Çok Faktörlü Kimlik Doğrulama zorunludur.

---

## 6. Rotation (Anahtar ve Şifre Yenileme)
* Sistem şifreleme anahtarları, JWT secret key'leri ve veritabanı şifreleri yılda en az 1 kez otomatik veya manuel olarak yenilenmelidir (rotation).

---

## 7. Olay Müdahale Planı (Incident Response)
* Güvenlik ihlali veya yetkisiz erişim algılandığı an:
  * **İzolasyon:** Etkilenen tenant veya sunucu anında karantinaya alınır.
  * **Geçici Kilit:** İlgili API anahtarları ve JWT oturumları tek tuşla iptal edilir (revocation list).
  * **Log İnceleme:** Audit loglar üzerinden saldırı kaynağı tespit edilip kapatılır.
