# 🧬 Conversation Model Standard

**Title:** Conversation Model Standard  
**Version:** 1.0.0  
**Status:** Approved / Freeze  
**Owner:** Architecture Board  
**Last Updated:** 2026-07-10  
**Dependencies:** DOMAIN_MODEL.md  

---

Bu doküman, Omnichannel Messaging Core (OMC) bünyesindeki veri tabanı modelleme standartlarını ve kanalların konuşma oturumlarıyla (Conversations) nasıl ilişkilendirileceğine dair mimari kararları tanımlar.

## Mimari Karar: Tek Konuşmada Çoklu Kanal (Unified Omni-Channel Threading)

OMC kapsamında konuşma oturumlarının nasıl modelleneceğine dair yapılan analiz ve verilen kesin mimari karar aşağıdadır:

### Seçenek A: Tek Konuşma İçinde Çok Kanal (Seçilen Model)
Müşteriyle olan görüşme mantıksal bir bütündür. Müşteri sabah WhatsApp'tan yazıp, öğlen Facebook Messenger'dan devam ettiğinde, bu etkileşimler tek bir `Conversation` altında birleştirilir.

* **Avantajları:**
  * **Bütünsel Müşteri Deneyimi (Unified Context):** Operatör ve yapay zeka ajanları, müşterinin tüm kanallardaki yazışma geçmişini tek bir ekranda kesintisiz görür. AI bağlam kaybetmez.
  * **CRM ve Ticket Bütünlüğü:** Görüşmeye bağlı aktif destek talebi (`SupportTicket`) ve cari kartı (`CustomerId`) tektir, mükerrer kayıt açılmasını engeller.
  * **Modülerlik:** Kanallar arası geçişlerde (Handoff) konuşma durumunun korunması kolaylaşır.
* **Dezavantajları:**
  * **Yanıt Yönlendirme (Outbound Routing) Karmaşıklığı:** Operatör yanıt verdiğinde sistemin mesajı hangi kanaldan (WhatsApp mı, Messenger mı) göndereceğini bilmesi gerekir. Bu durum, her mesajın hangi kanaldan geldiğinin (`Channel`) ve aktif kanal eşleşmelerinin takibini gerektirir.

### Seçenek B: Her Kanal İçin Ayrı Konuşma
Her WhatsApp numarası veya Meta PSID (Page Scoped ID) için bağımsız bir konuşma kaydı açılır.

* **Avantajları:**
  * **Basit Veri Modeli:** Eşleştirme ve veri tabanı şeması basittir. Yönlendirme (routing) doğrusal çalışır.
* **Dezavantajları:**
  * **Kırık Zaman Akışı (Fractured Timeline):** Operatör ekranında aynı müşteriye ait 3-4 farklı sohbet sekmesi açık kalır.
  * **AI Bağlam Eksikliği:** Yapay zeka WhatsApp'ta konuşulan bir konuyu Messenger'da hatırlamaz.

---

### Kesin Mimari Karar (Verdict)
Emare Shared Intelligence vizyonuna uygun olarak **"Tek Konuşma İçinde Çoklu Kanal (Seçenek A)"** kararlaştırılmıştır. 

Sistem bunu çözmek için **Hibrit İlişkilendirme Şeması** kullanacaktır:
1. `Conversation` aggregate root'u tek bir müşteri görüşmesini temsil eder.
2. Bir `Conversation`, birden fazla `ConversationChannel` kaydına sahip olabilir (Çoklu kanal adresi bağlama).
3. Gelen her `ConversationMessage` kendi kanalı (`Channel`) ve gönderici kimliğiyle (`ExternalMessageId`, `SenderId`) kaydedilir.
4. Operatör veya AI yanıt verdiğinde, mesaj **son gelen aktif kanal adresi** üzerinden (`ConversationChannel.IsActive == true` veya en son mesajın kanalı baz alınarak) dış dünyaya yönlendirilir.

---

## Veri Modeli Standartları

### 1. Conversation Tablo Şeması
```csharp
public class Conversation : AuditableEntity, ITenantEntity
{
    public Guid Id { get; set; }
    public Guid? TenantId { get; set; }
    public Guid? CustomerId { get; set; }            // CRM Cari Kartı
    public Guid? AssignedUserId { get; set; }         // İnsan Operatör
    public Guid? ActiveSupportTicketId { get; set; }  // Aktif Destek Talebi
    public ConversationStatus Status { get; set; } = ConversationStatus.Open;
    public DateTime LastMessageAt { get; set; }
    public string? LastMessagePreview { get; set; }
    public int UnreadCount { get; set; }

    public Customer? Customer { get; set; }
    public User? AssignedUser { get; set; }
    public SupportTicket? ActiveSupportTicket { get; set; }

    // İlişkili Alt Koleksiyonlar
    public ICollection<ConversationChannel> Channels { get; set; } = new List<ConversationChannel>();
    public ICollection<ConversationParticipant> Participants { get; set; } = new List<ConversationParticipant>();
    public ICollection<ConversationMessage> Messages { get; set; } = new List<ConversationMessage>();
}
```

### 2. ConversationChannel Tablo Şeması
Müşterinin bu konuşmaya dahil olduğu aktif adres eşleşmelerini tutar.
```csharp
public class ConversationChannel : BaseEntity, ITenantEntity
{
    public Guid Id { get; set; }
    public Guid? TenantId { get; set; }
    public Guid ConversationId { get; set; }
    public OmniChannelType Channel { get; set; }      // WhatsApp, Messenger vb.
    public string ChannelExternalId { get; set; } = string.Empty; // Telefon no, PSID, Email adresi
    public bool IsPreferred { get; set; } = false;    // Tercih edilen iletişim kanalı mı?
    public bool IsActive { get; set; } = true;         // Kanal şu an aktif/açık mı?

    public Conversation Conversation { get; set; } = null!;
}
```

### 3. ConversationParticipant Tablo Şeması
Katılımcıların (müşteri temsilcileri, AI botları veya müşteri kontakları) rollerini belirler.
```csharp
public class ConversationParticipant : BaseEntity, ITenantEntity
{
    public Guid Id { get; set; }
    public Guid? TenantId { get; set; }
    public Guid ConversationId { get; set; }
    public Guid? UserId { get; set; }                 // Sistem Kullanıcısı (Temsilci/Süpervizör)
    public Guid? ContactId { get; set; }              // CRM Kişi (Müşteri Kontağı)
    public string Role { get; set; } = "visitor";     // visitor | agent | system_bot | supervisor

    public Conversation Conversation { get; set; } = null!;
    public User? User { get; set; }
}
```

---

## Veri Bütünlüğü ve Kısıtlamalar
* **TenantId:** Tüm alt tablolar (`ConversationChannel`, `ConversationParticipant`) üst root olan `Conversation` ile aynı `TenantId` alanını taşımak ve doğrulamak zorundadır.
* **IsDeleted (Soft Delete):** Konuşma geçmişinin silinmesi durumunda tüm ilişkili mesajlar ve kanallar eş zamanlı olarak soft-delete yapılmalıdır (`IsDeleted = true`).
