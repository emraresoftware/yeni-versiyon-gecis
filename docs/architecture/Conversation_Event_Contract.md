# ⚡ Conversation Event Contract

**Title:** Conversation Event Contract  
**Version:** 1.0.0  
**Status:** Approved / Freeze  
**Owner:** Architecture Board  
**Last Updated:** 2026-07-10  
**Dependencies:** EVENT_BUS.md  

---

Bu doküman, Omnichannel Messaging Core (OMC) kapsamında yayınlanacak ve tüketilecek olan tüm olayların (events) sözleşmesini ve veri şemalarını tanımlar. Bütün mesajlaşma kanalları bu standart olay modellerine uymak zorundadır.

## Temel Event Üst Bilgisi (Event Envelope)
Tüm olaylar `EVENT_BUS.md` standardına uygun olarak aşağıdaki ortak üst bilgi alanlarını taşır:
```json
{
  "eventId": "guid",
  "eventType": "string",
  "aggregateId": "guid",
  "aggregateType": "Conversation",
  "tenantId": "guid",
  "userId": "guid?",
  "occurredAt": "datetime-utc",
  "version": 1,
  "correlationId": "guid",
  "traceId": "string"
}
```

---

## Olay Detayları

### 1. ConversationCreated
* **Amacı:** Sisteme herhangi bir kanaldan (WebWidget, WhatsApp, Messenger vb.) ilk defa gelen veya zaman aşımı sonrasında yeni açılan bir konuşma oturumu başladığında yayınlanır.
* **Producer:** `MessagingCore.OmniMessageOrchestrator`
* **Consumer:** `ConversationEngine`, `CrmService`, `AiAgentRouter`, `AuditService`
* **Payload:**
  ```json
  {
    "conversationId": "guid",
    "channel": "WhatsApp | Messenger | Instagram | WebWidget | Email",
    "channelAccountId": "string (WABA ID / Meta Page ID / Email address)",
    "externalConversationId": "string",
    "initiator": {
      "externalParticipantId": "string",
      "role": "visitor",
      "name": "string?",
      "email": "string?",
      "phone": "string?"
    }
  }
  ```
* **Idempotency:** `conversationId` bazlı deduplication yapılır.
* **Retry:** Üç defa (exponetial backoff: 2s, 10s, 30s), ardından DLQ.
* **Ordering:** `conversationId` partition key olarak kullanılır. Bu event, bu aggregate için mutlaka ilk işlenen event olmalıdır.

---

### 2. ConversationUpdated
* **Amacı:** Konuşmanın durumu, atanan temsilci veya eşleşen cari bilgileri değiştiğinde yayınlanır.
* **Producer:** `MessagingCore.ConversationEngine`
* **Consumer:** `LiveChatHub` (UI updates), `CrmService`, `AiAgentRouter`, `AnalyticsService`
* **Payload:**
  ```json
  {
    "conversationId": "guid",
    "status": "Open | Pending | Resolved | Closed",
    "assignedUserId": "guid?",
    "customerId": "guid?",
    "activeSupportTicketId": "guid?",
    "lastMessageAt": "datetime-utc",
    "lastMessagePreview": "string?"
  }
  ```
* **Idempotency:** `conversationId` ve `occurredAt` (timestamp) bazlı son durumu ezme (last-write-wins).
* **Retry:** Hızlı retry (3 defa), başarısızlık kritik değildir (UI state).
* **Ordering:** `conversationId` bazlı sıralı işlenir.

---

### 3. ConversationClosed
* **Amacı:** Görüşme temsilci veya AI tarafından çözüldü/kapatıldı durumuna getirildiğinde yayınlanır.
* **Producer:** `MessagingCore.ConversationEngine`
* **Consumer:** `CrmService` (Timeline log), `AnalyticsService` (CSAT Survey Trigger), `WorkflowEngine`
* **Payload:**
  ```json
  {
    "conversationId": "guid",
    "closedAt": "datetime-utc",
    "closedByUserId": "guid?",
    "reason": "resolved | timeout | abandoned",
    "durationSeconds": 1200
  }
  ```
* **Idempotency:** `conversationId` kontrol edilerek mükerrer anket/log engellenir.
* **Retry:** 5 defa exponential backoff ile retry edilir. Kaybolması kritik olduğundan DLQ'ya düşürülür.
* **Ordering:** `conversationId` bazlı sıralı.

---

### 4. MessageReceived
* **Amacı:** Dış dünyadan (müşteriden) yeni bir normalize edilmiş mesaj OMC Gateway'e ulaştığında yayınlanır.
* **Producer:** `MessagingCore.MessagingGateway`
* **Consumer:** `ConversationEngine`, `LiveChatHub` (Temsilci ekranı), `AuditService`
* **Payload:**
  ```json
  {
    "messageId": "guid",
    "externalMessageId": "string",
    "conversationId": "guid",
    "channel": "WhatsApp | Messenger | Instagram | WebWidget | Email",
    "direction": "Inbound",
    "messageType": "Text | Image | Video | Audio | Document | Location | InteractiveResponse",
    "text": "string?",
    "senderId": "string (PSID / Phone / Email)",
    "attachments": [
      {
        "attachmentId": "guid",
        "url": "string",
        "mimeType": "string?",
        "filename": "string?",
        "fileSize": 1024
      }
    ],
    "rawPayloadHash": "string",
    "metadata": {}
  }
  ```
* **Idempotency:** `omc_idempotency:{channel}:{externalMessageId}` key ile gateway seviyesinde deduplication yapılır.
* **Retry:** 3 defa. Hata durumunda DLQ.
* **Ordering:** `conversationId` partition key. Mesajlar zaman sırasına göre işlenmelidir.

---

### 5. MessageDelivered
* **Amacı:** Gönderdiğimiz (outbound) mesajın hedef cihaza veya kanal sunucusuna başarıyla teslim edildiğini bildiren webhook olayıdır.
* **Producer:** `MessagingCore.ChannelAdapter` (webhook status updates)
* **Consumer:** `ConversationEngine`, `LiveChatHub` (UI ticks)
* **Payload:**
  ```json
  {
    "externalMessageId": "string",
    "deliveredAt": "datetime-utc"
  }
  ```
* **Idempotency:** `externalMessageId` ve durum (`Delivered`) bazlı veri tabanı güncellenir.
* **Retry:** 3 defa. Başarısızlık durumunda loglanır, DLQ zorunlu değildir.
* **Ordering:** Sıra bağımlılığı yoktur.

---

### 6. MessageRead
* **Amacı:** Gönderdiğimiz mesajın müşteri tarafından okunduğuna dair kanal durum güncellemesidir.
* **Producer:** `MessagingCore.ChannelAdapter`
* **Consumer:** `ConversationEngine`, `LiveChatHub` (UI double ticks)
* **Payload:**
  ```json
  {
    "externalMessageId": "string",
    "readAt": "datetime-utc"
  }
  ```
* **Idempotency:** `externalMessageId` üzerinden `ReadAt` alanı güncellenir, mükerrer güncelleme ezilir.
* **Retry:** 3 defa.
* **Ordering:** Sıra bağımlılığı yoktur.

---

### 7. MessageFailed
* **Amacı:** Müşteriye gönderilmeye çalışılan bir outbound mesajın başarısız olduğunu (Örn: geçersiz numara, engelleme, kota aşımı) bildirir.
* **Producer:** `MessagingCore.ChannelAdapter` ya da `MessagingGateway.OutboundDispatcher`
* **Consumer:** `ConversationEngine`, `LiveChatHub` (UI error icon), `AuditService`
* **Payload:**
  ```json
  {
    "externalMessageId": "string",
    "failedAt": "datetime-utc",
    "errorCode": "string",
    "errorMessage": "string"
  }
  ```
* **Idempotency:** `externalMessageId` üzerinden mesaj durumu `Failed` olarak güncellenir.
* **Retry:** 3 defa. Hata logu kritik olduğundan DLQ'ya atılır.
* **Ordering:** Sıra bağımlılığı yoktur.

---

### 8. MessageDeleted
* **Amacı:** Ziyaretçi veya temsilci gönderdiği mesajı sildiğinde (Örn: WhatsApp "Herkesten Sil") tetiklenir.
* **Producer:** `MessagingCore.ChannelAdapter`
* **Consumer:** `ConversationEngine`, `LiveChatHub` (UI message removal)
* **Payload:**
  ```json
  {
    "externalMessageId": "string",
    "deletedAt": "datetime-utc"
  }
  ```
* **Idempotency:** `externalMessageId` ile veri tabanında mesaj `IsDeleted = true` yapılır.
* **Retry:** 3 defa.
* **Ordering:** `conversationId` bazlı sıralı işlenir.

---

### 9. MessageEdited
* **Amacı:** Gönderilen bir mesaj üzerinde sonradan düzenleme yapıldığında tetiklenir.
* **Producer:** `MessagingCore.ChannelAdapter`
* **Consumer:** `ConversationEngine`, `LiveChatHub` (UI text replacement)
* **Payload:**
  ```json
  {
    "externalMessageId": "string",
    "newText": "string",
    "editedAt": "datetime-utc"
  }
  ```
* **Idempotency:** `externalMessageId` üzerinden text güncellenir.
* **Retry:** 3 defa.
* **Ordering:** `conversationId` bazlı sıralı.

---

### 10. HumanTakeoverStarted
* **Amacı:** AI asistan devreden çıkarılıp, görüşme manuel olarak bir insan temsilciye aktarıldığında (Human Escalation) tetiklenir.
* **Producer:** `EnterpriseIntelligence.NextBestAction` veya `MessagingCore.ConversationEngine` (manuel temsilci atama)
* **Consumer:** `AiAgentRouter` (AI auto-replies are paused), `LiveChatHub` (Agent notification), `CrmService` (Timeline activity)
* **Payload:**
  ```json
  {
    "conversationId": "guid",
    "assignedUserId": "guid",
    "triggerSource": "Rule | Sentiment | ExplicitUserRequest | OperatorClaim",
    "startedAt": "datetime-utc"
  }
  ```
* **Idempotency:** `conversationId` bazlı durum `HumanTakeover = active` olarak set edilir.
* **Retry:** 5 defa exponential backoff.
* **Ordering:** `conversationId` bazlı.

---

### 11. HumanTakeoverFinished
* **Amacı:** Temsilci görüşmeyi sonlandırdığında veya "AI asistanı geri aktar" butonuna bastığında tetiklenir.
* **Producer:** `MessagingCore.ConversationEngine` (temsilcinin aksiyonu veya timeout)
* **Consumer:** `AiAgentRouter` (AI auto-replies are resumed), `LiveChatHub` (UI updates)
* **Payload:**
  ```json
  {
    "conversationId": "guid",
    "finishedAt": "datetime-utc",
    "releasedByUserId": "guid?",
    "reason": "resolved | manual_release | timeout"
  }
  ```
* **Idempotency:** `conversationId` bazlı durum güncellemesi yapılır.
* **Retry:** 3 defa.
* **Ordering:** `conversationId` bazlı.

---

### 12. AIResponseGenerated
* **Amacı:** Enterprise Intelligence veya AI servis katmanı, inbound mesaja karşılık otomatik bir yanıt (taslak veya doğrudan gönderilecek mesaj) ürettiğinde yayınlanır.
* **Producer:** `EnterpriseIntelligence.ResponseGenerator`
* **Consumer:** `MessagingCore.OutboundDispatcher`, `LiveChatHub` (Temsilci ekranına taslak düşürme)
* **Payload:**
  ```json
  {
    "messageId": "guid",
    "conversationId": "guid",
    "text": "string",
    "attachments": [],
    "isDraft": "boolean",
    "generatedByAgent": "SupportAgent | SalesAgent | OrderAgent | AppointmentAgent"
  }
  ```
* **Idempotency:** `messageId` bazlı kontrol edilir.
* **Retry:** 3 defa.
* **Ordering:** `conversationId` bazlı sıralı.

---

### 13. AIResponseRejected
* **Amacı:** Temsilci, AI tarafından hazırlanan taslak yanıtı beğenmeyip sildiğinde veya düzenlediğinde tetiklenir.
* **Producer:** `LiveChatHub` / `ConversationEngine`
* **Consumer:** `EnterpriseIntelligence.Memory` (Ajanı eğitmek/geri bildirim sağlamak için)
* **Payload:**
  ```json
  {
    "conversationId": "guid",
    "originalAiText": "string",
    "rejectedByUserId": "guid",
    "rejectedAt": "datetime-utc",
    "customFeedback": "string?"
  }
  ```
* **Idempotency:** Event bazlı audit log oluşturulur.
* **Retry:** 3 defa.
* **Ordering:** Sıra bağımlılığı yoktur.

---

### 14. AttachmentUploaded
* **Amacı:** Bir eklenti (resim, pdf, ses vb.) başarıyla güvenli nesne depolama alanına yüklenip virüs taramasından geçtiğinde yayınlanır.
* **Producer:** `MessagingCore.AttachmentService`
* **Consumer:** `ConversationEngine`, `LiveChatHub`, `CrmService`
* **Payload:**
  ```json
  {
    "attachmentId": "guid",
    "conversationId": "guid",
    "url": "string",
    "storageKey": "string",
    "mimeType": "string",
    "fileSize": 2048576,
    "filename": "string"
  }
  ```
* **Idempotency:** `attachmentId` bazlı.
* **Retry:** 3 defa.
* **Ordering:** Sıra bağımlılığı yoktur.
