# ADR-0001 — Architecture Principles

**Status:** Accepted
**Date:** 2026-06-27
**Decision Makers:** Architecture Team

---

# Context

Emare Business Operating System (BOS), klasik bir ERP uygulaması değildir.

Platform;

* ERP
* CRM
* BPM
* AI
* Integration Platform
* Marketplace

özelliklerini tek mimari altında birleştirmektedir.

Bu nedenle başlangıçta temel mimari prensiplerinin tanımlanması gerekmektedir.

---

# Decision

Platform aşağıdaki mimari ilkeleri benimser.

## 1. Domain Driven Design

Business kuralları domain içerisinde modellenir.

Her bounded context bağımsızdır.

---

## 2. Clean Architecture

Bağımlılık yönü

```text id="adr001"
Domain

↓

Application

↓

Infrastructure

↓

API

↓

UI
```

---

## 3. Event Driven Architecture

Business Engine'ler birbirini doğrudan çağırmaz.

Event Bus kullanılır.

---

## 4. AI Native

AI sonradan eklenen bir chatbot değildir.

Platformun doğal parçasıdır.

---

## 5. Metadata Driven

Ekranlar

Formlar

Workflow

Dashboard

metadata üzerinden yönetilir.

---

## 6. API First

Her Business Engine API üzerinden erişilebilir olmalıdır.

---

## 7. Multi Tenant

Her kayıt TenantId taşır.

Tenant izolasyonu zorunludur.

---

## 8. Zero Trust

Hiçbir istek varsayılan olarak güvenilir değildir.

---

## 9. Async First

Uzun süren işlemler Queue üzerinden yürütülür.

---

## 10. Cloud Native

Platform Docker ve Kubernetes uyumlu tasarlanır.

---

# Consequences

Bu kararlar aşağıdaki sonuçları doğurur.

Pozitif

* Ölçeklenebilir mimari
* Modüler geliştirme
* AI entegrasyonu kolay
* Mikroservise geçiş kolay

Negatif

* İlk geliştirme maliyeti artar.
* Öğrenme eğrisi yüksektir.
* Dokümantasyon zorunludur.

---

# Related Documents

* ERP_MIMARISI.md
* EVENT_BUS.md
* DOMAIN_MODEL.md
* BOUNDED_CONTEXTS.md
* SECURITY_ARCHITECTURE.md
