# 🔁 Distributed Idempotency Roadmap

**Title:** Distributed Idempotency Roadmap  
**Version:** 1.0.0  
**Status:** Approved / Freeze  
**Owner:** Architecture Board  
**Last Updated:** 2026-07-10  
**Dependencies:** EVENT_BUS.md, DOMAIN_MODEL.md  

---

Webhook üzerinden gelen mükerrer mesaj isteklerini ve ağ tekrarlarını önlemek amacıyla Omnichannel Messaging Core (OMC) katmanında uygulanacak olan Idempotency (tekilleştirme) yol haritası üç faza bölünmüştür.

---

## Faz Analizi ve Karşılaştırma Matrisi

### 1. Faz: In-Memory Idempotency (Mevcut - MVP)
* **Teknoloji:** `IMemoryCache` (Uygulama yerel bellek alanı).
* **Anahtar Ömrü (TTL):** 24 Saat.
* **Çalışma Şekli:** Gelen webhook `ExternalMessageId` değeri yerel önbellekte sorgulanır, yoksa kaydedilir.
* **Avantajları:**
  * Sıfır ek altyapı bağımlılığı (Redis veya DB kurulumu gerektirmez).
  * Son derece hızlı okuma/yazma (bellek içi erişim süresi < 1 mikrosaniye).
  * Kolay test ve hızlı devreye alma.
* **Dezavantajları:**
  * Sunucu yeniden başladığında (restart) veya yeni versiyon deploy edildiğinde tüm önbellek silinir.
  * **Yatay Ölçekleme Sorunu:** Çoklu instance (Load Balancer) yapısında, aynı webhook isteğinin tekrarları farklı sunuculara yönlendirilirse tekilleştirme çalışmaz.

### 2. Faz: Distributed Redis Cache (Üretim Ortamı - Target)
* **Teknoloji:** `IDistributedCache` + Redis Sentinel/Cluster.
* **Anahtar Ömrü (TTL):** 7 Gün (1 Hafta).
* **Çalışma Şekli:** Sunucular ortak bir Redis önbelleğine bağlanır. `omc:idempotency:{channel}:{externalMessageId}` anahtarı kontrol edilir.
* **Avantajları:**
  * Sunucu restartlarından veya deploy süreçlerinden etkilenmez.
  * Tüm sunucu instance'ları ortak önbellek kullandığı için yatay ölçeklemede mükerrer işlemeyi %100 engeller.
  * Dağıtık Kilit (Distributed Lock - `RedLock` veya Redis `SETNX`) desteğiyle yarış durumlarını (Race Conditions) önler.
* **Dezavantajları:**
  * Redis altyapı maliyeti ve sunucu yönetimi gereksinimi.
  * Ağ gecikmesi (Network I/O - ~1ms).

### 3. Faz: Veri Tabanı Kayıt ve Outbox Entegrasyonu (Gelecek - Hardened)
* **Teknoloji:** Relational Database Unique Constraint (`MessageIdempotencyLog` tablosu) + Inbox/Outbox Pattern.
* **Anahtar Ömrü (TTL):** Süresiz (veya Partitioned/Archived).
* **Çalışma Şekli:** Gelen mesajın benzersiz kimliği, ana veri tabanı transaction'ı içerisinde tekilleştirme tablosuna yazılır. Çift yazma durumunda DB seviyesinde `Unique Key Violation` fırlatılarak transaction rollback edilir.
* **Avantajları:**
  * **İşlem Garantisi (Transaction Safety):** Mesajın yazılması ve tekilleştirme kaydının atılması ACID prensipleriyle korunur. Önbellek çökse dahi mükerrer işlem olasılığı sıfırdır.
* **Dezavantajları:**
  * Yüksek trafik altında veri tabanında I/O dar boğazı (Connection pool starvation) ve kilitlenmeler oluşturabilir.

---

## Hibrit Çözüm Mimarisi (Production Target)

En güvenli ve performanslı yapı, **2. Faz (Redis)** ve **3. Faz (Veri Tabanı Kısıtı)** yapılarının bir arada kullanıldığı **Hibrit Model**dir:

```text
Webhook İsteyi
     ↓
Redis Kontrolü (Hızlı ve Performanslı Filtre)
     ├─ Var ise → Yanıt Ver (Bypass DB)
     └─ Yok ise → DB Transaction Başlat
                     ↓
                  Database INSERT (Unique Key Constraint)
                     ├─ Başarılı → Commit & Dispatch
                     └─ Hata (Mükerrer) → Rollback
```

---

## Implementasyon Planı

1. **Sprint 3 (Mevcut):** `InMemoryIdempotencyChecker` MVP olarak devrededir ve test geçişlerinde kullanılır.
2. **Sprint 4 (Redis Entegrasyonu):** `Program.cs` altındaki `IMessageIdempotencyChecker` kaydı `RedisIdempotencyChecker` ile değiştirilir. Redis bağlantı kütüphanesi (`Microsoft.Extensions.Caching.StackExchangeRedis`) projeye eklenir.
3. **Sprint 5 (DB Inbox/Outbox Hardening):** `ConversationMessage` veri tabanı şemasına `ExternalMessageId` ve `Channel` alanları için `HasUniqueIndex` kuralı eklenerek en dip katmanda veri bütünlüğü koruma altına alınır.
