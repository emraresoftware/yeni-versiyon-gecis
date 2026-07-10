# QA Review

**Task:** TASK_MSG_002_INDEPENDENT_QA  
**Date:** 2026-07-10  
**Reviewer:** A2 Sentinel  
**Scope:** Omnichannel Messaging Core (OMC) Persistence and Gateway Layers  
**Kısıt:** Kod değiştirilmedi, commit yapılmadı.

---

## Build

* **Status:** PASS (0 errors, 2 warnings)
* **Log Output:** `dotnet build EmareTicket.sln -c Release`
  * Warning CS8600 in `MessagingGateway.cs(123,32)`: Converting null literal or possible null value to non-nullable type.
  * Warning CS8600 in `ProductsController.cs(240,22)`: Converting null literal or possible null value to non-nullable type.

---

## Tests

* **Status:** PASS (18 messaging tests, 699 total tests passed successfully)
* **Log Output:** `dotnet test EmareTicket.sln -c Release --filter "FullyQualifiedName~Messaging"`

---

## Clean Architecture

* **Domain Bağımsızlığı:** EVET. `MessagingEntities.cs` herhangi bir dış kütüphane bağımlılığı olmaksızın `EmareTicket.Domain` katmanında tanımlanmıştır.
* **Infrastructure Sızıntısı:** EVET (Engellendi). Veri tabanı repository sözleşmesi `IConversationStore` arayüzü `EmareTicket.Application` katmanındayken, somut implementasyon `ConversationStore` persistence katmanındadır.
* **Controller DbContext Kullanımı:** EVET (Engellendi). Controller katmanlarında doğrudan DbContext kullanımına rastlanmamıştır.

---

## DDD Compliance

* **AggregateRoot / Entity Sınırları:** EVET. `Conversation` sınıfı, ilişkili kanallar (`ConversationChannel`), katılımcılar (`ConversationParticipant`), mesajlar (`ConversationMessage`) ve ekler (`ConversationAttachment`) için Aggregate Root (Küme Kökü) rolünü doğru bir şekilde üstlenmektedir.
* **Domain Event Kullanımı:** HAYIR. OMC veri modellerinde henüz domain event tetikleyici mekanizmalar kurulmamıştır.
* **Repository Sınırı:** EVET. `IConversationStore` doğrudan Aggregate Root üzerinden veri yönetimini kontrol etmektedir.

---

## Security

* **DateTime.Now Kullanımı:** EVET (Engellendi). Tüm zaman damgalarında `DateTime.UtcNow` kullanılmış, sunucu yerel saatine bağımlılık yaratılmamıştır.
* **Ham Exception Fırlatma (throw new Exception):** EVET (Engellendi). Hatalar `Result` deseni üzerinden güvenli bir şekilde döndürülmektedir.
* **Hardcoded Secret / Conn String / Tenant:** EVET (Engellendi). Dosyalarda herhangi bir hardcoded gizli anahtar veya bağlantı metni saptanmamıştır.

---

## Performance

* **N+1 Sorgu Riski:** EVET (Engellendi). `FindActiveConversationAsync` metodunda kanallar ve katılımcılar `.Include()` ile; `GetTimelineAsync` metodunda ise ekler eager loading ile getirilerek N+1 performans zafiyetleri önlenmiştir.
* **Async ve CancellationToken Kullanımı:** EVET. Tüm veri tabanı sorguları asenkron metodlar üzerinden yürütülmekte ve `CancellationToken` parametresi EF Core sorgularına iletilmektedir.

---

## Persistence

* **Soft Delete:** EVET. Tüm OMC tabloları `SoftDeletableEntity` miras almakta ve sorgularda `!IsDeleted` kontrolü başarıyla uygulanmaktadır.
* **Tenant Isolation:** KISMEN GEÇERLİ. `AppDbContext.OnModelCreating` üzerinde `ITenantEntity` arayüzüne sahip tüm tablolar için otomatik global tenant filtrelemesi kurulmuştur. Webhook girişlerinde `SetCurrentTenant` çağrısı yapılmaktadır. *(Kritik istisnalar aşağıda listelenmiştir).*
* **Concurrency (Eşzamanlılık):** `Conversation` tablosunda `UnreadCount` veya `LastMessageAt` güncellemelerinde paralel gelen webhook istekleri sırasında yarış durumlarını (race condition) engelleyecek bir iyimser eşzamanlılık (optimistic concurrency) token'ı tanımlanmamıştır.

---

## API & Gateway

* **Persist Sıralaması:** EVET. `MessagingGateway.cs` içinde mesaj verileri önce veri tabanına yazılmakta, ardından normalleştirme ve dağıtım (`INormalizedMessageDispatcher`) aşamasına iletilmektedir. Bu sayede olası dispatch hatalarında mesaj kaybı önlenmiştir.

---

## Test Coverage

* **Birim Test Kapsamı:** EVET (Yeterli). `ConversationStoreTests.cs` ve `MessagingGatewayTests.cs` dosyaları; tekil kısıtları, çoklu kanal bağlamayı, silinen kayıtların görünmezliğini ve mesaj ekleme süreçlerini başarıyla doğrulamaktadır.

---

## Critical Issues

### 🚨 1. Out-of-Order Webhook ile Mesaj Okunma Durumunun Bozulması (High)
* **Konum:** [ConversationStore.cs:L217](file:///Users/emre/Elyafgroup/src/EmareTicket.Persistence/Repositories/ConversationStore.cs#L217)
* **Bulgu:** `UpdateDeliveryReadStatusAsync` metodunda durum güncellenirken herhangi bir durum makinesi (state machine) veya zaman damgası sırası kontrol edilmemektedir. Mesaj durumu körlemesine güncellenmektedir: `message.Status = status;`
* **Risk:** Bulut sağlayıcılarından (örn. WhatsApp) gelen webhook durum bildirimleri asenkron ağ yapısı sebebiyle sırasız gelebilir. Zaten `Read` (Okundu) olmuş bir mesaj için sonradan gecikmeli gelen bir `Delivered` (İletildi) webhooğu, mesaj durumunu geriye çekerek veriyi bozacaktır.
* **Öneri:** Mesaj durumunun geriye doğru değişmesini engelleyecek bir kontrol eklenmelidir:
  ```csharp
  if (message.Status == MessageStatus.Read && (status == MessageStatus.Delivered || status == MessageStatus.Sent))
  {
      continue; // Sırasız gelen eski webhook bilgisini atla
  }
  ```

### 🚨 2. Soft-Deleted Mesajlarda Benzersiz Kısıt Çakışması ve DB Çökme Riski (High)
* **Konum:** [MessagingConfigurations.cs:L120](file:///Users/emre/Elyafgroup/src/EmareTicket.Persistence/Configurations/MessagingConfigurations.cs#L120) ve [ConversationStore.cs:L116](file:///Users/emre/Elyafgroup/src/EmareTicket.Persistence/Repositories/ConversationStore.cs#L116)
* **Bulgu:** `ConversationMessages` tablosundaki benzersiz indeks `(ExternalMessageId, Channel, TenantId)` olarak tanımlanmıştır ve filtre sadece `\"ExternalMessageId\" IS NOT NULL` şeklindedir. `AppendMessageAsync` metodunda ise mükerrer kontrolü `!m.IsDeleted` filtresiyle yapılmaktadır:
  ```csharp
  var exists = await _context.ConversationMessages.AnyAsync(m => ... && !m.IsDeleted, cancellationToken);
  ```
* **Risk:** Eğer bir mesaj yumuşak silinmişse (`IsDeleted = true`), `AppendMessageAsync` kontrolü bunu "mevcut değil" olarak görecek ve yeni ekleme işlemini başlatacaktır. Ancak veri tabanındaki benzersiz indeks yumuşak silinen kayıtları filtrelemediği için insert işlemi **Unique Constraint Violation Exception (DbUpdateException)** ile uygulamanın çökmesine yol açacaktır.
* **Öneri:** Benzersiz indeks filtresine `IsDeleted = false` koşulu eklenmelidir:
  ```csharp
  builder.HasIndex(x => new { x.ExternalMessageId, x.Channel, x.TenantId })
      .IsUnique()
      .HasFilter("\"ExternalMessageId\" IS NOT NULL AND \"IsDeleted\" = false");
  ```

### 🚨 3. Durum Güncellemelerinde Eksik Tenant Filtresi (Medium)
* **Konum:** [ConversationStore.cs:L207](file:///Users/emre/Elyafgroup/src/EmareTicket.Persistence/Repositories/ConversationStore.cs#L207)
* **Bulgu:** `UpdateDeliveryReadStatusAsync` metodu mesajı veri tabanından çekerken sadece `ExternalMessageId` filtresi uygulamaktadır:
  ```csharp
  var messages = await _context.ConversationMessages
      .Where(m => m.ExternalMessageId == externalMessageId && !m.IsDeleted)
      .ToListAsync(cancellationToken);
  ```
* **Risk:** Eğer bu metod anonim bir webhook veya arka plan işi gibi TenantId'nin set edilmediği (`IsFilterDisabled = true`) bir bağlamdan çağrılırsa ve farklı tenant'larda aynı external id'ye sahip mesajlar varsa, sistem çapında tüm eşleşen mesajlar güncellenerek tenant izolasyonu ihlal edilecektir.
* **Öneri:** Metoda parametre olarak `Guid tenantId` geçilmeli ve sorguya eklenmelidir.

### 🚨 4. Transaction Boundary Eksikliği ve Yetim (Orphaned) Veri Riski (Medium)
* **Konum:** [MessagingGateway.cs:L107-167](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/MessagingGateway.cs#L107-L167)
* **Bulgu:** `ProcessWebhookAsync` metodunda sırasıyla `CreateConversationAsync`, `AddChannelAsync`, `AddParticipantAsync` ve `AppendMessageAsync` çağrıları yapılmaktadır. Her bir repository metodu kendi içerisinde `SaveChangesAsync()` çağırarak değişiklikleri veri tabanına anında kaydetmektedir.
* **Risk:** Eğer `AppendMessageAsync` adımı herhangi bir kısıt hatası veya hata sebebiyle patlarsa, önceki adımlarda kaydedilmiş olan `Conversation`, `Channel` ve `Participant` kayıtları veri tabanında kalıcı olarak **yetim/boş** bir şekilde kalacaktır (veri tabanı kirliliği).
* **Öneri:** Gateway düzeyinde tüm bu süreç tek bir veri tabanı transaction bloğuna sarılmalı veya repository metodlarındaki anlık `SaveChangesAsync` çağrıları kaldırılarak tek seferde commit edilmesi sağlanmalıdır.

---

## Suggestions

* **Attachment ScanStatus Varsayılanı:** `MessagingGateway.cs` içinde ekler kaydedilirken durum doğrudan `ScanStatus = AttachmentScanStatus.Clean` olarak set edilmektedir. Güvenlik politikaları gereği eklerin başlangıç durumunun `Scanning` olması ve bir antivirüs servisi tarafından tarandıktan sonra `Clean` yapılması daha güvenlidir.
* **Split-Brain Veri Modeli Riski:** Sistemde halihazırda eski WhatsApp ve Canlı Chat mesaj tabloları (`WhatsAppMessages`, `ChatMessages`) mevcuttur. Yeni OMC tabloları ile eski tabloların veri bütünlüğü ve geçmişe dönük veri göçü (migration plan) netleştirilmelidir.

---

## Final Verdict

* **STATUS:** **CONDITIONAL PASS** (Yukarıda listelenen 2 adet yüksek ve 2 adet orta seviyeli kritik bulgunun düzeltilmesi şartıyla geçiş uygundur).
