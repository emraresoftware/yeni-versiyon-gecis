# Sprint 0 — Development Readiness (SPRINT_0_DEVELOPMENT_READINESS.md)

**Title:** Sprint 0 — Development Readiness
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** MASTER_ARCHITECTURE_INDEX.md
**Related Documents:** ANAYASA.md, ORTAK_TEKNIK_PROTOKOL.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Created development readiness guidelines for Sprint 0. |

---

# 1. Sprint 0 Amacı

* Kod üretimine başlamadan önce son hazırlıkların yapılması.
* Ortak standartların doğrulanması.
* Repository yapısının ve kod üretim disiplininin kilitlenmesi.

---

# 2. Geliştirme Ekibi

Geliştirme sürecinde toplam 4 geliştirme ajanı kullanılacaktır. Her ajanın sorumluluk alanları ve repo sahiplikleri aşağıdaki gibidir:

## Ajan 1 — Platform Core
* **Sorumluluk:** Shared Kernel, Common, Identity, Authorization, Tenant, Audit, Event Bus, Workflow, Rule Engine, Metadata, Infrastructure, Persistence, PostgreSQL, Redis.
* **Repository Ownership:**
  ```text
  src/BuildingBlocks
  src/Platform
  src/Infrastructure
  ```

## Ajan 2 — Commercial Core
* **Sorumluluk:** CRM, Sales, Proposal, SalesOrder, Customer.
* **Repository Ownership:**
  ```text
  src/Modules/CRM
  src/Modules/Sales
  ```

## Ajan 3 — Finance Core
* **Sorumluluk:** Finance, Journal, Bank, Cash, Budget, Tax.
* **Repository Ownership:**
  ```text
  src/Modules/Finance
  ```

## Ajan 4 — Operations Core
* **Sorumluluk:** Warehouse, Logistics, Production, QC, Service.
* **Repository Ownership:**
  ```text
  src/Modules/Warehouse
  src/Modules/Production
  src/Modules/QC
  src/Modules/Logistics
  ```

---

# 3. Branch Stratejisi

* `main`
* `develop`
* `release/*`
* `feature/*`
* `hotfix/*`

Her ajan yalnızca kendi feature branch'inde çalışır. Doğrudan `develop` veya `main` branch'lerine commit yapılması yasaktır.

---

# 4. Pull Request Kuralları

PR açılmadan önce zorunlu kontroller:
* Derleme (Build) başarılı olmalıdır.
* Testler (Unit/Integration) sıfır hata ile çalışmalıdır.
* Lint ve statik analiz başarılı olmalıdır.
* Architecture Rule (Clean Architecture katman yönleri) ihlali olmamalıdır.
* Yeni Entity Matrix tanımlarına tam uyum olmalıdır.
* Permission Matrix tanımlarına tam uyum olmalıdır.

---

# 5. Definition of Done (Bitti Tanımı)

Bir geliştirme görevinin tamamlanmış sayılabilmesi için aşağıdaki koşullar aranır:
* Kod yazıldı ve test edildi.
* Unit Test yazıldı.
* Integration Test yazıldı.
* Dokümantasyon güncellendi (gerekliyse).
* Event Matrix güncellendi (gerekliyse).
* Entity Matrix güncellendi (gerekliyse).
* ADR (Architecture Decision Record) gerekiyorsa oluşturuldu.

---

# 6. Kod Üretim Sırası

Geliştirme süresince aşağıdaki bağımlılık sırasına riayet edilecektir. Bu sıra değiştirilmeyecektir:
1. Shared Kernel
2. Common
3. Identity
4. Infrastructure
5. Event Bus
6. Rule Engine
7. Workflow
8. CRM
9. Sales
10. Finance
11. Warehouse
12. Production
13. QC
14. Service
15. Analytics
16. AI

---

# 7. Sprint 1 Hedefi

Sprint 1 sonunda yalnızca aşağıdakiler tamamlanmış olmalıdır:
* Solution Structure
* Shared Kernel
* Common Library
* Identity
* Tenant
* Authorization
* PostgreSQL
* Migration Framework
* Event Bus Skeleton
* Rule Engine Skeleton
* Workflow Skeleton

> [!IMPORTANT]
> Hiçbir iş modülü (CRM, Finance, Logistics vb.) Sprint 1'de tamamlanmaya çalışılmayacaktır. Sadece çekirdek mimari ve iskelet yapılar kilitlenecektir.
