# 🗺️ ERD Model

## Amaç

Bu doküman Emare Business Operating System (BOS) içerisindeki temel ERP/CRM modüllerinin veritabanı ilişki modelini tanımlar.

Amaç; kodlamaya başlamadan önce tabloların, anahtarların, ilişkilerin ve modül sınırlarının netleştirilmesidir.

---

# Genel İlkeler

Tüm ana tablolar aşağıdaki ortak alanları taşımalıdır:

```text
Id
TenantId
CreatedAt
UpdatedAt
CreatedBy
UpdatedBy
IsDeleted
RowVersion
```

Tüm tarih alanları UTC olmalıdır.

---

# CRM ERD

```text
CrmAccount
 ├── CrmContact
 ├── CrmOpportunity
 └── CrmProposal
        └── CrmProposalItem
```

## İlişkiler

* `CrmAccount 1-N CrmContact`
* `CrmAccount 1-N CrmOpportunity`
* `CrmAccount 1-N CrmProposal`
* `CrmProposal 1-N CrmProposalItem`

---

# Finance ERD

```text
FinanceAccountPlan

FinanceJournalEntry
 └── FinanceJournalEntryLine
```

## İlişkiler

* `FinanceJournalEntry 1-N FinanceJournalEntryLine`
* `FinanceJournalEntryLine.AccountCode` → `FinanceAccountPlan.Code`

## Kritik Kural

Yevmiye fişi için:

```text
SUM(Debit) = SUM(Credit)
```

olmak zorundadır.

---

# HR ERD

```text
HrEmployee
 └── HrLeave

HrLeaveType
 └── HrLeave
```

## İlişkiler

* `HrEmployee 1-N HrLeave`
* `HrLeaveType 1-N HrLeave`

## Kritik Kural

İzin onaylandığında:

```text
HrEmployee.AnnualLeaveBalance -= HrLeave.Days
```

---

# Logistics ERD

```text
LogisticsWarehouse
 ├── LogisticsStockMovement
 ├── LogisticsStockTransfer as SourceWarehouse
 └── LogisticsStockTransfer as TargetWarehouse

LogisticsStockTransfer
 └── LogisticsStockTransferLine
```

## İlişkiler

* `LogisticsWarehouse 1-N LogisticsStockMovement`
* `LogisticsWarehouse 1-N LogisticsStockTransfer.SourceWarehouseId`
* `LogisticsWarehouse 1-N LogisticsStockTransfer.TargetWarehouseId`
* `LogisticsStockTransfer 1-N LogisticsStockTransferLine`

## Kritik Kural

Transfer tamamlandığında:

```text
Source Warehouse → Out Movement
Target Warehouse → In Movement
```

oluşturulur.

---

# QC ERD

```text
QcStandard

QcTestResult

QcClaim
 └── CrmAccount
```

## İlişkiler

* `QcClaim N-1 CrmAccount`
* `QcStandard.ProductCode` ürün koduna referans verir.
* `QcTestResult.ProductCode` ürün koduna referans verir.

## Kritik Kural

```text
FailedQuantity <= TestedQuantity
```

olmalıdır.

---

# CEO ERD

```text
DecisionLog
```

Bağımsız yönetici karar defteri tablosudur.

İleride diğer modüllerden KPI ve event okuyabilir.

---

# Modüller Arası İlişkiler

```text
CrmAccount
   ↓
QcClaim

CrmAccount
   ↓
CrmProposal
   ↓
FinanceJournalEntry

LogisticsWarehouse
   ↓
LogisticsStockMovement
   ↓
Finance

Production Batch
   ↓
QcTestResult
```

---

# Foreign Key İlkeleri

* Aynı bounded context içindeki ilişkilerde FK kullanılabilir.
* Modüller arası ilişkilerde doğrudan FK dikkatli kullanılmalıdır.
* Kritik entegrasyonlar Event Bus veya Application Service üzerinden yapılmalıdır.
* Multi-tenant uyumluluk için FK ilişkilerinde `TenantId` kontrolü zorunludur.

---

# Index Önerileri

## Genel

```text
TenantId
TenantId + IsDeleted
TenantId + CreatedAt
```

## CRM

```text
TenantId + Code
TenantId + Name
TenantId + TaxNumber
```

## Finance

```text
TenantId + EntryNo
TenantId + Date
TenantId + IsPosted
```

## Logistics

```text
TenantId + WarehouseId
TenantId + ProductCode
TenantId + ReferenceNo
```

## QC

```text
TenantId + ProductCode
TenantId + BatchNumber
TenantId + Status
```

---

# Silme Stratejisi

Ana kayıtlar fiziksel silinmez.

```text
IsDeleted = true
```

Detay satırları için karar aggregate seviyesinde verilir.

Örneğin:

* Teklif silinirse teklif kalemleri de soft delete olabilir.
* Yevmiye fişi post edilmişse silinemez.
* Stok hareketi oluşmuşsa silinemez.

---

# Concurrency Stratejisi

Aşağıdaki tablolarda optimistic concurrency önerilir:

* CrmProposal
* FinanceJournalEntry
* HrLeave
* LogisticsStockTransfer
* QcClaim
* DecisionLog

---

# Kodlama Öncesi Kontrol

Her ajan entity oluşturmadan önce şunları kontrol etmelidir:

* Tablo hangi bounded context'e ait?
* Aggregate root doğru mu?
* TenantId var mı?
* UTC DateTime alanları doğru mu?
* FK ilişkisi gerçekten gerekli mi?
* Index ihtiyacı var mı?
* Soft delete uygulanacak mı?
* Concurrency gerekli mi?

---

# Nihai İlke

ERD modeli, veritabanı şemasının teknik temelidir.

Kodlama başlamadan önce tüm entity ilişkileri bu dokümana göre doğrulanmalıdır.
