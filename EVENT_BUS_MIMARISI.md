# ⚡ Event Bus Mimarisi

**Title:** Event Bus Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** README.md
**Related Documents:** WORKFLOW_ENGINE_MIMARISI.md, RULE_ENGINE.md

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
CustomerCreated

ProposalApproved

JournalPosted

StockReserved

LeaveApproved

TransferCompleted
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
CustomerCreated

CustomerUpdated

CustomerDeleted

ProposalSent

ProposalApproved

PurchaseApproved

StockTransferred

JournalPosted

EmployeeCreated

LeaveApproved

QcTestCompleted

ShipmentDelivered
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

## CRM

* CustomerCreated
* CustomerUpdated
* OpportunityCreated
* ProposalSent

---

## Sales

* OrderCreated
* OrderApproved
* OrderCancelled

---

## Purchasing

* PurchaseRequested
* PurchaseApproved
* PurchaseCompleted

---

## Warehouse

* StockReserved
* StockReleased
* StockTransferred

---

## Production

* WorkOrderCreated
* ProductionStarted
* ProductionCompleted

---

## QC

* TestStarted
* TestCompleted
* ClaimCreated

---

## HR

* EmployeeCreated
* LeaveApproved

---

## Finance

* JournalPosted
* PaymentReceived
* InvoiceCreated

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
