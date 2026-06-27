# 📊 Analytics Engine Mimarisi

## Amaç

Analytics Engine, Emare Business Operating System (BOS) içerisindeki tüm raporlama, iş zekâsı (BI), KPI yönetimi, veri analizi ve tahminleme süreçlerini yöneten merkezi analiz platformudur.

Bu katman yalnızca rapor üretmez.

Şirketin operasyonlarını gerçek zamanlı analiz eder, eğilimleri belirler ve karar destek mekanizması oluşturur.

---

# Temel Mimari

```text
Business Engines

↓

Event Bus

↓

Analytics Engine

↓

Data Warehouse

↓

Dashboards

↓

AI Insights
```

Analytics Engine hiçbir Business Engine'i değiştirmez.

Sadece okur ve analiz eder.

---

# Analytics Katmanları

## Operational Analytics

Gerçek zamanlı operasyon verileri.

Örnek

* Açık Sipariş
* Bekleyen Sevkiyat
* Üretimdeki İş Emirleri
* Bekleyen Onaylar

---

## Management Analytics

Yönetici raporları.

Örnek

* Satış Performansı
* Karlılık
* Departman Verimliliği
* Personel Performansı
* Nakit Akışı

---

## Strategic Analytics

Uzun dönem analizleri.

Örnek

* Büyüme Trendleri
* Müşteri Yaşam Boyu Değeri
* Talep Tahmini
* Üretim Kapasite Planlaması

---

# KPI Engine

KPI'lar merkezi olarak tanımlanır.

Örnek KPI'lar

## Sales

* Revenue
* Gross Profit
* Conversion Rate
* Average Order Value

---

## Finance

* Cash Flow
* EBITDA
* Budget Variance
* Current Ratio

---

## HR

* Employee Turnover
* Leave Rate
* Recruitment Time
* Training Hours

---

## Production

* OEE
* Scrap Rate
* Capacity Utilization
* On-Time Production

---

## Logistics

* Inventory Turnover
* Delivery Performance
* Picking Accuracy
* Warehouse Occupancy

---

## Quality

* First Pass Yield
* Complaint Rate
* Defect Rate
* CAPA Completion Rate

---

# Dashboard Engine

Desteklenen bileşenler

* KPI Cards
* Line Charts
* Bar Charts
* Pie Charts
* Heatmaps
* Gauges
* Tables
* Maps
* Timelines

Dashboard'lar metadata ile oluşturulur.

---

# Drill Down

Her KPI detayına inilebilir.

Örnek

```text
Revenue

↓

Region

↓

Customer

↓

Invoice

↓

Journal Entry
```

---

# Drill Through

KPI'dan ilgili modüle geçiş yapılabilir.

Örnek

```text
Complaint Rate

↓

QC Claim

↓

Order

↓

Customer
```

---

# Veri Kaynakları

Analytics aşağıdaki kaynaklardan beslenebilir.

* CRM
* Finance
* HR
* Production
* Warehouse
* Logistics
* QC
* Projects
* Service

---

# Data Warehouse

Analitik amaçlı ayrı veri modeli kullanılabilir.

Katmanlar

* Raw Data
* Cleansed Data
* Business Data
* Analytics Model

Operasyonel veritabanı doğrudan ağır rapor yükü altında bırakılmaz.

---

# OLAP

Desteklenebilir.

* Slice
* Dice
* Pivot
* Rollup
* Drill Down

---

# Tahminleme (Forecast)

Analytics Engine aşağıdaki tahminleri destekler.

* Sales Forecast
* Demand Forecast
* Inventory Forecast
* Cash Flow Forecast
* Workforce Forecast
* Production Forecast

Tahmin algoritmaları AI Engine ile birlikte çalışır.

---

# Anomali Tespiti

Örnek

* Olağandışı satış
* Negatif stok eğilimi
* Beklenmeyen maliyet artışı
* Hatalı üretim oranı
* Nakit akışı riski

---

# Benchmark

Departmanlar karşılaştırılabilir.

Örnek

```text
Warehouse A

↓

Warehouse B

↓

Warehouse C
```

---

# Gerçek Zamanlı Analitik

Event Bus üzerinden canlı KPI güncellenebilir.

Örnek

```text
StockTransferred

↓

Analytics

↓

Inventory KPI Updated
```

---

# AI Insights

Analytics Engine, AI Engine ile birlikte çalışır.

Örnek

* KPI açıklamaları
* Trend yorumları
* Risk değerlendirmeleri
* Otomatik yönetici özeti
* Kök neden analizi (Root Cause Analysis)

---

# Export

Desteklenen formatlar

* PDF
* Excel
* CSV
* JSON

---

# Yetkilendirme

Her kullanıcı yalnızca yetkili olduğu KPI ve raporları görebilir.

RBAC ve ABAC kuralları uygulanır.

---

# Tenant İzolasyonu

Her tenant kendi Analytics alanına sahiptir.

KPI tanımları tenant bazında özelleştirilebilir.

---

# Audit

Tüm rapor erişimleri kayıt altına alınır.

Kaydedilen bilgiler

* Kullanıcı
* Rapor
* Filtreler
* Tarih
* Süre

---

# Performans

Analytics Engine;

* Cache kullanmalıdır.
* Büyük raporları arka planda oluşturmalıdır.
* Gerçek zamanlı KPI'lar Event Bus ile güncellenmelidir.
* Veri ambarı mimarisini desteklemelidir.

---

# Temel Mimari İlkeleri

* Analytics yalnızca veri okur.
* İş kurallarını değiştirmez.
* Dashboard'lar metadata ile oluşturulur.
* KPI'lar merkezi tanımlanır.
* AI ile birlikte karar destek üretir.
* Tenant izolasyonunu zorunludur.
* Tüm raporlar denetlenebilir olmalıdır.

---

# Nihai Vizyon

Analytics Engine sayesinde Emare BOS;

* operasyonel,
* yönetsel,
* stratejik

analizleri tek platformda sunabilen, AI destekli, gerçek zamanlı ve ölçeklenebilir kurumsal bir iş zekâsı altyapısına sahip olur.

Bu motor, şirket yönetiminin veri odaklı karar almasını sağlayan merkezi analiz katmanıdır.
