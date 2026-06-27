# 🧩 Bounded Contexts

**Title:** Bounded Contexts
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** DOMAIN_MODEL.md
**Related Documents:** UBIQUITOUS_LANGUAGE.md, EVENT_BUS.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Bu doküman Emare Business Operating System (BOS) içerisindeki Domain Driven Design (DDD) bounded context yapılarını tanımlar.

Her Business Engine kendi bounded context'i içerisinde çalışır.

Hiçbir bounded context başka bir bounded context'in iç modeline doğrudan bağımlı olamaz.

---

# Temel Prensip

```text id="ddd001"
Kernel

↓

Shared Kernel

↓

Business Contexts

↓

Integration Events

↓

Other Contexts
```

Context'ler yalnızca sözleşmeler (Contracts), Domain Events veya Application Services üzerinden haberleşir.

---

# Context Haritası

```text id="ddd002"
CRM

↓

Sales

↓

Finance

CRM

↓

Service

Warehouse

↓

Production

↓

QC

↓

Analytics

HR

↓

Payroll

↓

Finance
```

---

# Shared Kernel

Aşağıdaki yapılar ortak kullanılabilir.

* Tenant
* User
* Role
* Permission
* Money
* Address
* DateRange
* Result Pattern
* Audit
* Notification Contracts
* Event Contracts

Business Entity'ler Shared Kernel içine konulamaz.

---

# CRM Context

## Aggregate Root

* CrmAccount

## Entity

* CrmContact
* CrmOpportunity
* CrmProposal
* CrmProposalItem

## Domain Events

* CrmAccountCreated
* OpportunityCreated
* ProposalApproved

CRM başka context'in tablolarına yazamaz.

---

# Sales Context

Sorumluluk

* Teklif
* Sipariş
* Fiyat
* Kampanya

Bağımlı olduğu context

CRM

Çıktıları

Finance

Warehouse

Analytics

---

# Procurement Context

Sorumluluk

* Satın Alma
* RFQ
* Supplier Evaluation

Çıktıları

Warehouse

Finance

Production

---

# Warehouse Context

Sorumluluk

* Depo
* Lot
* Seri
* Stok

Warehouse yalnızca stoktan sorumludur.

Muhasebe yapmaz.

---

# Production Context

Sorumluluk

* BOM
* Routing
* MRP
* MES
* Work Order

Üretim muhasebe kaydı oluşturmaz.

Sadece Event yayınlar.

---

# Finance Context

Sorumluluk

* General Ledger
* Cash
* Bank
* Budget
* Tax
* Fixed Assets

Finance başka context'in verisini değiştiremez.

Yalnızca muhasebeleştirir.

---

# HR Context

Sorumluluk

* Employee
* Leave
* Payroll
* Recruitment

HR stok yönetmez.

---

# QC Context

Sorumluluk

* Standard
* Test
* Claim
* CAPA

QC üretim planlamaz.

---

# Service Context

Sorumluluk

* Warranty
* Maintenance
* Field Service

---

# Analytics Context

Sorumluluk

* KPI
* Dashboard
* Forecast
* BI

Analytics hiçbir veriyi değiştirmez.

---

# AI Context

Sorumluluk

* Copilot
* Agents
* Vision
* Analytics
* RAG

AI doğrudan Aggregate değiştirmez.

---

# Integration Context

Sorumluluk

* API
* Connector
* Webhook
* Queue

Integration Engine iş kuralı içermez.

---

# Notification Context

Sorumluluk

* Email
* SMS
* Push
* WhatsApp
* Telegram

Notification Engine yalnızca mesaj teslim eder.

---

# Workflow Context

Sorumluluk

* Approval
* SLA
* Escalation
* Task

Workflow iş verisini değiştirmez.

---

# Rule Context

Sorumluluk

* Validation
* Business Rule
* Calculation

Rule Engine yalnızca karar üretir.

---

# Metadata Context

Sorumluluk

* Dynamic Form
* Dynamic Screen
* Dynamic Report
* Dynamic Workflow

---

# Context Haberleşmesi

Context'ler aşağıdaki yollarla haberleşebilir.

* Domain Event
* Integration Event
* REST API
* Application Service
* Workflow
* Event Bus

Doğrudan DbContext paylaşımı yasaktır.

---

# Yasaklar

Aşağıdaki işlemler yasaktır.

❌ Finance Repository → Warehouse DbContext

❌ QC Repository → CRM DbContext

❌ HR → Finance Entity

❌ UI → Entity

❌ Controller → DbContext

❌ AI → Database

---

# Ownership

Her tablo yalnızca tek bir bounded context'e aittir.

Örnek

```text id="ddd003"
FinanceJournalEntry

↓

Finance Context
```

Warehouse bu tabloyu güncelleyemez.

---

# Transaction Sınırı

Transaction yalnızca aynı bounded context içerisinde tutulmalıdır.

Context'ler arası işlem gerekiyorsa:

* Domain Event
* Saga
* Process Manager
* Workflow

kullanılmalıdır.

---

# Anti-Corruption Layer (ACL)

Dış sistemlerden gelen veriler doğrudan domain modeline yazılmaz.

Önce ACL katmanında dönüştürülür.

Örnek

```text id="ddd004"
SAP

↓

ACL

↓

Finance Context
```

---

# Temel Mimari İlkeleri

* Her context kendi verisinin sahibidir.
* Context sınırları ihlal edilemez.
* Modüller yalnızca sözleşmeler üzerinden konuşur.
* Event Bus varsayılan haberleşme yöntemidir.
* Aggregate sınırları korunmalıdır.
* Shared Kernel minimum tutulmalıdır.

---

# Nihai Vizyon

Bounded Context yaklaşımı sayesinde Emare BOS;

* modüler,
* bağımsız geliştirilebilir,
* yüksek ölçeklenebilir,
* bakım maliyeti düşük,
* mikroservis dönüşümüne hazır

kurumsal bir Business Operating System mimarisine sahip olur.

Bu doküman tüm Domain Model tasarımının sınırlarını tanımlar.
