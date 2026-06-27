# 🧩 Metadata Engine Mimarisi

**Title:** Metadata Engine Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** RULE_ENGINE.md
**Related Documents:** EVENT_BUS.md, WORKFLOW_ENGINE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Metadata Engine, Emare Business Operating System (BOS) içerisinde ekranların, formların, alanların, doğrulamaların, iş akışlarının ve raporların kod yazılmadan tanımlanmasını sağlayan çekirdek platform bileşenidir.

Bu yapı sayesinde sistem **configurable** ve **extensible** hale gelir.

---

# Temel Prensip

Kod yalnızca altyapıyı oluşturur.

İş uygulamaları ise metadata ile tanımlanır.

```text
Metadata

↓

Form

↓

Validation

↓

Workflow

↓

UI

↓

API

↓

Business Engine
```

---

# Metadata Türleri

## Entity Metadata

Bir iş nesnesinin tanımı.

Örnek:

* Customer
* Product
* Warehouse
* Employee
* JournalEntry

Her Entity;

* Name
* DisplayName
* Description
* Module
* Version

bilgilerini taşır.

---

## Field Metadata

Her alan metadata olarak tanımlanır.

Örnek

```text
Field Name

Display Name

Data Type

Required

Default Value

Nullable

Length

Precision

Scale

Visibility

ReadOnly
```

---

## Relationship Metadata

İlişkiler metadata ile tanımlanır.

Desteklenen tipler

* One To One
* One To Many
* Many To Many
```

---

## Validation Metadata

Örnek

```text
Required

Min

Max

Regex

Unique

Email

Phone

Tax Number

Identity Number
```

Kod içerisine validation yazılmaz.

---

## Form Metadata

Formlar aşağıdaki bileşenlerden oluşur.

* Tabs
* Sections
* Groups
* Fields
* Buttons
* Actions

---

## View Metadata

Desteklenen görünüm tipleri

* Table
* Card
* Kanban
* Tree
* Calendar
* Timeline
* Dashboard
* Pivot

---

## Dashboard Metadata

Dashboard tamamen metadata ile oluşturulur.

Widget tipleri

* KPI
* Chart
* Table
* Gauge
* Progress
* Heatmap
* Map

---

## Workflow Metadata

Workflow Engine süreçlerini metadata üzerinden okur.

Her Workflow;

* Trigger
* Conditions
* Steps
* SLA
* Escalation

bilgilerini içerir.

---

## API Metadata

Her servis metadata içerir.

* Route
* Version
* Permission
* Request
* Response

---

## Report Metadata

Raporlar metadata ile oluşturulur.

Desteklenen çıktılar

* PDF
* Excel
* CSV
* JSON

---

# Dynamic UI

Frontend metadata okur.

Kendi ekranını üretir.

Örnek

```text
Customer Entity

↓

Metadata

↓

React Components

↓

Çalışan Form
```

Yeni ekran geliştirmek için React kodu yazılması gerekmez.

---

# Dynamic API

API metadata okuyabilir.

Örnek

```text
Entity

↓

Metadata

↓

CRUD API
```

Standart CRUD işlemleri otomatik üretilebilir.

---

# Metadata Versioning

Her metadata versiyon taşır.

```text
Customer v1

↓

Customer v2

↓

Customer v3
```

Eski ekranlar çalışmaya devam eder.

---

# Tenant Bazlı Özelleştirme

Her Tenant kendi metadata'sını kullanabilir.

Örnek

Tenant A

↓

Customer Form

15 Alan

Tenant B

↓

Customer Form

22 Alan

Kod değişmez.

---

# Localization

Metadata çok dilli çalışır.

Örnek

```text
Customer

↓

Müşteri

↓

Kunde

↓

Customer
```

---

# Feature Flags

Metadata üzerinden özellik açılıp kapatilebilir.

Örnek

```text
Subscription Module

↓

Enabled

Tenant A

Disabled

Tenant B
```

---

# Audit

Metadata değişiklikleri kayıt altına alınır.

Kaydedilen bilgiler

* Kim değiştirdi
* Ne değişti
* Eski değer
* Yeni değer
* Tarih
* Versiyon

---

# Performans

Metadata;

* Cache'lenebilir olmalıdır.
* Değiştiğinde cache yenilenmelidir.
* Sık okunan tanımlar bellekte tutulmalıdır.

---

# Güvenlik

Metadata değişiklikleri yalnızca yetkili kullanıcılar tarafından yapılabilir.

Her değişiklik:

* Audit Log
* Tenant kontrolü
* Yetki kontrolü

ile korunmalıdır.

---

# Temel Mimari İlkeleri

* İş kuralları Business Engine'de kalır.
* Metadata yalnızca tanım içerir.
* UI metadata'dan üretilebilir.
* API metadata'dan üretilebilir.
* Workflow metadata'dan okunabilir.
* Raporlar metadata ile oluşturulabilir.
* Metadata versiyonlanır.
* Metadata tenant bazında özelleştirilebilir.

---

# Nihai Vizyon

Metadata Engine sayesinde Emare BOS;

* yeni modülleri,
* yeni ekranları,
* yeni alanları,
* yeni formları,
* yeni raporları,
* yeni iş akışlarını

minimum kod değişikliği ile oluşturabilen, kurumsal ölçekte genişletilebilir bir platform haline gelir.

Bu yaklaşım Emare BOS'u klasik ERP uygulamalarından ayıran en önemli mimari bileşenlerden biridir.
