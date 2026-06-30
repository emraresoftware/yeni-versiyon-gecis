# 📐 EAOS Architecture Standards (Teknik ve Tasarım Standartları)

Bu doküman, EAOS bünyesindeki tüm servislerin uyması gereken teknik kuralları, veri modellerini, haberleşme protokollerini ve kod standartlarını belirler.

---

## 1. Mimari Tasarım Kalıpları
* **Modular Monolith & Microservices:** Çekirdek CRM/ERP işleri modüler monolit (.NET 8) yapısında kalırken, AI servisleri ve ses köprüleri bağımsız mikroservisler (Python, Go veya Node.js) olarak Docker üzerinde izole çalışır.
* **CQRS (Command Query Responsibility Segregation):** İş katmanında komutlar (yazma) ve sorgular (okuma) kesin olarak ayrılır. Veri tutarlılığı ve performans için MediatR handler'ları kullanılır.
* **Result Pattern:** Metotlar doğrudan hata fırlatmak (throw exception) yerine `Result<T>` veya `ApiResponse` sarmalayıcıları dönerek hata durumlarını güvenli şekilde yönetir.

---

## 2. Haberleşme ve API Standartları
* **Gerçek Zamanlı (Realtime) Akışlar:** Sesli aramalar için AudioSocket (raw PCM), tarayıcı veya mobil asistan bağlantıları için WebSocket tercih edilir.
* **Servisler Arası İletişim (Internal):** Mikroservisler ve orkestratörler arasında yüksek performanslı ve düşük gecikmeli **gRPC** kullanılır.
* **Dış Entegrasyonlar (External):** API Marketplace üzerindeki tüm entegrasyonlar REST / JSON standartlarında olmalıdır.
* **Asenkron Bildirimler:** Loglama, bildirim ve istatistik verileri kuyruk yapıları (RabbitMQ / Redis PubSub) üzerinden asenkron iletilir.

---

## 3. Veritabanı ve Kalıcılık Standartları
* **PostgreSQL + EF Core:** Ana ilişkisel veri tabanı PostgreSQL'dir.
* **Zaman Dilimi (DateTime) Kuralı:** PostgreSQL `timestamptz` kullanır. Kod seviyesindeki tüm tarih atamaları **`DateTimeKind.Utc`** olmak zorundadır. `DateTime.UtcNow` kullanılmalı, `DateTime.Now` kesinlikle yasaktır.
* **Vektör Veri Tabanı:** Anlamsal hafıza ve RAG süreçleri için Qdrant/Milvus gibi vektör veritabanları kullanılır.

---

## 4. Güvenlik ve Uyumluluk Standartları
* **PII Masking (KVKK/GDPR):** E-posta, T.C. Kimlik No, telefon numarası ve kart bilgileri harici LLM sağlayıcılarına gönderilmeden önce regex tabanlı maskeleme filtresinden (`Safe Adapter`) geçirilmelidir.
* **Tenant Isolation:** Tüm SQL sorgularında tenant filtrelemesi (`TenantId`) EF Core global query filters ile otomatik uygulanmalıdır.
