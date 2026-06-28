# 📋 TASK 016 — AI Voice Bridge Refactor Plan (TASK_016_AI_VOICE_BRIDGE_REFACTOR_PLAN.md)

**Title:** AI Voice Bridge Refactor & Integration Plan  
**Version:** 1.0.0  
**Status:** Draft / Proposed  
**Owner:** Security & Architecture Team / Agent 3  
**Last Updated:** 2026-06-28  
**Task Number:** TASK 016  
**Dependencies:** AI_VOICE_ERP_NIGHTLY_QA.md, TASK_014_REPORT.md, SECURITY_AUTHORIZATION.md, EVENT_BUS.md  
**Related Documents:** STATUS.md, 2026-06-28.md  

---

## 1. Giriş ve Amaç (Executive Summary)

**Emare Ai Dashboard** platformunun Asterisk PBX ve Python AudioSocket ses köprüsü (Gemini Live API entegrasyonu) mimarisi olan **AI Voice Bridge** (`gemini-live-standalone`), mevcut yapıda PostgreSQL veritabanına `asyncpg` ve ham SQL (raw SQL) sorguları ile doğrudan erişmektedir. 

Bu yapı;
*   [SECURITY_AUTHORIZATION.md](file:///Users/emre/yeni-versiyon-gecis/SECURITY_AUTHORIZATION.md) § 5'te yer alan *"AI Ajanları veritabanına doğrudan bağlanamaz"* güvenlik anayasasını ihlal etmektedir.
*   Application katmanındaki MediatR iş kurallarını, FluentValidation doğrulamalarını ve EF Core `SaveChanges` denetimlerini (Audit & Outbox) tamamen baypas etmektedir.
*   Giriş verilerinin doğrulanamaması nedeniyle PostgreSQL veritabanında tarih-saat uyuşmazlığı ve veri bütünlüğü riskleri doğurmaktadır.

Bu planın amacı; AI Voice Bridge'in veritabanı bağlantılarını tamamen kaldırıp, tüm okuma ve yazma işlemlerini platformun resmi **REST API / CQRS** hattına taşımaktır.

---

## 2. Mevcut Durum Analizi: Hangi Araçlar Raw SQL Kullanıyor?

`AI_VOICE_ERP_NIGHTLY_QA.md` raporuna göre, Python tarafındaki `standalone_bridge.py` içerisinde veritabanına doğrudan sorgu atan araçlar (tools) şunlardır:

1.  **`create_support_ticket_db`:** `"SupportTickets"` ve `"SupportTicketActivities"` tablolarına doğrudan `INSERT` atarak ticket oluşturmaktadır.
2.  **`create_appointment_db`:** `"Appointments"` tablosuna doğrudan `INSERT` yapmaktadır.
3.  **`create_order_db`:** `"Orders"`, `"OrderItems"` ve `"Products"` tablolarına doğrudan sipariş ve kalem verisi yazmaktadır.
4.  **`update_customer_context`:** Eski taslak mimarideki `"Customers"` ve `"CustomerContacts"` tablolarına arayan bilgisi güncelleme ve çağrı notları (activity log) yazmaktadır.
5.  **`check_ticket_status_db`:** Arayanın Customer ID'sine göre son 5 ticket durumunu doğrudan `"SupportTickets"` tablosundan okumaktadır.
6.  **Arayan Kimliği Sorgusu (Caller Lookup):** Gelen çağrının telefon numarasını doğrudan veritabanında aratarak cari hesap (Account) ve yetkili kişi (Contact) çözümlemektedir.

---

## 3. Tool Entegrasyon ve API Eşleme Tablosu

Bridge içerisindeki tüm araçların API katmanına yönlendirilmesi ve ilgili CQRS komut/sorgularıyla eşleşmesi aşağıdaki tabloda kurgulanmıştır:

| Voice Tool | İşlem Tipi | Hedef API Endpoint | Tetiklenen CQRS Command/Query | Etkilenen Entity | İhtiyaç Duyulan Yetki |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **`caller_lookup`** | Read | `GET /api/crm/contacts/by-phone/{phone}` | `GetCrmContactByPhoneQuery` | `CrmContact`, `CrmAccount` | `CRM.Contact.Read` |
| **`create_support_ticket`** | Write | `POST /api/support-tickets` | `CreateSupportTicketCommand` | `SupportTicket` | `Ticket.Write` |
| **`check_ticket_status`** | Read | `GET /api/support-tickets/customer/{customerId}` | `ListSupportTicketsQuery` | `SupportTicket` | `Ticket.Read` |
| **`create_appointment`** | Write | `POST /api/appointments` | `CreateAppointmentCommand` | `Appointment` | `Appointment.Write` |
| **`create_order`** | Write | `POST /api/sales/orders` | `CreateSalesOrderCommand` | `SalesOrder`, `SalesOrderItem` | `Sales.Order.Write` |
| **`create_crm_opportunity`** | Write | `POST /api/crm/opportunities` | `CreateCrmOpportunityCommand` | `CrmOpportunity` | `CRM.Opportunity.Write` |
| **`create_crm_proposal`** | Write | `POST /api/crm/proposals` | `CreateCrmProposalCommand` | `CrmProposal`, `CrmProposalItem` | `CRM.Proposal.Write` |
| **`log_call_activity`** | Write | `POST /api/crm/activities` | `CreateCrmActivityCommand` | `CrmActivity` | `CRM.Activity.Write` |

---

## 4. Güvenlik, Servis Hesabı ve JWT İzin Modeli

Ses köprüsünün backend API'lerini güvenli şekilde çağırabilmesi için bir **Servis Hesabı (Service Account)** modeli kurgulanacaktır:

1.  **Rol Tanımı:** [SECURITY_AUTHORIZATION.md](file:///Users/emre/yeni-versiyon-gecis/SECURITY_AUTHORIZATION.md) dosyasına yeni bir sistem rolü eklenecektir: **`VoiceBridgeService`**.
2.  **Kimlik Doğrulama:** Python Voice Bridge başlangıçta kendi ClientId ve ClientSecret (Service Key) bilgileriyle platformun auth servisine istek atacaktır:
    *   `POST /api/auth/token` (grant_type: `client_credentials`)
    *   Dönen JWT token `gemini-live-standalone` hafızasında tutulacak ve süresi bittiğinde otomatik yenilenecektir.
3.  **İzin Sınırlandırması (Least Privilege):** `VoiceBridgeService` rolüne sadece yukarıdaki matriste yer alan kısıtlı okuma ve yazma yetkileri (`CRM.Contact.Read`, `Ticket.Write`, `Sales.Order.Write` vb.) tanımlanacaktır. Global admin yetkileri verilmeyecektir.

---

## 5. Güvenli Kiracı (TenantId) Taşıma Protokolü

Çok kiracılı (multi-tenant) sistemlerde ses köprüsünün hangi kiracının verilerine erişeceğini belirlemesi ve bunu API'ye güvenli şekilde iletmesi gerekmektedir:

```text
SIP Çağrısı Gelir (Örn: +90 212 555 1212)
      ↓
Voice Bridge, SIP Trunk veya Hedef DID Numarasıyla TenantId Eşlemesini Çözer
      ↓
API Çağrısı Yapılır: Authorization: Bearer {Token} + X-Tenant-Id: {Resolved-Tenant-UUID}
      ↓
API Gateway / Middleware: Servis Hesabının Yetkisini ve X-Tenant-Id Değerini Doğrular
      ↓
ITenantProvider: TenantId'yi HTTP Context'e Set Eder ve EF Core HasQueryFilter'ı Devreye Sokar
```

*   **Güvenlik Doğrulaması (Middleware Check):** 
    Sadece `VoiceBridgeService` rolüne sahip token'ların istek başlığında (Header) harici bir `X-Tenant-Id` UUID taşımasına izin verilecektir. Standart kullanıcı isteklerinde bu başlık dikkate alınmayacak ve güvenlik bypass girişimleri engellenecektir.
*   **Doğrulama Filtresi (Cross-Check):**
    Middleware, gelen çağrı sahibinin (arayan telefon numarası) gerçekten de istekte belirtilen `X-Tenant-Id` kiracısına ait olup olmadığını veya SIP Trunk DID numarasının o kiracıya kayıtlı olup olmadığını veritabanından doğrulayacaktır.

---

## 6. Audit, Outbox ve Domain Event Entegrasyonu

İşlemlerin doğrudan veritabanı yerine REST API CQRS hattına taşınmasıyla event ve log sistemleri otomatik olarak garanti altına alınır:

1.  **Denetim İzi (Auditing):** İstekler `VoiceBridgeService` kullanıcı context'i ile MediatR pipeline'ına gireceği için, EF Core `AuditableEntitySaveChangesInterceptor` interceptor'ı oluşturulan/güncellenen kayıtlara otomatik olarak `CreatedBy = "VoiceBridgeService"` ve `CreatedAt = DateTime.UtcNow` değerlerini yazar.
2.  **İş Kuralları Doğrulaması:** FluentValidation boruları devreye girerek geçersiz veri (negatif sipariş tutarı, hatalı telefon formatı vb.) yazılmasını engeller ve bridge'e `400 Bad Request` hatası döner. AI bu hatayı yorumlayarak sesli olarak kullanıcıya bildirebilir.
3.  **Domain Event ve Outbox Garantisi:** Handler içerisinde tetiklenen (örn. `CrmOpportunityCreated`) domain event'leri, EF Core outbox interceptor'ı ile aynı DB transaction'ında `OutboxMessages` tablosuna yazılır. Arka plan servisi bu event'leri alarak Event Bus'a (RabbitMQ/Masstransit) iletir ve böylece CEO/Sales Dashboard kulelerine ciro verileri anlık yansır.

---

## 7. Production Blocker Listesi (Canlıya Geçiş Engelleri)

Aşağıdaki açıklar giderilmeden sistemin canlı sunuculara (`185.189.54.107` / `31.169.72.85`) deploy edilmesi **kesinlikle yasaktır**:

1.  **`standalone_bridge.py` içindeki PostgreSQL Bağlantısı:** Python kodundaki Postgres connection string parametreleri tamamen kaldırılmalı ve `asyncpg` kütüphanesi devre dışı bırakılmalıdır.
2.  **Direct DB Erişim Yetkisi:** Canlı veritabanı güvenlik duvarında (firewall) sadece `EmareTicket.API` ip adresine izin verilmeli; Asterisk/Python sunucusunun PostgreSQL portuna doğrudan erişimi kapatılmalıdır.
3.  **UTC Tarih Hatası:** `CallCampaignsController.cs#L326` satırındaki `DateTime.Now` kullanımı, Postgres `timestamptz` sütunlarında runtime 500 hatası vermemesi için `DateTime.UtcNow` olarak düzeltilmelidir.
4.  **AI Karar Onay Kontrolü:** AI sesli aramada teklif onaylama yetkisine sahip olmamalıdır; teklifleri onaylamak için sadece "onay isteği" oluşturmalı, onay bir insan tarafından arayüzden yapılmalıdır (Human-in-the-loop).

---

## 8. Refactor Task Listesi

Refactor süreci 4 aşamada gerçekleştirilecektir:

### Faz 1: API / Backend Hazırlığı (Platform.API)
*   [ ] `SECURITY_AUTHORIZATION.md` dosyasına `VoiceBridgeService` rolünün ve ilişkili izinlerin eklenmesi.
*   [ ] `POST /api/auth/token` servisine `client_credentials` grant_type desteğinin veya ses köprüsüne özel API Key doğrulama mekanizmasının entegre edilmesi.
*   [ ] `X-Tenant-Id` başlığını okuyan ve sadece `VoiceBridgeService` rolüne sahip isteklere tenant override izni veren güvenli Middleware yazılması.
*   [ ] `CallCampaignsController` içindeki `DateTime.Now` ifadesinin `DateTime.UtcNow` ile değiştirilmesi.

### Faz 2: Python Voice Bridge Geliştirmesi (`gemini-live-standalone`)
*   [ ] `asyncpg` veritabanı kütüphanesinin ve veritabanı secrets tanımlarının bridge projesinden silinmesi.
*   [ ] Python `httpx` (asynchronous HTTP client) kütüphanesinin projeye eklenmesi.
*   [ ] Platform API'si ile haberleşecek `EmareApiClient` sınıfının yazılması (otomatik JWT login ve token yenileme özellikli).
*   [ ] `caller_lookup`, `create_support_ticket`, `create_appointment`, `create_order` araçlarının (tools) doğrudan SQL yazmak yerine REST API uçlarını çağıracak şekilde refactor edilmesi.
*   [ ] Çağrı notlarının girilmesi için yeni `log_call_activity` aracının implemente edilmesi.

### Faz 3: Test ve Doğrulama
*   [ ] REST API entegrasyonu sonrasında Python ses köprüsü entegrasyon testlerinin API mock servisleriyle çalıştırılması.
*   [ ] MediatR pipeline entegrasyonunun loglarının kontrol edilmesi; Outbox tablosuna kayıt düştüğünün ve eventlerin pub-sub mekanizmasında çalıştığının doğrulanması.
*   [ ] Kiracı izolasyon sızma testleri: Bir tenant SIP numarasından gelen aramayla diğer tenant verilerine erişilemediğinin teyit edilmesi.

---

*Bu plan Agent 3 (Security & CRM Planning) tarafından kurgulanmış olup, kod veya üretim ortamı sırları barındırmaz.*
