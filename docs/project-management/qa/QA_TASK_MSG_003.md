# QA Review

**Task:** TASK_MSG_003_INDEPENDENT_QA  
**Date:** 2026-07-10  
**Reviewer:** A2 Sentinel  
**Scope:** Message Normalizer & Channel Adapters Layer  
**Kısıt:** Kod değiştirilmedi, commit yapılmadı.

---

## Build

* **Status:** PASS (0 errors, 5 warnings)
* **Log Output:** `dotnet build EmareTicket.sln -c Release`
  * Warning CA1510 in `WhatsAppAdapter.cs`, `WebWidgetAdapter.cs`, and `MessengerAdapter.cs` (Use `ArgumentNullException.ThrowIfNull`).
  * Warning CS8600 in `MessagingGateway.cs` (Nullability assignment).

---

## Tests

* **Status:** PASS (37 messaging tests, 718 total tests passed successfully)
* **Log Output:** `dotnet test EmareTicket.sln -c Release`

---

## Clean Architecture

* **Domain Bağımsızlığı:** EVET. Tüm normalizer ve adapter sınıfları `EmareTicket.Infrastructure` katmanında ve arayüz tanımları `EmareTicket.Application` katmanında tutularak bağımlılıklar ayrılmıştır.
* **Provider-Specific Sızıntı Kontrolü:** EVET. Meta Messenger, WhatsApp ve WebWidget'a özel ham veri yapıları tamamen kendi adapter sınıfları (`MessengerAdapter.cs`, `WhatsAppAdapter.cs`, `WebWidgetAdapter.cs`) içerisinde kapsüllenmiştir. Çekirdek ağ geçidine (`MessagingGateway`) ve veritabanı katmanına herhangi bir provider modeli sızmamaktadır.
* **Metadata Yönetimi:** EVET. Kanallara özel ek alanlar (örn. WhatsApp durum bilgileri, Meta reaction tipleri vb.) standarda sızmadan `InboundMessageEnvelope` üzerindeki `Metadata.Values` sözlüğü içerisinde taşınmaktadır.

---

## DDD Compliance

* **Sınırlar ve Rol Ayrımı:** EVET. Adapter'lar ham payloaddan envelope üretirken herhangi bir aggregate kurallarına veya veritabanı durumlarına müdahale etmez. Sadece girdi dönüşümü yaparlar.

---

## Security

* **datetime.now Kullanımı:** EVET (Engellendi). Tüm zaman damgalarında `UtcNow` kullanılmıştır.
* **Secret & PII Loglama:** EVET. Logger çıktılarında webhook'lardan gelen kimlik doğrulama token'ları, gizli anahtarlar veya kişisel veriler ham biçimde kaydedilmemekte, sadece `CorrelationId` ve `MessageId` takibi yapılmaktadır.
* **Tenant Spoofing (Kiracı Taklidi) Riski:** KISMEN GEÇERLİ. *(Detaylar Kritik Bulgular bölümünde açıklanmıştır).*

---

## Performance

* **Gereksiz JSON Parse Tekrarı:** EVET (Engellendi). `ValidateWebhookAsync` ve `NormalizeInboundAsync` kendi içlerinde parse işlemlerini optimize etmiştir.
* **Büyük Payload ve Bellek Yönetimi:** `JsonDocument` kullanımı .NET Core üzerinde bellek performansını yüksek tutmaktadır.

---

## Persistence & Gateway Integration

* **Persistence Sıralaması:** EVET. Mesaj persistence katmanına yazıldıktan sonra dispatch edilmektedir.
* **Status Updates Yönlendirmesi:** EVET. WhatsApp veya Meta üzerinden gelen durum güncellemeleri (`status_update`) yeni bir mesaj gibi kaydedilmemekte, doğrudan `UpdateDeliveryReadStatusAsync` metoduna yönlendirilerek mevcut mesajın durumu güncellenmektedir.
* **Transaction Sınırı:** EVET. Önceki aşamada kurulan veritabanı transaction yönetimi (`BeginTransactionAsync` ve rollback/commit mantığı) başarıyla korunmaktadır.

---

## Test Coverage

* **Yeterlilik:** EVET. `MessageNormalizerTests.cs` altındaki testler Meta Messenger metin/ek/reaksiyon, WhatsApp metin/görüntü/döküman/durum ve WebWidget metin/reconnect akışlarını hem pozitif hem negatif senaryolarla başarıyla doğrulamaktadır.

---

## Critical Issues

### ⚠️ 1. Messenger Attachment URL Çözümlemesinde UriFormatException Çökme Riski (Medium)
* **Konum:** [MessengerAdapter.cs:L124](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Adapters/MessengerAdapter.cs#L124)
* **Bulgu:** Meta Messenger üzerinden gelen eklerin dosya adı ayıklanırken doğrudan `new Uri(url)` çağrısı yapılmaktadır:
  ```csharp
  Filename = System.IO.Path.GetFileName(new Uri(url).AbsolutePath) ?? "file"
  ```
* **Risk:** Eğer payload içindeki URL alanı göreceli (relative) gelirse veya herhangi bir malformed format barındırıyorsa, `new Uri(url)` ifadesi `UriFormatException` fırlatarak tüm webhook işleme akışının yarıda kesilmesine sebep olacaktır.
* **Öneri:** URL doğrulaması için `Uri.TryCreate` kullanılmalıdır:
  ```csharp
  Filename = Uri.TryCreate(url, UriKind.Absolute, out var parsedUri) 
      ? (System.IO.Path.GetFileName(parsedUri.AbsolutePath) ?? "file") 
      : "file";
  ```

### ⚠️ 2. Çoklu Webhook Mesajlarında (Batching) Veri Kaybı Riski (Low/Medium)
* **Konum:** [WhatsAppAdapter.cs:L65-106](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Adapters/WhatsAppAdapter.cs#L65) ve [MessengerAdapter.cs:L76-87](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Adapters/MessengerAdapter.cs#L76)
* **Bulgu:** Meta Messenger ve WhatsApp webhook'ları yüksek yoğunluklu anlarda tek bir HTTP isteğinde birden fazla mesaj veya durum bildirimini liste (`entry` veya `changes` dizileri) halinde gönderebilir. Mevcut adapter implementasyonları sadece ilk elemanı (`[0]`) okumaktadır:
  ```csharp
  var firstEntry = entries[0];
  var msg = messages[0];
  ```
* **Risk:** Meta'nın aynı webhook çağrısında paketlediği ikinci ve sonraki mesajlar tamamen göz ardı edilecek ve veri kaybı yaşanacaktır.
* **Öneri:** Gelecek fazlarda adapter'ların `List<InboundMessageEnvelope>` dönecek şekilde döngü (loop) yapısına geçirilmesi gerekmektedir.

### ⚠️ 3. Web Widget Tenant Spoofing Güvenlik Riski (Low/Medium)
* **Konum:** [WebWidgetAdapter.cs:L97-100](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Adapters/WebWidgetAdapter.cs#L97) ve [MessagingGateway.cs:L84](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/MessagingGateway.cs#L84)
* **Bulgu:** Web Widget istemci taraflı bir yapı olduğu için payload içerisinde `tenantId` bilgisini kendisi yollamaktadır. `MessagingGateway` ise eğer payloaddan bir `TenantId` gelmişse `ResolveTenantIdAsync` adımını atlamaktadır.
* **Risk:** Kötü niyetli bir istemci, API endpoint'ine başka bir tenant'a ait UUID gönderirse, mesaj o tenant'ın konuşma geçmişine yazılabilir.
* **Öneri:** Web Widget bağlantısı kurulurken tenantId bilgisinin JWT token veya sunucu taraflı güvenli bir session/slug doğrulaması ile kontrol edilmesi sağlanmalıdır.

---

## Final Verdict

* **STATUS:** **PASS** (Kritik bug bulunmamaktadır. Listelenen bulgular mimari kısıtlardan kaynaklı iyileştirme önerileridir ve sonraki fazlarda ele alınabilir).
