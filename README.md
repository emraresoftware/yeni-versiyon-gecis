# 🏛️ Emare Business Operating System (BOS) Mimarisi

**Title:** Emare Business Operating System (BOS) Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** Yok
**Related Documents:** MASTER_ARCHITECTURE_INDEX.md, DOMAIN_MODEL.md, BOUNDED_CONTEXTS.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Emare Business Operating System (BOS), klasik ERP yaklaşımının ötesine geçerek; şirketin tüm süreçlerini, verilerini, kullanıcılarını, yapay zekâ ajanlarını ve entegrasyonlarını tek platform üzerinde yöneten kurumsal işletim sistemi mimarisidir.

Bu mimari SAP, Oracle, Microsoft Dynamics, IFS ve Odoo gibi sistemlerden edinilen deneyimlerin üzerine; Event Driven Architecture, AI Native Design ve Business Engine yaklaşımı eklenerek tasarlanmıştır.

---

# Mimari Katmanları

```text
                    Kullanıcılar
                         │
────────────────────────────────────────────
                Web / Mobile / API
────────────────────────────────────────────
                     AI Copilot
────────────────────────────────────────────
               Business Applications
────────────────────────────────────────────
                 Business Engines
────────────────────────────────────────────
              Workflow • Event Bus
────────────────────────────────────────────
                Common Services
────────────────────────────────────────────
               BOS Kernel Platform
────────────────────────────────────────────
 Database • Cache • Queue • Storage • Search
────────────────────────────────────────────
```

---

# Katman 1 — BOS Kernel

Bu katman sistemin işletim sistemidir.

## İçerik

* Authentication
* Authorization (RBAC + ABAC)
* Tenant Management
* User Management
* Role Management
* Permission Engine
* Audit Log
* Configuration
* Localization
* Feature Flags
* License Management

Kernel hiçbir iş modülüne bağımlı değildir.

---

# Katman 2 — Common Services

Tüm sistem tarafından ortak kullanılan servisler.

## Servisler

* Notification Service
* Email Service
* SMS Service
* WhatsApp Service
* Telegram Service
* File Storage
* OCR
* Barcode
* QR
* Currency Service
* Exchange Rate Service
* PDF Service
* Report Service
* Search Service
* Number Generator
* Digital Signature

---

# Katman 3 — Workflow & Automation

İş süreçlerini yöneten katmandır.

## İçerik

* Workflow Engine
* BPMN
* Rule Engine
* Approval Engine
* Escalation Engine
* Scheduler
* Background Jobs
* Retry Queue
* Dead Letter Queue

Tüm modüller aynı Workflow Engine'i kullanır.

---

# Katman 4 — Event Bus

Sistem Event Driven Architecture kullanır.

Her işlem Event üretir.

Örnek:

```text
SalesOrderCreated

↓

ReserveStock

↓

ShipmentCreated

↓

InvoiceCreated

↓

AccountingPosted

↓

CustomerNotified
```

Modüller birbirini doğrudan çağırmaz.

---

# Katman 5 — Business Engines

İş kuralları burada bulunur.

## CRM Engine

* Customer
* Contact
* Opportunity
* Proposal
* Activity
* Campaign

---

## Sales Engine

* Sales Order
* Price Lists
* Discount Rules
* Contract
* Dealer

---

## Procurement Engine

* Purchase Request
* RFQ
* Purchase Order
* Supplier Evaluation

---

## Inventory Engine

* Warehouse
* Stock
* Reservation
* Lot
* Serial
* Barcode
* RFID

---

## Production Engine

* BOM
* Routing
* Work Order
* Capacity Planning
* MRP
* MES
* OEE

---

## Finance Engine

* General Ledger
* Journal Entry
* Cash
* Bank
* Budget
* Fixed Assets
* Tax
* Cost Accounting

---

## HR Engine

* Employee
* Leave
* Payroll
* Performance
* Recruitment
* Training

---

## Service Engine

* Service Requests
* Warranty
* Maintenance
* Field Service

---

## Project Engine

* Projects
* Tasks
* Resources
* Timesheets
* Budget

---

## Quality Engine

* QC Standards
* QC Tests
* Claims
* CAPA
* Non-Conformance

---

# Katman 6 — Business Applications

Bu katman kullanıcı ekranlarını içerir.

Örnek:

* CRM
* Finance
* HR
* Production
* Logistics
* CEO Dashboard
* AI Dashboard

Bu katmanda iş kuralı bulunmaz.

---

# Katman 7 — AI Platform

Sistemin tüm yapay zekâ bileşenleri.

## AI Copilot

Doğal dil ile ERP kullanımı.

Örnek:

> "Son 30 gündeki en büyük müşterilerimi göster."

---

## AI Analytics

* Tahminleme
* Anomali tespiti
* Trend analizi
* KPI açıklamaları

---

## AI Vision

* OCR
* Barkod
* QR
* Görsel kalite kontrol
* Belge analizi

---

## AI Agent Platform

Departman bazlı otonom ajanlar.

* CEO Agent
* Sales Agent
* Finance Agent
* HR Agent
* Production Agent
* QC Agent
* Logistics Agent

Her ajan yalnızca yetkili olduğu modüllerde işlem yapabilir.

---

# Katman 8 — Integration Platform

Dış sistem entegrasyonları.

## Desteklenen Protokoller

* REST API
* GraphQL
* Webhook
* gRPC
* MQTT
* Kafka
* RabbitMQ

## Hazır Entegrasyonlar

* e-Fatura
* e-Arşiv
* e-İrsaliye
* Bankalar
* Kargo Firmaları
* Pazaryerleri
* ERP Aktarım Servisleri

---

# Katman 9 — Marketplace

Platform genişletilebilir yapıdadır.

Marketplace üzerinden;

* Plugin
* Tema
* Widget
* Connector
* AI Agent
* Rapor

yüklenebilir.

Çekirdek sistem değiştirilmeden yeni özellik eklenebilir.

---

# Çok Kiracılı (Multi-Tenant) Yapı

Sistem tamamen Multi-Tenant olarak tasarlanmıştır.

Her kayıt;

* TenantId
* Audit bilgileri
* Yetki kontrolleri

ile korunur.

Tenant izolasyonu zorunludur.

---

# Güvenlik

Desteklenen güvenlik mekanizmaları:

* RBAC
* ABAC
* MFA
* Audit Log
* API Key
* OAuth2
* OpenID Connect
* JWT
* Row Level Security
* Column Level Security

---

# Temel Mimari İlkeleri

* Business Logic yalnızca Engine katmanında bulunur.
* Controller hiçbir iş kuralı içermez.
* UI yalnızca servis çağırır.
* Modüller Event Bus üzerinden haberleşir.
* AI doğrudan veritabanına yazmaz.
* Her işlem Audit Log üretir.
* Her modül Tenant izolasyonuna uyar.
* Tüm zaman bilgileri UTC olarak saklanır.
* Tüm servisler asenkron çalışır.

---

# Nihai Vizyon

Emare BOS yalnızca bir ERP değildir.

Amaç;

* süreç yöneten,
* karar destek sağlayan,
* yapay zekâ ile çalışan,
* olay tabanlı mimariye sahip,
* genişletilebilir,
* çok kiracılı,
* kurumsal ölçeklenebilir

bir **Business Operating System** oluşturmaktır.

Bu doküman, sistemin tüm teknik ve iş mimarisinin temel referansıdır. Kod geliştiren tüm ajanlar bu mimariye uygun hareket etmekle yükümlüdür.
