# 📈 Observability Mimarisi

**Title:** Observability Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** README.md
**Related Documents:** EVENT_BUS.md, WORKFLOW_ENGINE.md, SECURITY_ARCHITECTURE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Observability, Emare Business Operating System (BOS) platformunun çalışmasını gerçek zamanlı olarak izleyen, ölçen, analiz eden ve sorunları proaktif olarak tespit eden platform katmanıdır.

Amaç;

* Sistem sağlığını izlemek
* Hataları erken tespit etmek
* Performansı ölçmek
* AI destekli operasyon yönetimi sağlamak
* SLA takibi yapmak

---

# Temel Mimari

```text
Application

↓

Logs

Metrics

Traces

Events

↓

Observability Platform

↓

Dashboard

↓

Alerting

↓

AI Operations
```

---

# Ana Bileşenler

## Logging Engine

Tüm servisler standart log üretmelidir.

Log seviyeleri

* Trace
* Debug
* Information
* Warning
* Error
* Critical

---

## Metrics Engine

Toplanan metrikler

* CPU
* RAM
* Disk
* Network
* API Response Time
* Queue Length
* Active Users
* Workflow Count
* Event Count

---

## Distributed Tracing

Her işlem CorrelationId ile takip edilir.

Örnek

```text
Login

↓

Sales

↓

Finance

↓

Notification

↓

Completed
```

Her adım aynı TraceId altında izlenebilir.

---

# Health Checks

Her servis aşağıdaki kontrolleri sağlamalıdır.

* Database
* Redis
* Queue
* Storage
* Search
* External APIs
* AI Services

---

# Service Health

Durumlar

* Healthy
* Degraded
* Unhealthy

---

# Alert Engine

Alarm üretilebilir.

Örnek

* CPU > %90
* Queue > 1000
* API > 2 sn
* Error Rate > %5

---

# SLA Monitoring

Takip edilir.

* Workflow SLA
* API SLA
* Queue SLA
* Background Job SLA

---

# Dashboard

Operasyon panelinde gösterilir.

* Sistem Durumu
* API Durumu
* Event Bus
* Workflow
* AI
* Integration
* Notification

---

# Event Monitoring

Takip edilir.

* Published
* Processed
* Failed
* Retried
* Dead Letter

---

# Queue Monitoring

Gösterilir.

* Bekleyen İş
* İşlenen İş
* Başarısız İş
* Ortalama Süre

---

# API Monitoring

Ölçülür.

* Ortalama Süre
* P95
* P99
* Error Rate
* Request Count

---

# AI Monitoring

İzlenir.

* Model
* Token Kullanımı
* Ortalama Yanıt Süresi
* Başarı Oranı
* Maliyet
* Prompt Versiyonu

---

# Tenant Monitoring

Her tenant için

* Kullanıcı
* API Kullanımı
* Depolama
* AI Kullanımı
* Lisans

izlenebilir.

---

# Audit

Observability değiştirilemez.

Tüm kayıtlar

* Timestamp
* Tenant
* User
* Service
* Severity

ile saklanır.

---

# Desteklenen Teknolojiler

Mimari aşağıdaki sistemlerle uyumlu olacak şekilde tasarlanmalıdır.

* OpenTelemetry
* Prometheus
* Grafana
* Loki
* Jaeger
* Elastic Stack
* Azure Monitor
* AWS CloudWatch

---

# AI Operations (AIOps)

AI aşağıdaki alanlarda destek sağlar.

* Anomali Tespiti
* Kapasite Tahmini
* Olası Arıza Tahmini
* Log Özetleme
* Kök Neden Analizi
* Alarm Önceliklendirme

---

# Güvenlik

Observability verileri;

* Tenant İzolasyonu
* RBAC
* Audit
* Şifreleme

ile korunmalıdır.

---

# Temel Mimari İlkeleri

* Tüm servisler standart log üretmelidir.
* Tüm API'ler izlenebilir olmalıdır.
* Dağıtık izleme desteklenmelidir.
* CorrelationId zorunludur.
* AI Operations desteklenmelidir.
* Dashboard gerçek zamanlı çalışmalıdır.

---

# Nihai Vizyon

Observability sayesinde Emare BOS;

* kendi sağlığını izleyen,
* sorunları erken tespit eden,
* performansını ölçen,
* AI destekli operasyon yönetimi yapan,

kurumsal seviyede gözlemlenebilir bir platform haline gelir.
