# 🌐 Microservice Boundary Plan

**Title:** Microservice Boundary Plan  
**Version:** 1.0.0  
**Status:** Approved / Freeze  
**Owner:** Architecture Board  
**Last Updated:** 2026-07-10  
**Dependencies:** None  

---

Bu doküman, Omnichannel Messaging Core (OMC) modülünün ilerleyen aşamalarda monolit yapıdan ayrılarak bağımsız bir **Messaging Gateway Mikroservisi** olarak konumlandırılması durumunda değişmeyecek sözleşmeleri, sınırları ve entegrasyon arayüzlerini tanımlar.

## Mikroservis Ayrım Mimarisi

Ayrım sonrasında OMC Mikroservisi sadece **Kanal Bağlantı ve Mesaj Taşıma (I/O)** görevini üstlenecek; veri tabanı yazma yükü, AI işleme ve CRM eşleştirme mantıkları Event Bus üzerinden asenkron olarak diğer mikroservislere (örn: `CustomerEngagementService`, `EnterpriseAiService`) delege edilecektir.

---

## Değişmeyecek Arayüzler (Stable Interfaces)

Ayrım sonrasında C# kod tabanında tamamen aynı kalacak olan çekirdek arayüzler şunlardır:

1. [IMessagingGateway](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Abstractions/Messaging/IMessagingGateway.cs)  
   * **Rolü:** Webhook isteklerini normalize edip sisteme sokan ana giriş kapısıdır. Mikroservis içinde HTTP Controller'lar tarafından çağrılmaya devam edecektir.
2. [IChannelAdapter](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Abstractions/Messaging/IChannelAdapter.cs)  
   * **Rolü:** Kanala özel imza doğrulama, normalizasyon ve gönderme mantığını kapsüller. Yeni kanallar (Örn: Telegram) eklendiğinde sadece bu arayüzden türeyen adaptörler yazılacaktır.

---

## Kararlı DTO Modelleri (Immutable Contracts)

Ağ üzerinden (JSON ile) taşınan ve mikroservis sınırları arasında asla bozulmayacak veri transfer nesneleri (DTOs):

* [InboundMessageEnvelope](file:///Users/emre/Elyafgroup/src/EmareTicket.Contracts/Messaging/InboundMessageEnvelope.cs): Dış kanallardan gelen normalize edilmiş mesaj gövdesi.
* [OutboundMessageEnvelope](file:///Users/emre/Elyafgroup/src/EmareTicket.Contracts/Messaging/OutboundMessageEnvelope.cs): Sistemin dış kanallara göndermek istediği normalize edilmiş yanıt gövdesi.
* [MessageParticipant](file:///Users/emre/Elyafgroup/src/EmareTicket.Contracts/Messaging/MessageParticipant.cs) & [MessageAttachment](file:///Users/emre/Elyafgroup/src/EmareTicket.Contracts/Messaging/MessageAttachment.cs): Katılımcı ve eklenti tanımlayıcıları.

---

## Entegrasyon Eventlerinin Versiyonlanması (Event Versioning)

Mikroservis dış ortama olay yayınlarken event isimlerinde ve şemalarında semantik versiyonlama (`v1`, `v2`) kullanır.
* **Örnek:**
  * `Emare.Events.Messaging.MessageReceived.v1`
  * `Emare.Events.Messaging.ConversationCreated.v1`
* **Kural:** Şemaya zorunlu alan eklenmesi veya mevcut alanların silinmesi durumunda yeni bir event versiyonu (`v2`) yayınlanır; eski versiyon (`v1`) en az bir majör sürüm boyunca geriye dönük uyumluluk (backward compatibility) için desteklenmeye devam eder.

---

## Kamu API Giriş Noktaları (Public API Endpoints)

Mikroservisin dış ağa ve API Gateway'e açacağı kararlı HTTP API'leri:

| Metot | URI / Path | Sorumluluk | Erişim Tipi |
|---|---|---|---|
| **POST** | `/api/v1/messaging/webhooks/{channel}` | Dış sağlayıcılardan gelen webhook olaylarını kabul eder. | Anonim / Public |
| **POST** | `/api/v1/messaging/send` | Diğer mikroservislerin dış kanallara mesaj göndermesini sağlar. | Dahili JWT (Internal Auth) |
| **GET** | `/api/v1/messaging/health` | Adaptörlerin sağlık durumlarını ve kanal bağlantı kalitesini izler. | Monitor / Internal |
