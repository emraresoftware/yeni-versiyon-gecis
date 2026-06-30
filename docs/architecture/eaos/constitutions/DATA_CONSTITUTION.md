# 🗄️ DATA_CONSTITUTION.md (EAOS Veri ve Kalıcılık Anayasası)

Bu anayasa, EAOS platformundaki verilerin saklanması, izole edilmesi, şifrelenmesi, yedeklenmesi ve silinmesi süreçlerindeki yasal ve teknik standartları belirler. [CONSTITUTION.md](../CONSTITUTION.md) Madde II'ye doğrudan bağlıdır.

---

## 1. Tenant Isolation (Kiracı İzolasyonu)
* **Mantıksal Ayrım:** Veritabanındaki tüm tablolarda `TenantId` kolonu bulunmak zorundadır. EF Core üzerinde `HasQueryFilter(x => x.TenantId == _tenantProvider.TenantId)` filtresi global olarak uygulanmalıdır.
* **Fiziksel Ayrım:** Büyük ölçekli veya yüksek güvenlik gereksinimi olan kiracılar için "database-per-tenant" (her kiracıya ayrı DB) modeli desteklenmeli, bağlantı dizgisi (connection string) çalışma zamanında dinamik çözümlenmelidir.

---

## 2. Şifreleme (Encryption)
* **Rest (Saklanan Veri):** Hassas veriler (SMTP şifreleri, API Key'ler, entegrasyon şifreleri) veritabanına kaydedilmeden önce **AES-256-GCM** algoritması ve sunucuya özel `ENCRYPTION_KEY` kullanılarak şifrelenmelidir.
* **Transit (Taşınan Veri):** Tüm veri transferleri zorunlu olarak TLS 1.3/HTTPS ve güvenli WebSocket (WSS) protokolleri üzerinden yapılmalıdır.

---

## 3. Yedekleme (Backup)
* **Veritabanı Yedekleri:** PostgreSQL yedekleri otomatik olarak günlük, haftalık ve aylık periyotlarda alınmalı, izole edilmiş ve şifrelenmiş yedek sunucularında (Standby/S3) saklanmalıdır.
* **Yedeklerin Geri Yüklenmesi:** Yılda en az 2 kez "Olağanüstü Durum Kurtarma" (Disaster Recovery) testleri yapılarak yedeklerin geri yüklenebilirliği doğrulanmalıdır.

---

## 4. Audit Log (Değişiklik İzleme)
* **Entity Değişiklikleri:** Veritabanındaki her yazma, güncelleme ve silme işlemi `AuditLog` tablosuna eski/yeni değer JSON'ı, işlemi yapan kullanıcı ID'si ve IP adresi ile kaydedilmelidir. Bu loglar silinemez ve değiştirilemez.
* **Yapay Zeka İzleri:** AI ile yapılan her prompt/response ve token kullanımı `AIAuditLogs` tablosunda saklanmalıdır.

---

## 5. KVKK ve GDPR Uyum standartları
* **Unutulma Hakkı:** Kullanıcı veya müşteri "hesabımın/verilerimin silinmesini istiyorum" dediğinde, sistem soft-delete mekanizmasının yanında, veritabanından ve loglardan verileri tamamen kazıyan (hard-delete/anonymize) süreçleri çalıştırmalıdır.
* **Açık Rıza:** Ses kayıtlarının alınması veya verilerin işlenmesi öncesinde IVR/Sesli onay veya SMS ile açık rıza (Consent) doğrulaması alınmalıdır.

---

## 6. Retention Policy (Veri Saklama Süresi)
* Çağrı ses kayıtları (WAV dosyaları) aksi kiracı tarafından belirtilmedikçe en fazla 90 gün saklanır, bu sürenin sonunda otomatik olarak kalıcı olarak silinir.
* Sistem hata logları en fazla 30 gün, audit loglar ise yasal zorunluluklar gereği en az 2 yıl saklanmalıdır.

---

## 7. Veritabanı Teknolojileri Rolleri
* **PostgreSQL:** Ana işlemsel (transactional) veri tabanıdır. CQRS komut ve sorguları buradan beslenir.
* **Redis:** Oturum hafızası, rate limiting sayaçları, ElevenLabs ses önbelleği ve PubSub event bus için bellek içi (in-memory) veri deposudur.
* **Vector DB (Qdrant):** Yapay zeka ajanlarının anlamsal hafızası ve bilgi tabanı aramaları için kullanılır.
