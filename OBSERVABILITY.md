# 📈 Observability Mimarisi

**Title:** Observability Mimarisi
**Version:** 1.1.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-07-12
**Dependencies:** README.md
**Related Documents:** EVENT_BUS.md, WORKFLOW_ENGINE.md, SECURITY_ARCHITECTURE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.1.0   | 2026-07-12 | Agent 0 (Antigravity) | Production stack detayları, health check endpoints ve Docker health probes eklendi. |
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

# 🏭 Production Implementasyon (Temmuz 2026)

Aşağıdaki bölüm, gerçek production ortamında aktif olarak çalışan monitoring stack'i belgelemektedir.

## Aktif Logging Pipeline

```text
.NET 8 API (Serilog)
       │
       ▼
  stdout / file
       │
       ▼
 Promtail Agent (Docker sidecar)
       │
       ▼
   Grafana Loki
       │
       ▼
   Grafana Dashboard
```

**Framework:** Serilog (Structured Logging)
**Transport:** Promtail agent (`emareticket-promtail` container) → Grafana Loki (`emareticket-loki` container)
**Görselleştirme:** Grafana Dashboard
**Log Format:** JSON structured log (timestamp, level, message, properties, exception)

## Docker Container Health Probes

Tüm production container'lar `compose.prod.yml`'de health check tanımına sahiptir:

| Container | Health Check | Interval |
|---|---|---|
| `emareticket-postgres-prod` | `pg_isready` | 10s |
| `emareticket-api-prod` | HTTP → `:8080` | 30s |
| `emareticket-web-prod` | HTTP → `:3000` | 30s |
| `emareticket-wa-bridge` | Socket check | 15s |
| `emareticket-whisper-prod` | HTTP → `/health` | 60s |
| `standalone-asterisk` | `asterisk -rx 'core show uptime'` | 30s |

## API Health Check Endpoints

| Endpoint | Amaç | Auth |
|---|---|---|
| `GET /health` | Temel yaşam kontrolü (DB, Redis, Queue) | Yok |
| `GET /health/ready` | Readiness probe (migration tamamlandı mı?) | Yok |
| `GET /api/tenants/current` | Tenant çözümleme doğrulaması | JWT |

## Asterisk Telephony Monitoring

```bash
# SIP Trunk kayıt durumu
docker exec standalone-asterisk asterisk -rx 'pjsip show registrations'

# Aktif çağrı sayısı
docker exec standalone-asterisk asterisk -rx 'core show channels count'

# Endpoint durumları
docker exec standalone-asterisk asterisk -rx 'pjsip show endpoints'
```

## Container Sağlık Kontrolü

```bash
# Tüm container durumları
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

# API container logları (son 50 satır)
docker logs emareticket-api-prod --tail 50

# Voice Bridge bağlantı durumu
docker logs standalone-voice-bridge --tail 20
```

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

Observability verileri; Tenant İzolasyonu, RBAC, Audit ve Şifreleme (Encryption) ile korunmalıdır. Bu konu için ana kaynak: [SECURITY_ARCHITECTURE.md](file:///Users/emre/yeni-versiyon-gecis/SECURITY_ARCHITECTURE.md).

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
