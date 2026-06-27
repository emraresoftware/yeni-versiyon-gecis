# 📘 Ubiquitous Language

**Title:** Ubiquitous Language
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** DOMAIN_MODEL.md
**Related Documents:** BOUNDED_CONTEXTS.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Bu doküman Emare Business Operating System (BOS) içerisinde kullanılan ortak iş ve teknik terimleri tanımlar.

Amaç; geliştiricilerin, AI ajanlarının, yöneticilerin ve kullanıcıların aynı kavramları aynı anlamda kullanmasını sağlamaktır.

---

# Genel İlke

Her kavram tek bir anlam taşımalıdır.

Aynı kavram için farklı isimler kullanılmamalıdır.

Örnek:

```text
Doğru: CrmAccount

Yanlış: Customer, Cari, Client, Account karışık kullanımı
```

Kodda teknik isim İngilizce olabilir.

Arayüzde Türkçe karşılık gösterilebilir.

---

# Temel Kavramlar

## Tenant

Sistemi kullanan bağımsız şirket veya organizasyon.

Her veri bir Tenant'a aittir.

---

## User

Sisteme giriş yapan kişi.

---

## Role

Kullanıcının sistem içindeki görevi.

Örnek:

* CEO
* Sales Manager
* Finance Manager
* HR Manager
* Warehouse Manager

---

## Permission

Kullanıcının yapabileceği işlem.

Örnek:

* CRM.Read
* CRM.Write
* Finance.PostJournal
* HR.ApproveLeave

---

## Audit

Sistemde yapılan işlemlerin değiştirilemez kayıt geçmişi.

---

# CRM Kavramları

## CrmAccount

Müşteri, tedarikçi, partner veya rakip gibi ticari ilişki kurulan ana cari varlık.

Arayüz adı:

```text
Cari / Müşteri
```

Kod adı:

```text
CrmAccount
```

---

## CrmContact

CrmAccount altında yer alan ilgili kişi.

Örnek:

* Satın alma sorumlusu
* Finans yetkilisi
* Operasyon yetkilisi

---

## CrmOpportunity

Potansiyel satış fırsatı.

Henüz kesinleşmiş sipariş değildir.

---

## CrmProposal

Müşteriye sunulan teklif.

---

## CrmProposalItem

Teklif içerisindeki ürün/hizmet kalemi.

---

# Sales Kavramları

## Sales Order

Onaylanmış satış siparişi.

Tekliften doğabilir.

---

## Price List

Ürün veya hizmet fiyatlarının tanımlandığı liste.

---

## Discount

İndirim.

Kurallı veya manuel olabilir.

---

# Finance Kavramları

## FinanceAccountPlan

Tek düzen hesap planı.

---

## FinanceJournalEntry

Yevmiye fişi.

Muhasebe kayıt başlığıdır.

---

## FinanceJournalEntryLine

Yevmiye fişi satırı.

Borç veya alacak tutarı içerir.

---

## Debit

Borç.

---

## Credit

Alacak.

---

## Posted

Muhasebe fişinin deftere işlenmiş olması.

Posted olan kayıt değiştirilemez.

---

# HR Kavramları

## HrEmployee

Personel kartı.

---

## HrLeaveType

İzin tipi.

Örnek:

* Yıllık izin
* Raporlu
* Ücretsiz izin

---

## HrLeave

İzin talebi.

---

## AnnualLeaveBalance

Çalışanın kalan yıllık izin hakkı.

---

# Logistics Kavramları

## LogisticsWarehouse

Depo.

---

## LogisticsStockMovement

Stok hareketi.

Giriş veya çıkış hareketidir.

---

## LogisticsStockTransfer

Depolar arası transfer talebi.

---

## LogisticsStockTransferLine

Transfer içindeki ürün kalemi.

---

## SourceWarehouse

Transferin çıkış deposu.

---

## TargetWarehouse

Transferin varış deposu.

---

# QC Kavramları

## QcStandard

Ürün kalite standardı.

---

## QcTestResult

Üretim veya ürün kalite test sonucu.

---

## QcClaim

Müşteri kalite şikayeti veya iade talebi.

---

## FailedQuantity

Testten geçemeyen miktar.

---

## TestedQuantity

Test edilen toplam miktar.

---

# CEO Kavramları

## DecisionLog

Yönetici karar defteri.

Stratejik kararların, etkilerinin ve durumlarının tutulduğu kayıt.

---

## Impact

Kararın etki seviyesi.

Değerler:

* High
* Medium
* Low

---

## Status

Kararın durumu.

Örnek:

* Draft
* Approved
* Implemented
* Cancelled

---

# Platform Kavramları

## Business Engine

İş kurallarını çalıştıran motor.

Örnek:

* Finance Engine
* CRM Engine
* HR Engine

---

## Business Module

Kullanıcıya görünen modül veya ekranlar.

Örnek:

* CRM ekranı
* Finans ekranı
* Depo ekranı

---

## Workflow Engine

Süreçleri, onayları ve görev akışlarını yöneten motor.

---

## Rule Engine

Koşullu iş kurallarını değerlendiren motor.

---

## Event Bus

Modüller arası olay tabanlı haberleşme katmanı.

---

## Metadata Engine

Ekran, form, alan, rapor ve workflow tanımlarını metadata üzerinden yöneten motor.

---

## AI Engine

Yapay zekâ servislerini, ajanları ve Copilot özelliklerini yöneten motor.

---

## Notification Engine

E-posta, SMS, WhatsApp, Push ve uygulama içi bildirimleri yöneten motor.

---

## Integration Engine

Dış sistem bağlantılarını yöneten motor.

---

## Analytics Engine

Raporlama, KPI ve iş zekâsı analizlerini yöneten motor.

---

# Teknik Kavramlar

## Aggregate Root

Domain içerisindeki ana tutarlılık sınırı.

Örnek:

* CrmAccount
* FinanceJournalEntry
* LogisticsStockTransfer

---

## Entity

Kimliği olan domain nesnesi.

---

## Value Object

Kimliği olmayan, değeriyle anlam kazanan nesne.

Örnek:

* Money
* Address
* DateRange

---

## Domain Event

Domain içinde gerçekleşen önemli olay.

Örnek:

* CrmProposalApproved
* FinanceJournalEntryPosted
* HrLeaveApproved

---

## DTO

API üzerinden veri taşımak için kullanılan nesne.

Entity doğrudan dışarı açılmaz.

---

## Result Pattern

Metotların başarı/başarısızlık sonucunu standart şekilde döndürmesini sağlayan yapı.

---

## ApiResponse

API cevaplarının ortak sarmalayıcı formatı.

---

# İsimlendirme Kuralları

## Entity

PascalCase kullanılır.

```text
CrmAccount
FinanceJournalEntry
LogisticsWarehouse
```

---

## API Route

Kebab-case kullanılır.

```text
/api/control-tower/crm/accounts
/api/control-tower/finance/entries
```

---

## Event

Entity + Action formatı kullanılır.

```text
CrmAccountCreated
ProposalApproved
JournalEntryPosted
```

---

## Permission

Module.Action formatı kullanılır.

```text
CRM.Read
CRM.Write
Finance.PostJournal
HR.ApproveLeave
```

---

# Yasaklı Karışımlar

Aynı kavram için karışık kullanım yapılmaz.

```text
Customer / Client / Cari / Account
```

yerine:

```text
CrmAccount
```

kullanılır.

```text
Warehouse / Depot / Depo
```

yerine:

```text
LogisticsWarehouse
```

kullanılır.

```text
Journal / Voucher / Fiş
```

yerine:

```text
FinanceJournalEntry
```

kullanılır.

---

# Nihai İlke

Bu doküman, Emare BOS'un ortak dil sözlüğüdür.

Kod, doküman, API, UI ve AI Agent görevlerinde aynı kavramlar aynı anlamda kullanılmalıdır.

Ortak dil bozulursa mimari bütünlük bozulur.
