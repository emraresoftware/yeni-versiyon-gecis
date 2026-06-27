# ⚖️ Rule Engine Mimarisi

**Title:** Rule Engine Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** WORKFLOW_ENGINE_MIMARISI.md
**Related Documents:** METADATA_ENGINE.md, SECURITY_ARCHITECTURE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Rule Engine, Emare Business Operating System (BOS) içerisindeki tüm iş kurallarını merkezi olarak yöneten motordur.

İş kuralları uygulama koduna gömülmez.

Kurallar metadata olarak tanımlanır ve çalışma zamanında değerlendirilir.

---

# Temel Prensip

```text
İşlem

↓

Rule Engine

↓

Koşullar

↓

Karar

↓

Workflow / Event Bus

↓

Sonuç
```

Rule Engine yalnızca karar üretir.

İşlemi ilgili Business Engine gerçekleştirir.

---

# Rule Türleri

## Validation Rule

Veri doğrulama.

Örnek

* Vergi numarası zorunlu
* E-posta formatı
* Negatif stok yasak
* Borç = Alacak

---

## Business Rule

İş mantığı.

Örnek

```text
Sipariş > 100.000 TL

↓

CEO Onayı
```

---

## Calculation Rule

Hesaplama.

Örnek

* KDV
* İskonto
* Komisyon
* Amortisman
* Kur farkı

---

## Authorization Rule

Yetkilendirme.

Örnek

```text
Departman = Finance

↓

Muhasebe ekranını aç
```

---

## Notification Rule

Koşula bağlı bildirim.

Örnek

```text
Stok < Minimum

↓

Depo Müdürüne Bildirim
```

---

## AI Rule

AI değerlendirmesi.

Örnek

```text
Risk > %80

↓

Finance Agent Analiz
```

---

# Rule Yapısı

Her kural aşağıdaki bilgileri içerir.

* Rule Id
* Name
* Module
* Category
* Priority
* Version
* Status
* Description

---

# Condition

Koşullar.

Desteklenen operatörler

* =
* !=
* >
* <
* > =
* <=
* Contains
* StartsWith
* EndsWith
* In
* Between
* Exists

---

# Logical Operators

Desteklenir.

* AND
* OR
* NOT

Örnek

```text
Country = TR

AND

Amount > 50000

↓

Kural Çalışır
```

---

# Actions

Rule başarılı olursa yapılacak işlemler.

Desteklenen aksiyonlar

* Workflow Başlat
* Event Yayınla
* Görev Oluştur
* Bildirim Gönder
* Alan Güncelle
* Hesaplama Yap
* AI Analizi Başlat

---

# Priority

Birden fazla kural varsa öncelik uygulanır.

Örnek

```text
Priority

1

↓

2

↓

3
```

---

# Rule Groups

Kurallar gruplanabilir.

Örnek

Finance Rules

↓

Tax Rules

↓

Invoice Rules

↓

Payment Rules

---

# Rule Versioning

Her kural versiyon taşır.

```text
CreditLimitRule

↓

v1

↓

v2

↓

v3
```

Eski işlemler eski versiyon ile çalışmaya devam eder.

---

# Rule Scope

Kurallar uygulanabilir.

* Global
* Tenant
* Module
* Department
* User

---

# Rule Execution

Çalışma sırası

```text
Load Rule

↓

Validate

↓

Evaluate

↓

Execute

↓

Publish Event

↓

Complete
```

---

# Rule Cache

Kurallar bellekte tutulabilir.

Değişiklik olduğunda cache yenilenir.

---

# Rule Audit

Her çalıştırma kayıt altına alınır.

Kaydedilen bilgiler

* Rule
* Kullanıcı
* Tenant
* Tarih
* Sonuç
* Süre

---

# Rule Güvenliği

Kural değiştirme yetkisi yalnızca yetkili yöneticilere verilir.

Her değişiklik;

* Audit Log
* Version
* Yetki kontrolü

ile korunur.

---

# AI Entegrasyonu

AI aşağıdaki alanlarda Rule Engine'i destekleyebilir.

* Risk skoru üretme
* Dolandırıcılık analizi
* Anomali tespiti
* Kural önerisi
* Kural optimizasyonu

AI mevcut kuralları değiştirmez; yalnızca öneri sunar veya yetkili politikalar kapsamında otomatik güncelleme talebi oluşturabilir.

---

# Workflow Entegrasyonu

Rule Engine ve Workflow birlikte çalışır.

```text
Purchase Request

↓

Rule Engine

↓

Approval Required

↓

Workflow Engine

↓

CEO Approval
```

---

# Event Bus Entegrasyonu

Her Rule sonucu Event oluşturabilir.

Örnek

```text
CreditLimitExceeded

↓

Publish Event

↓

Finance

↓

Sales

↓

Notification
```

---

# Örnek Kurallar

## Satış

* Kredi limiti aşılırsa sipariş durdur.
* İskonto %20 üzerindeyse yönetici onayı iste.

## Finans

* Borç ≠ Alacak ise fişi kaydetme.
* Kapalı döneme fiş girişini engelle.

## Lojistik

* Negatif stok oluşturma.
* Yetersiz stokta transferi reddet.

## İK

* İzin bakiyesi yetersizse talebi reddet.
* Fazla mesai limiti aşılırsa yöneticiyi bilgilendir.

## Kalite

* Hata oranı %5'i aşarsa CAPA başlat.
* Aynı ürün için tekrar eden şikâyette kalite yöneticisini ata.

---

# Temel Mimari İlkeleri

* İş kuralları kod içine gömülmez.
* Kurallar metadata olarak saklanır.
* Kurallar versiyonlanır.
* Workflow ve Event Bus ile entegre çalışır.
* AI karar mekanizmasını destekler.
* Tüm çalıştırmalar denetlenebilir olmalıdır.

---

# Nihai Vizyon

Rule Engine sayesinde Emare BOS;

* iş kurallarını merkezi yöneten,
* kod bağımlılığını azaltan,
* tenant bazında özelleştirilebilen,
* sürümlenebilir,
* denetlenebilir,
* AI ile desteklenen

kurumsal bir karar motoruna sahip olur.

Bu motor, tüm Business Engine'lerin ortak karar katmanıdır.
