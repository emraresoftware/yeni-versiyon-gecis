# 🔄 Workflow Engine Mimarisi

**Title:** Workflow Engine Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** EVENT_BUS_MIMARISI.md
**Related Documents:** RULE_ENGINE.md, NOTIFICATION_ENGINE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Workflow Engine, Emare Business Operating System (BOS) içerisinde tüm iş süreçlerini yöneten merkezi otomasyon motorudur.

Sistemde hiçbir iş süreci manuel olarak modüller içerisine gömülmez.

Tüm onay mekanizmaları, görev atamaları, SLA kuralları, eskalasyonlar ve otomasyonlar Workflow Engine tarafından yönetilir.

---

# Temel Prensip

Bir işlem gerçekleşir.

↓

Workflow tetiklenir.

↓

Kurallar değerlendirilir.

↓

Görev oluşturulur.

↓

Onay alınır.

↓

Sonraki adım çalıştırılır.

↓

İşlem tamamlanır.

---

# Workflow Bileşenleri

## Workflow Definition

Sürecin tanımıdır.

Örnek

```text
Satın Alma Süreci

↓

Talep

↓

Müdür Onayı

↓

Finans Onayı

↓

Satın Alma

↓

Teslim

↓

Kapanış
```

---

## Workflow Instance

Her çalışan süreç bir instance oluşturur.

Örnek

```text
Workflow

↓

Purchase Approval

↓

Instance #5842
```

---

## Workflow Step

Her süreç adımı bağımsızdır.

Desteklenen adımlar

* Approval
* Task
* Notification
* Decision
* Integration
* Script
* Delay
* AI Decision

---

## Workflow Variables

Her süreç değişken taşıyabilir.

Örnek

```text
PurchaseAmount

Department

EmployeeId

WarehouseId

Currency

ManagerId
```

---

# Desteklenen Adım Tipleri

## Approval

Bir veya daha fazla kullanıcının onayını bekler.

---

## Multi Approval

Örnek

```text
Finans

↓

Satın Alma

↓

CEO
```

Hepsi onaylamadan süreç devam etmez.

---

## Sequential Approval

```text
Manager

↓

Director

↓

CEO
```

Sıralı çalışır.

---

## Parallel Approval

```text
HR

Finance

Legal

Production
```

Aynı anda çalışır.

---

## Decision

Koşul değerlendirir.

Örnek

```text
Amount > 100000

↓

CEO Onayı

↓

Devam
```

---

## Timer

Belirli süre bekler.

Örnek

```text
24 Saat

↓

Hatırlatma Gönder
```

---

## Escalation

Süre dolarsa

↓

Üst yöneticiye aktar.

---

## Notification

Desteklenen kanallar

* Email
* SMS
* Push
* WhatsApp
* Telegram
* Teams
* Slack

---

## Integration

REST

Webhook

Kafka

RabbitMQ

gRPC

çağrıları yapılabilir.

---

## AI Decision

AI öneri oluşturabilir.

Örnek

```text
Satın alma riskli mi?

↓

AI Analizi

↓

Risk %

↓

Workflow devam eder.
```

AI tek başına nihai onay vermez; politika izin veriyorsa öneri sunar veya belirli sınırlar içinde otomatik karar verebilir.

---

# Workflow Durumları

```text
Draft

↓

Published

↓

Running

↓

Waiting

↓

Completed

↓

Cancelled

↓

Failed
```

---

# SLA Yönetimi

Her Workflow SLA tanımlayabilir.

Örnek

```text
İzin Talebi

↓

24 Saat

↓

Aşıldı

↓

Escalation
```

---

# Görev Motoru

Workflow görev üretir.

Görev özellikleri

* Atanan Kullanıcı
* Departman
* Öncelik
* Başlangıç
* Bitiş
* SLA
* Durum
* Açıklama

---

# Workflow Versiyonlama

Her süreç versiyon taşır.

```text
Purchase Approval v1

Purchase Approval v2

Purchase Approval v3
```

Eski instance eski versiyonla çalışmaya devam eder.

---

# Yetkilendirme

Workflow aşağıdaki yetkileri kontrol eder.

* Kullanıcı
* Rol
* Departman
* Tenant
* Organizasyon
* Tutar Limiti
* Lokasyon
```

---

# BPMN Uyumluluğu

Workflow Engine aşağıdaki BPMN kavramlarını destekleyecek şekilde tasarlanmalıdır.

* Start Event
* End Event
* User Task
* Service Task
* Exclusive Gateway
* Parallel Gateway
* Timer Event
* Message Event
* Signal Event

---

# Event Bus Entegrasyonu

Workflow Event Bus ile haberleşir.

Örnek

```text
PurchaseApproved

↓

Workflow

↓

StockReserveRequested

↓

FinanceJournalRequested

↓

NotificationRequested
```

---

# AI Entegrasyonu

AI aşağıdaki alanlarda Workflow'u destekler.

* Risk Analizi
* Öncelik Belirleme
* Tahminleme
* Otomatik Kategori
* Doküman Analizi
* SLA İhlal Tahmini
* İş Yükü Tahmini

---

# No-Code Workflow Designer

Yönetici kullanıcılar sürükle bırak ile süreç oluşturabilir.

Desteklenen öğeler

* Node
* Connection
* Condition
* Approval
* Delay
* Script
* Integration
* AI Node

Kod yazmadan yeni süreç geliştirilebilir.

---

# Audit

Her adım kayıt altına alınır.

Kaydedilen bilgiler

* Kim başlattı
* Kim onayladı
* Kim reddetti
* Ne zaman gerçekleşti
* Eski değer
* Yeni değer
* Süre

---

# Performans

Workflow Engine

* Asenkron çalışmalıdır.
* Event Bus kullanmalıdır.
* Uzun süren işlemleri Queue üzerinden yürütmelidir.
* Tek transaction içerisinde gereksiz bekleme yapmamalıdır.

---

# Temel Mimari İlkeleri

* Workflow tanımları kod içerisine gömülmez.
* Süreçler metadata olarak saklanır.
* Tüm süreçler versiyonlanır.
* Event Bus ile entegre çalışır.
* Yetkilendirme merkezi güvenlik katmanı üzerinden yapılır.
* AI yalnızca tanımlı politika ve yetki sınırları içinde karar mekanizmasına katkı sağlar.
* Workflow Engine, Emare BOS içerisindeki tüm modüllerin ortak süreç yönetim altyapısıdır.
