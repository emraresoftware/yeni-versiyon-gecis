# 📐 ARCHITECTURE_REVIEW_STANDARD.md (Mimari İnceleme Kontrol Listesi)

Bu kontrol listesi, EAOS platformunda yapılacak kod incelemelerinde (Code Review) mimarlar ve Platform Guardian tarafından adım adım doldurulması zorunlu olan kontrol maddelerini içerir. [ARCHITECTURE_STANDARDS.md](../ARCHITECTURE_STANDARDS.md) belgesine doğrudan bağlıdır.

---

## 📋 Mimarî Kontrol Listesi

### 1. Servis Bağımsızlığı & Hard Dependency Kontrolü
* [ ] Modül veya servis kendi başına deploy edilebilir yapıda mı?
* [ ] Diğer servislerin çökmesi (örn: ERP veya CRM API'si) durumunda bu servis çalışmayı sürdürebiliyor mu?
* [ ] Harici API çağrılarında platformu kilitlemeyecek asenkron (`async/await`) yapılar kullanılmış mı?

### 2. Kiracı Güvenliği & Veri İzolasyonu (Tenant Security)
* [ ] Tüm veritabanı sorgularında ve Entity Framework Core konfigürasyonlarında `TenantId` filtrelemesi yapılmış mı?
* [ ] Kullanıcının ait olmadığı bir kiracının verilerine erişmesini engelleyecek yetki denetimi yapılmış mı?

### 3. Sağlayıcı Soyutlaması (Provider Abstraction)
* [ ] Yapay zeka dil modelleri ve ses motorları doğrudan çağrılmak yerine `VoiceProvider` ve `DynamicLLMProvider` adaptörleri üzerinden soyutlanmış mı?
* [ ] Yeni bir LLM sağlayıcısı eklendiğinde ses çekirdeği koduna dokunulması gerekiyor mu? (Gerekmemeli).

### 4. Hata ve Dayanıklılık Yönetimi (Resilience)
* [ ] Tüm harici ağ isteklerinde (HTTP, gRPC, WebSocket) maksimum 2000ms **Timeout** sınırı uygulanmış mı?
* [ ] Geçici ağ hataları için **Polly Retry** (Katlanarak artan bekleme süresi) yapısı kurulmuş mu?
* [ ] Hata durumlarında diğer servisleri korumak için **Circuit Breaker** (Devre Kesici) entegre edilmiş mi?

### 5. Esneklik ve Geri Dönüş Güvencesi (Feature Flag & Rollback)
* [ ] Yeni eklenen tüm özellikler ve entegrasyonlar bir **Feature Flag** (Ortam değişkeni) arkasına alınmış mı?
* [ ] Olası bir hata anında özellik kapatıldığında sistemin stabil haline geri döneceği test edilmiş mi?

### 6. Observability & Loglama Standartları
* [ ] Tüm loglar `Structured JSON` formatında ve `CorrelationId` alanıyla birlikte yazılıyor mu?
* [ ] Kritik metrikler ve SLA durumları Prometheus/Grafana için dışarıya sunulmuş mu?
* [ ] İstek zinciri boyunca `OpenTelemetry` trace takipleri yapılmış mı?
