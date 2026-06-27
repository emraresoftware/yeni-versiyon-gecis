# ⚡ Event Bus Mimarisi

**Title:** Event Bus Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** README.md
**Related Documents:** WORKFLOW_ENGINE.md, RULE_ENGINE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Emare Business Operating System (BOS), Event Driven Architecture (EDA) kullanır.

Hiçbir modül başka bir modülü doğrudan çağırmaz.

Bütün modüller Event Bus üzerinden haberleşir.

Bu yaklaşım;

* gevşek bağlı (Loose Coupling)
* yüksek ölçeklenebilir
* mikroservis uyumlu
* AI Agent uyumlu

bir mimari oluşturur.

---

# Temel İlke

Her işlem bir Event üretir.

```text
Kullanıcı İşlem Yapar

↓

Business Engine

↓

Domain Event

↓

Event Bus

↓

Subscriber

↓

Yeni İşlem
```

---

# Event Türleri

## Domain Events

İş kuralları sonucunda oluşur.

Örnek

```text
CrmAccountCreated

CrmProposalApproved

FinanceJournalEntryPosted

LogisticsStockReserved

HrLeaveApproved

LogisticsStockTransferCompleted
```

---

## Integration Events

Dış sistemlere gönderilir.

Örnek

```text
InvoiceCreated

↓

e-Fatura

ShipmentCreated

↓

Kargo Firması

PaymentReceived

↓

Muhasebe

SMSSent

↓

CRM
```

---

## System Events

Platform tarafından üretilir.

```text
UserLoggedIn

PasswordChanged

TenantCreated

RoleAssigned

ApiKeyCreated
```

---

# Event Yapısı

Her Event aşağıdaki alanları içerir.

```json
{
  "eventId": "",
  "eventType": "",
  "aggregateId": "",
  "aggregateType": "",
  "tenantId": "",
  "userId": "",
  "occurredAt": "",
  "version": 1,
  "payload": {}
}
```

---

# Event İsimlendirme Standardı

Format

```text
EntityAction
```

Örnek

```text
CrmAccountCreated

CrmAccountUpdated

CrmAccountDeleted

CrmProposalSent

CrmProposalApproved

PurchaseOrderApproved

LogisticsStockTransferCompleted

FinanceJournalEntryPosted

HrEmployeeCreated

HrLeaveApproved

QcTestResultCompleted

LogisticsShipmentDelivered
```

---

# Event Yaşam Döngüsü

```text
Create

↓

Validate

↓

Commit

↓

Publish Event

↓

Subscribers

↓

Completed
```

Event yalnızca başarılı transaction sonrasında yayınlanır.

---

# Retry Mekanizması

Başarısız Event

↓

Retry Queue

↓

Retry 1

↓

Retry 2

↓

Retry 3

↓

Dead Letter Queue

Hiçbir Event kaybolmaz.

---

# Dead Letter Queue (DLQ)

İşlenemeyen Event'ler

DLQ içerisine taşınır.

Yetkili kullanıcılar;

* yeniden çalıştırabilir
* iptal edebilir
* log inceleyebilir
```

---

# Event Sıralaması

Aynı Aggregate için Event sırası korunmalıdır.

Örnek

```text
SalesOrderCreated

↓

StockReserved

↓

ShipmentCreated

↓

InvoiceCreated

↓

AccountingPosted
```

Bu sıra değiştirilemez.

---

# Event Versioning

Her Event version taşır.

```text
CustomerCreated v1

CustomerCreated v2

CustomerCreated v3
```

Eski tüketiciler çalışmaya devam eder.

---

# Idempotency

Bir Event ikinci kez işlense bile aynı sonucu üretmelidir.

Örnek

```text
PaymentReceived
```

iki kez gelirse

↓

Muhasebe kaydı yalnızca bir kez oluşmalıdır.

---

# Event Transaction Kuralı

Aynı transaction içerisinde

Database Commit

↓

Event Publish

sırası korunmalıdır.

Outbox Pattern kullanılması önerilir.

---

# Event Kategorileri

| Event Name | Type | Owner Context | Trigger | Subscribers | Notes |
| ---------- | ---- | ------------- | ------- | ----------- | ----- |
| **CRM** | | | | | |
| `CrmAccountCreated` | Integration / Domain | CRM | Cari hesap (Müşteri) oluşturulduğunda | Finance, AI, Notification | Dış sistem entegrasyonu ve bildirim için. |
| `CrmAccountUpdated` | Domain | CRM | Cari hesap güncellendiğinde | AI, Integration | Veri senkronizasyonu. |
| `CrmAccountDeleted` | Domain | CRM | Cari hesap silindiğinde (soft-delete) | Logistics, Finance | İlişkili işlemlerin kontrolü. |
| `CrmOpportunityCreated` | Domain | CRM | Yeni satış fırsatı açıldığında | AI, Sales | Satış tahmini ve olasılık hesaplama. |
| **Sales** | | | | | |
| `CrmProposalSent` | Integration | Sales / Proposal | Müşteriye teklif gönderildiğinde | Notification, Analytics | Onay bekleyen teklif takibi. |
| `CrmProposalApproved` | Integration | Sales / Proposal | Teklif müşteri tarafından onaylandığında | Finance, Logistics, AI, Notification | Sipariş oluşturma ve faturalandırma. |
| `SalesOrderCreated` | Domain | Sales | Satış siparişi oluşturulduğunda | Warehouse, AI | Stok rezerve tetiklemesi. |
| `SalesOrderApproved` | Integration | Sales | Satış siparişi onaylandığında | Logistics, Production, Finance | Sevk süreci ve üretim planlama. |
| `SalesOrderCancelled` | Integration | Sales | Satış siparişi iptal edildiğinde | Logistics, Finance | Rezervasyon kaldırma ve iade. |
| **Finance** | | | | | |
| `FinanceJournalEntryPosted` | Integration | Finance | Yevmiye fişi onaylanıp deftere işlendiğinde | Analytics, AI | Muhasebe defteri güncellenmesi. |
| `FinanceInvoiceCreated` | Integration | Finance | Fatura kesildiğinde | CRM, Notification, Integration | E-Fatura entegrasyonu. |
| `FinancePaymentReceived` | Integration / Domain | Finance | Tahsilat/Ödeme alındığında | CRM, Notification, Analytics | Cari hesap limit ve bakiye güncellemesi. |
| **HR** | | | | | |
| `HrEmployeeCreated` | Domain | HR | Yeni personel kartı açıldığında | Finance, Security | Rol atamaları ve cari muhasebe hesabı. |
| `HrLeaveApproved` | Integration | HR | İzin onaylandığında | Notification, Workflows | Takvim ve planlama senkronizasyonu. |
| **Logistics** | | | | | |
| `LogisticsStockReserved` | Domain | Logistics | Stok rezerve edildiğinde | Sales, Production | Sipariş hazırlık durumu. |
| `LogisticsStockReleased` | Domain | Logistics | Rezerve çözüldüğünde | Sales, Production | İptaller sonrası stok serbest bırakma. |
| `LogisticsStockTransferCompleted` | Integration | Logistics | Depolar arası transfer tamamlandığında | Analytics, AI | Stok seviyesi güncelleme. |
| `LogisticsShipmentCreated` | Domain | Logistics | Sevk irsaliyesi oluşturulduğunda | Notification, Integration | Kargo firması entegrasyonu. |
| `LogisticsShipmentDelivered` | Integration | Logistics | Teslimat tamamlandığında | CRM, Finance | Fatura tetikleme. |
| **QC (Quality Control)** | | | | | |
| `QcTestResultCompleted` | Domain | QC | Kalite testi tamamlandığında | Production, Logistics | Stok kalite durumu (Kabul/Red). |
| `QcClaimCreated` | Integration | QC | Kalite şikâyeti / CAPA açıldığında | CRM, Production, AI | Müşteri şikâyet takibi. |
| **Production** | | | | | |
| `ProductionWorkOrderCreated` | Domain | Production | İş emri açıldığında | Logistics, AI | Hammadde hazırlığı. |
| `ProductionStarted` | Domain | Production | Üretim başladığında | Analytics | Üretim bandı izleme. |
| `ProductionCompleted` | Integration | Production | Üretim tamamlandığında | Logistics, QC | Kalite kontrol tetiklemesi. |
| **CEO / Karar Defteri** | | | | | |
| `DecisionLogCreated` | Domain | CEO | Yeni karar/strateji kaydı girildiğinde | AI, Workflow | Stratejik analiz. |
| `DecisionLogApproved` | Integration | CEO | Karar onaylandığında | All Contexts | Şirket içi tebliğ. |
| **System & Security** | | | | | |
| `UserLoggedIn` | Domain | Security | Kullanıcı sisteme girdiğinde | Observability, Audit | Güvenlik günlüğü. |
| `PasswordChanged` | Domain | Security | Şifre değiştiğinde | Notification, Audit | Güvenlik uyarısı. |
| `TenantCreated` | Integration | Tenant | Yeni kiracı oluşturulduğunda | All Contexts | Veritabanı ve tenant şeması hazırlama. |
| `RoleAssigned` | Domain | Security | Yetki rolü tanımlandığında | Audit | Erişim günlüğü. |
| `ApiKeyCreated` | Integration | Security | API anahtarı üretildiğinde | Audit | Entegrasyon izni takibi. |

---

# Event Subscribers

Bir Event'i birden fazla modül dinleyebilir.

Örnek

```text
ProposalApproved

↓

Sales

↓

Finance

↓

Notification

↓

AI Copilot

↓

Analytics
```

---

# AI Event Kullanımı

AI Agent'lar Event'leri dinleyebilir.

Örnek

```text
SalesOrderCreated

↓

AI Forecast

↓

Demand Prediction

↓

Purchase Recommendation
```

AI hiçbir zaman Event üreticisinin yerine geçmez.

---

# Event Güvenliği

Her Event aşağıdaki bilgileri taşır.

* TenantId
* CorrelationId
* UserId
* TraceId

Tüm Event'ler Audit Log'a yazılır.

---

# Desteklenen Teknolojiler

Mimari aşağıdaki altyapılarla uyumludur.

* Kafka
* RabbitMQ
* Azure Service Bus
* AWS SQS/SNS
* NATS
* Redis Streams

Başlangıçta In-Memory Event Bus kullanılabilir.

Kurumsal dağıtımlarda Message Broker kullanılmalıdır.

---

# Event Monitoring

Her Event için aşağıdaki bilgiler izlenir.

* Yayınlanma zamanı
* İşlenme süresi
* Başarı durumu
* Retry sayısı
* Subscriber sayısı
* Hata mesajı

---

# Temel İlke

Business Logic hiçbir zaman başka bir modülü doğrudan çağırmaz.

Modüller yalnızca:

* Domain Events
* Integration Events
* Event Bus

üzerinden haberleşir.

Bu yapı, Emare BOS'un ölçeklenebilir, dağıtık ve AI destekli mimarisinin temelini oluşturur.
