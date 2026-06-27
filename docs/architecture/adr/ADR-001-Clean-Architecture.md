# ADR-001 — Clean Architecture

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare Business Operating System (BOS), onlarca modül, çok kiracılı SaaS dağıtımı, AI ajan destekli geliştirme ve uzun ömürlü kurumsal bakım gereksinimleri taşır. Katmanlar arası bağımlılık kontrolü olmadan framework sızıntısı, test edilemez iş mantığı ve modüller arası sıkı coupling oluşur. Mevcut mimari dokümanlar (`docs/adr/0002-clean-architecture.md`, `ORTAK_TEKNIK_PROTOKOL.md`) bu ihtiyacı tanımlar; kurumsal ADR kaydı olarak bu karar resmileştirilir.

---

## Decision

Platform **Clean Architecture** kullanır. Bağımlılık yönü yalnızca içe doğrudur:

```text
Presentation (Web / Mobile)
        ↓
       API
        ↓
  Application
        ↓
     Domain
        ↑
Infrastructure (Persistence, External Services)
```

**Katman sorumlulukları:**

| Katman | Sorumluluk | Yasaklar |
|---|---|---|
| **Domain** | Aggregate, Entity, Value Object, Domain Event, Domain Service | EF Core, ASP.NET, HttpContext, IConfiguration |
| **Application** | Use case, Command/Query, Validation, Authorization, Event publish | Repository implementasyonu, DbContext |
| **Infrastructure** | EF Core, PostgreSQL, Redis, Queue, Email, AI provider | Business rule |
| **API** | Endpoint, Authentication, Model binding, Result mapping | Business logic, DbContext, Repository |
| **Web** | Next.js UI, form, dashboard | Domain entity, business rule |

**Zorunlu kurallar:**

- Repository arayüzleri Application katmanında; implementasyon Infrastructure'da.
- Tüm servisler DI container üzerinden çözülür; `new` ile servis oluşturulmaz.
- Application katmanı `Result<T>` döndürür; beklenmeyen durumlar dışında exception fırlatılmaz.
- UI yalnızca DTO/Contract kullanır; domain entity doğrudan expose edilmez.

---

## Consequences

**Pozitif:**

- Yüksek test edilebilirlik (Domain/Application unit test).
- Framework bağımsız domain modeli.
- AI ajanların katman sınırlarına uygun kod üretimi.
- Mikroservise geçişte modül ayrıştırma kolaylaşır.

**Negatif:**

- İlk geliştirme hızı düşer; boilerplate artar.
- Öğrenme eğrisi yüksektir; tüm ekip katman disiplinine uymalıdır.
- Katman ihlali code review'da sık tespit edilir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Transaction Script / Anemic Domain** | İş kuralları dağılır; test ve AI kod üretimi zorlaşır. |
| **Modular Monolith (katmansız)** | Kısa vadede hızlı; uzun vadede bağımlılık spiraline girer. |
| **Microservices (başlangıç)** | Operasyonel maliyet ve dağıtık tutarlılık erken aşamada gereksiz. |
| **Hexagonal Architecture (Ports & Adapters)** | Clean Architecture ile uyumlu; Emare BOS terminolojisi Clean Architecture ile standardize edildi. |

---

## References

- [DOMAIN_MODEL.md](../../../DOMAIN_MODEL.md)
- [BOUNDED_CONTEXTS.md](../../../BOUNDED_CONTEXTS.md)
- [ORTAK_TEKNIK_PROTOKOL.md](../../../ORTAK_TEKNIK_PROTOKOL.md)
- [docs/adr/0002-clean-architecture.md](../../adr/0002-clean-architecture.md)
- [SECURITY_ARCHITECTURE.md](../../../SECURITY_ARCHITECTURE.md)
