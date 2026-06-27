# ADR-0002 — Clean Architecture

**Status:** Accepted

**Date:** 2026-06-27

**Decision Makers:** Architecture Team

---

# Context

Emare BOS;

* uzun yıllar geliştirilecek,
* onlarca modül içerecek,
* AI Agent'lar tarafından kod üretilecek,
* çok sayıda geliştirici tarafından geliştirilecek,
* SaaS olarak dağıtılacak

kurumsal bir platformdur.

Katmanların birbirine bağımlı hale gelmesi uzun vadede bakım maliyetini ciddi şekilde artıracaktır.

Bu nedenle katman bağımlılıkları en baştan tanımlanmalıdır.

---

# Decision

Platform Clean Architecture kullanacaktır.

Bağımlılık yönü yalnızca içe doğrudur.

```text
Presentation

↓

API

↓

Application

↓

Domain

```

Infrastructure yalnızca Application ve Domain'e bağımlıdır.

Domain hiçbir katmanı bilmez.

---

# Katmanlar

## Domain

Sorumluluk

* Aggregate
* Entity
* Value Object
* Domain Event
* Domain Service

Domain hiçbir framework bilmez.

Domain içerisinde

❌ EF Core

❌ ASP.NET

❌ HttpContext

❌ IConfiguration

kullanılamaz.

---

## Application

Sorumluluk

* Use Case
* Command
* Query
* Validation
* Authorization
* Workflow çağrıları
* Event Publish

Application Repository Interface kullanır.

Repository implementasyonu bilmez.

---

## Infrastructure

Sorumluluk

* EF Core
* PostgreSQL
* Redis
* File Storage
* Queue
* Email
* SMS
* OCR
* AI Provider

Infrastructure yalnızca implementasyon katmanıdır.

---

## API

Sorumluluk

* Endpoint
* Authentication
* Model Binding
* Result Mapping

Business Logic içermez.

---

## Web

Sorumluluk

* React
* Next.js
* Component
* Form
* Dashboard

Hiçbir business rule içermez.

---

# Dependency Rule

```text
UI

↓

API

↓

Application

↓

Domain

```

Tersi yasaktır.

---

# Yasaklar

Application

↓

Infrastructure

doğrudan referans veremez.

---

Domain

↓

EF Core

yasaktır.

---

Controller

↓

DbContext

yasaktır.

---

Controller

↓

Repository

yasaktır.

---

UI

↓

Entity

yasaktır.

DTO kullanılır.

---

# Repository

Repository Interface

Application katmanında bulunur.

Implementasyon

Infrastructure katmanında bulunur.

---

# Dependency Injection

Tüm servisler

DI Container üzerinden çözülür.

New operatörü ile servis oluşturulmaz.

---

# Result Pattern

Application

Result<T>

döndürür.

Exception yalnızca beklenmeyen durumlarda kullanılır.

---

# CQRS

Platform CQRS destekler.

Ancak yalnızca ihtiyaç olan modüllerde uygulanır.

Her CRUD için zorunlu değildir.

---

# Event Bus

Application

↓

Domain Event

↓

Event Bus

↓

Subscribers

---

# Testing

Domain

↓

Unit Test

Application

↓

Integration Test

API

↓

API Test

Web

↓

UI Test

---

# Consequences

Avantajlar

* Test edilebilirlik
* Modülerlik
* Framework bağımsızlığı
* AI Agent uyumluluğu
* Uzun ömürlü mimari

Dezavantajlar

* İlk geliştirme daha uzun sürer.
* Öğrenme eğrisi yüksektir.

---

# Related Documents

* ERP_MIMARISI.md
* DOMAIN_MODEL.md
* BOUNDED_CONTEXTS.md
* ORTAK_TEKNIK_PROTOKOL.md
* DEVELOPER_PLATFORM.md

---

# Decision

Emare BOS'un tüm Business Engine'leri Clean Architecture kurallarına uymak zorundadır.

Bu karar platformun değiştirilemez mimari prensiplerinden biridir.
