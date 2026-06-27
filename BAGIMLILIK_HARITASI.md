# 🔗 Modül Bağımlılık Haritası (BAGIMLILIK_HARITASI.md)

Bu doküman, ERP/Business Operating System (BOS) içerisindeki tüm modüllerin birbirleriyle olan bağımlılıklarını tanımlar.

Amaç:

* Ajanların hangi modülü önce geliştireceğini belirlemek
* Döngüsel bağımlılıkları engellemek
* Kod tekrarını önlemek
* Modüller arası entegrasyonu standart hale getirmek

---

# Katmanlar

Sistem 6 katmandan oluşur.

```text
KERNEL

↓

COMMON SERVICES

↓

BUSINESS ENGINES

↓

BUSINESS MODULES

↓

AI ENGINES

↓

INTEGRATIONS
```

---

# 1. Kernel

Hiçbir modüle bağımlı değildir.

Tüm sistem bunun üzerine kurulur.

İçerik

* Authentication
* Authorization
* Tenant
* User
* Role
* Permission
* Audit Log
* Event Bus
* Workflow
* Notification
* Scheduler
* Configuration
* Localization

Bu katman tamamlanmadan hiçbir modül geliştirilmez.

---

# 2. Common Services

Bütün modüllerin ortak kullandığı servisler.

* File Service
* Email Service
* SMS Service
* WhatsApp Service
* OCR
* Barcode
* QR
* Currency
* Exchange Rate
* Number Generator
* PDF Generator
* Report Service

Bağımlılık

```text
Kernel

↓

Common Services
```

---

# 3. CRM

CRM ilk geliştirilecek iş modülüdür.

Bağımlılık

```text
Kernel

↓

Common

↓

CRM
```

CRM tarafından kullanılanlar

* User
* Tenant
* Notification

CRM'yi kullananlar

* Sales
* Finance
* QC
* Service
* Projects

---

# 4. Sales

Bağımlılık

```text
CRM

↓

Sales
```

Kullandıği Modüller

* CRM
* Products
* Price Lists
* Workflow

Sales'i kullananlar

* Finance
* Logistics
* Production

---

# 5. Product Management

Bağımlılık

```text
Kernel

↓

Product
```

Kullanan Modüller

* Sales
* Purchase
* Production
* QC
* Warehouse

---

# 6. Purchasing

Bağımlılık

```text
CRM

↓

Product

↓

Purchase
```

Satın alma tamamlandıktan sonra

↓

Warehouse

↓

Finance

↓

Production

tetiklenebilir.

---

# 7. Warehouse

Warehouse aşağıdaki modüllere bağlıdır.

```text
Product

↓

Warehouse
```

Warehouse kullananlar

* Sales
* Production
* QC
* Logistics
* Finance

---

# 8. Logistics

```text
Warehouse

↓

Logistics
```

Bağımlılıklar

* Warehouse
* Sales
* Purchase

Logistics tamamlandıktan sonra

↓

Stock Movement

↓

Shipment

↓

Delivery

oluşturur.

---

# 9. Production

Production

```text
Warehouse

↓

Product

↓

Production
```

Production

çıktı üretir

↓

QC

↓

Warehouse

↓

Finance

---

# 10. QC

QC

bağımlıdır

```text
CRM

↓

Warehouse

↓

Production

↓

QC
```

QC

çıktıları

↓

Finance

↓

Customer Service

↓

Analytics

---

# 11. Finance

ERP'nin merkezi modülüdür.

Bağımlılıklar

```text
CRM

Sales

Purchase

Warehouse

Production

HR

↓

Finance
```

Finance

hiçbir modülü tetiklemez.

Sadece muhasebeleştirir.

---

# 12. HR

Bağımlılık

```text
Kernel

↓

HR
```

HR'yi kullananlar

* Payroll
* Projects
* Production
* Service

---

# 13. Projects

Bağımlılık

```text
CRM

↓

HR

↓

Projects
```

---

# 14. Service

Bağımlılık

```text
CRM

↓

Warehouse

↓

Service
```

---

# 15. BI

BI

hiçbir modüle veri sağlamaz.

Sadece okur.

```text
Finance

CRM

HR

Production

Warehouse

QC

↓

BI
```

---

# 16. AI Engine

AI bütün modülleri kullanır.

```text
CRM

Finance

Warehouse

Production

HR

Projects

↓

AI
```

AI

hiçbir tabloya doğrudan yazmaz.

Her işlem servisler üzerinden yapılır.

---

# 17. Workflow

Workflow

bütün modülleri yönetir.

```text
Workflow

↓

Sales

↓

Purchase

↓

Finance

↓

HR

↓

QC

↓

Service
```

---

# 18. Event Bus

Her modül event üretir.

Örnek

```text
SalesOrderCreated

↓

ReserveStock

↓

CreateShipment

↓

CreateInvoice

↓

PostAccounting

↓

NotifyCustomer
```

Hiçbir modül diğer modülü doğrudan çağırmaz.

Event üzerinden haberleşir.

---

# 19. Bildirim Sistemi

Tüm modüller ortak Notification Engine kullanır.

Desteklenen kanallar

* Email
* SMS
* Push
* WhatsApp
* Telegram
* Teams
* Slack

---

# 20. Geliştirme Sırası

Kodlama aşağıdaki sıraya göre yapılacaktır.

```
1. Kernel

2. Common Services

3. Product

4. CRM

5. Sales

6. Purchasing

7. Warehouse

8. Logistics

9. Production

10. QC

11. Finance

12. HR

13. Projects

14. Service

15. BI

16. AI

17. Integrations

18. Marketplace
```

Bu sıra zorunludur.

---

# 21. Yasak Bağımlılıklar

Aşağıdaki bağımlılıklar oluşturulamaz.

❌ Finance → CRM

❌ Warehouse → Finance

❌ QC → Finance

❌ HR → Finance

❌ BI → Business Logic

❌ AI → Database

❌ Controller → DbContext

❌ UI → Entity

❌ Domain → Infrastructure

---

# 22. Temel Mimari İlkesi

Her modül yalnızca kendinden önce gelen katmanlara bağımlı olabilir.

Hiçbir modül kendi seviyesindeki başka bir modülün veritabanına doğrudan erişemez.

Modüller arası iletişim yalnızca aşağıdaki yollarla yapılabilir:

* Application Services
* Domain Events
* Event Bus
* Integration Events
* REST API
* gRPC (gerektiğinde)

Bu kural Business Operating System mimarisinin temelidir ve tüm ajanlar tarafından zorunlu olarak uygulanacaktır.
