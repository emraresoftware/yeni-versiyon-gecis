# 🧬 Domain Model

**Title:** Domain Model Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** BOUNDED_CONTEXTS.md
**Related Documents:** ERD_MODEL.md, UBIQUITOUS_LANGUAGE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Bu doküman Emare Business Operating System (BOS) içerisindeki temel domain modelini, modül sınırlarını, aggregate yapılarını ve entity ilişkilerini tanımlar.

Kodlamaya başlamadan önce tüm ajanlar bu dokümanı okumalıdır.

---

# Temel Yaklaşım

Emare BOS aşağıdaki domain prensiplerini kullanır:

* Domain Driven Design
* Clean Architecture
* Multi-Tenant Model
* Event Driven Architecture
* Audit First Design
* Metadata Driven Extension

---

# Ortak Entity Kuralları

Her ana entity aşağıdaki alanları taşımalıdır:

```csharp
Guid Id
Guid TenantId
DateTime CreatedAt
DateTime? UpdatedAt
Guid? CreatedBy
Guid? UpdatedBy
bool IsDeleted
byte[] RowVersion
```

Tüm DateTime alanları UTC olmalıdır.

---

# Ana Domain Alanları

## CRM Domain

Aggregate Root:

* CrmAccount

Alt Entity:

* CrmContact
* CrmOpportunity
* CrmProposal
* CrmProposalItem

Domain Event:

* CrmAccountCreated
* OpportunityCreated
* ProposalCreated
* ProposalApproved

---

## Finance Domain

Aggregate Root:

* FinanceJournalEntry
* FinanceAccountPlan

Alt Entity:

* FinanceJournalEntryLine

Domain Event:

* JournalEntryCreated
* JournalEntryPosted
* AccountPlanCreated

Kural:

Borç toplamı ve alacak toplamı eşit değilse fiş post edilemez.

---

## HR Domain

Aggregate Root:

* HrEmployee
* HrLeave

Alt Entity:

* HrLeaveType

Domain Event:

* EmployeeCreated
* LeaveRequested
* LeaveApproved
* LeaveRejected

Kural:

İzin onaylandığında bakiye düşürülür.

---

## Logistics Domain

Aggregate Root:

* LogisticsWarehouse
* LogisticsStockTransfer

Alt Entity:

* LogisticsStockMovement
* LogisticsStockTransferLine

Domain Event:

* WarehouseCreated
* StockMovementCreated
* StockTransferRequested
* StockTransferApproved
* StockTransferCompleted

Kural:

Yetersiz stokta transfer tamamlanamaz.

---

## QC Domain

Aggregate Root:

* QcClaim
* QcTestResult
* QcStandard

Domain Event:

* QcTestCompleted
* QcClaimCreated
* QcClaimResolved

Kural:

FailedQuantity, TestedQuantity değerinden büyük olamaz.

---

## CEO Domain

Aggregate Root:

* DecisionLog

Domain Event:

* DecisionCreated
* DecisionApproved
* DecisionImplemented
* DecisionCancelled

---

# Modül Bağımlılıkları

```text
CRM
↓
Sales
↓
Finance

CRM
↓
QC

Warehouse
↓
Logistics
↓
Finance

Production
↓
QC
↓
Analytics
```

Hiçbir modül başka modülün tablosuna doğrudan yazamaz.

---

# Aggregate Kuralları

Her aggregate kendi tutarlılığından sorumludur.

Örnek:

FinanceJournalEntry aggregate'i:

* Line toplamlarını kontrol eder.
* Debit/Credit dengesini doğrular.
* Posted olduktan sonra değiştirilemez.

LogisticsStockTransfer aggregate'i:

* Pending başlar.
* Approved olur.
* Completed olduğunda stok hareketleri üretir.

---

# Value Object Önerileri

Aşağıdaki kavramlar Value Object olarak modellenebilir:

* Money
* Address
* PhoneNumber
* EmailAddress
* TaxNumber
* IdentityNumber
* DateRange
* Quantity
* Percentage

---

# Domain Event Standardı

Her domain event aşağıdaki alanları taşımalıdır:

```csharp
Guid EventId
Guid TenantId
Guid AggregateId
string AggregateType
DateTime OccurredAt
Guid? UserId
int Version
```

---

# Tenant İzolasyonu

Her aggregate TenantId taşır.

Her sorgu TenantId ile filtrelenmelidir.

Tenant filtresi olmayan repository veya query yazılamaz.

---

# Soft Delete

Ana entity'lerde fiziksel silme yerine soft delete kullanılmalıdır.

```csharp
IsDeleted = true
DeletedAt = DateTime.UtcNow
DeletedBy = currentUserId
```

---

# Concurrency

Kritik entity'lerde optimistic concurrency kullanılmalıdır.

Örnek:

* JournalEntry
* StockTransfer
* Leave
* Proposal
* DecisionLog

---

# Audit

Her create/update/delete işleminde audit kaydı oluşmalıdır.

Audit kayıtları değiştirilemez olmalıdır.

---

# Kodlama Öncesi Kontrol

Her ajan kodlamaya başlamadan önce şunları doğrulamalıdır:

* Aggregate root doğru mu?
* Entity başka modülün sorumluluğuna giriyor mu?
* Domain event gerekip gerekmediği?
* TenantId var mı?
* UTC DateTime kullanılıyor mu?
* Soft delete gerekli mi?
* Audit gerekli mi?
* Validation domain içinde mi, application içinde mi?

---

# Nihai İlke

Domain Model, Emare BOS'un iş gerçeğini temsil eder.

Kod, veritabanı ve arayüz bu modele uymalıdır.

Domain netleşmeden kodlama yapılmaz.
