# 🧩 Plugin Marketplace Mimarisi

## Amaç

Plugin Marketplace, Emare Business Operating System (BOS) platformunun çekirdeğini değiştirmeden yeni özellikler, modüller, entegrasyonlar ve yapay zekâ ajanları eklenmesini sağlayan genişletilebilir platform katmanıdır.

Amaç;

* Çekirdeği korumak
* Modüler geliştirme yapmak
* Üçüncü taraf geliştiricileri desteklemek
* Tenant bazlı eklenti yönetimi sunmak

---

# Temel Mimari

```text
Business Operating System

↓

Plugin Loader

↓

Plugin Manager

↓

Marketplace

↓

Installed Plugins
```

Çekirdek sistem eklentileri yalnızca tanımlı sözleşmeler (Contracts) üzerinden yükler.

---

# Plugin Türleri

## Business Module

Yeni iş modülü ekler.

Örnek

* Rental Management
* Healthcare
* Education
* Agriculture
* Construction

---

## Integration Plugin

Dış sistem bağlantıları.

Örnek

* SAP Connector
* Oracle Connector
* Shopify Connector
* Trendyol Connector
* Bank Connector

---

## AI Plugin

Yeni yapay zekâ ajanları.

Örnek

* Procurement Agent
* Sustainability Agent
* Energy Agent
* Legal Agent
* Audit Agent

---

## UI Plugin

Arayüz bileşenleri.

* Dashboard Widget
* Custom Page
* Menu
* Form Component
* Chart Component

---

## Report Plugin

Yeni raporlar.

* Finansal Rapor
* Yönetim Raporu
* Üretim KPI
* Kalite Dashboard

---

## Workflow Plugin

Yeni süreçler.

Örnek

* ISO Süreci
* İzin Süreci
* Satın Alma Süreci
* Bakım Süreci

---

# Plugin Yapısı

Her eklenti aşağıdaki bilgileri içerir.

* PluginId
* Name
* Version
* Publisher
* Category
* Description
* License
* Minimum BOS Version
* Permissions
* Dependencies

---

# Plugin Manifest

Her eklenti bir manifest dosyası içerir.

Örnek bilgiler

* Kimlik
* Versiyon
* Desteklenen BOS sürümü
* Yetkiler
* Menü kayıtları
* Event abonelikleri
* API kayıtları

---

# Yaşam Döngüsü

```text
Install

↓

Validate

↓

Register

↓

Enable

↓

Update

↓

Disable

↓

Uninstall
```

Her aşama kayıt altına alınır.

---

# Dependency Management

Plugin'ler başka plugin'lere bağımlı olabilir.

Örnek

```text
Manufacturing Plugin

↓

Inventory Plugin

↓

Kernel
```

Eksik bağımlılık varsa kurulum tamamlanmaz.

---

# Event Bus Entegrasyonu

Plugin'ler Event Bus'a abone olabilir.

Örnek

```text
SalesOrderCreated

↓

Plugin

↓

Custom Action
```

Plugin çekirdeği değiştirmez.

---

# Workflow Entegrasyonu

Plugin yeni Workflow ekleyebilir.

* Approval Flow
* SLA
* Escalation
* Automation

---

# AI Entegrasyonu

Plugin yeni AI Agent ekleyebilir.

Örnek

* Energy Optimization Agent
* Procurement Advisor
* ESG Compliance Agent

---

# UI Entegrasyonu

Plugin;

* Menü
* Sayfa
* Dashboard
* Widget
* Form
* Dialog

ekleyebilir.

---

# API Entegrasyonu

Plugin;

* REST Endpoint
* GraphQL Resolver
* Webhook
* Background Job

ekleyebilir.

---

# Güvenlik

Plugin'ler sandbox mantığıyla çalışmalıdır.

Yetkiler açıkça tanımlanmalıdır.

Örnek

* CRM Read
* Finance Write
* Workflow Execute
* Notification Send

İzin verilmeyen alanlara erişim engellenir.

---

# Tenant Bazlı Yönetim

Her tenant;

* plugin yükleyebilir,
* kaldırabilir,
* devre dışı bırakabilir,
* lisanslayabilir.

Aynı sunucuda çalışan tenant'lar farklı plugin setlerine sahip olabilir.

---

# Marketplace

Marketplace;

* Sürüm bilgisi,
* lisans,
* puanlama,
* yorum,
* güncelleme geçmişi,
* güvenlik durumu

gibi bilgileri sunar.

---

# Güncelleme Yönetimi

Plugin güncellemeleri sürümlüdür.

Desteklenen işlemler

* Update
* Rollback
* Disable
* Remove

Rollback desteği zorunludur.

---

# Audit

Her plugin işlemi kayıt altına alınır.

Kaydedilen bilgiler

* Kuran kullanıcı
* Tenant
* Sürüm
* Tarih
* İşlem
* Sonuç

---

# Performans

Plugin'ler;

* çekirdeği yavaşlatmamalıdır.
* asenkron çalışmalıdır.
* Event Bus üzerinden haberleşmelidir.
* bellek tüketimi izlenmelidir.

---

# Geliştirici Desteği

Plugin geliştirenler için sağlanacaktır.

* SDK
* CLI
* Örnek projeler
* Test araçları
* Dokümantasyon

---

# Temel Mimari İlkeleri

* Çekirdek kod değiştirilmez.
* Plugin'ler sözleşmeler üzerinden çalışır.
* Yetkiler açıkça tanımlanır.
* Event Bus ortak haberleşme katmanıdır.
* Tenant izolasyonu korunur.
* Her plugin sürümlenir.
* Güvenli kaldırma ve geri alma desteklenir.

---

# Nihai Vizyon

Plugin Marketplace sayesinde Emare BOS;

* Sektör bazlı çözümler,
* Müşteri özel geliştirmeler,
* Üçüncü taraf entegrasyonlar,
* AI ajanları,
* Raporlar,
* Kullanıcı arayüzleri

için genişletilebilir bir platform haline gelir.

Bu yapı, Emare BOS'un uzun vadeli ekosistem stratejisinin temelini oluşturur.
