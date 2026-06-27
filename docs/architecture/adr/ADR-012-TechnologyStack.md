# ADR-012 — Technology Stack

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS kurumsal ERP+CRM+BPM+AI platformu olarak onlarca modül, çok kiracılı SaaS, event-driven mimari ve AI native tasarım gereksinimlerini karşılayan tutarlı bir teknoloji yığını seçilmelidir. Dağınık teknoloji seçimleri operasyonel karmaşıklık, hiring zorluğu ve entegrasyon maliyeti üretir. `README.md`, `ORTAK_TEKNIK_PROTOKOL.md`, `DEPLOYMENT_ARCHITECTURE.md` ve `FRONTEND_STANDARDLARI.md` mevcut stack kararlarını tanımlar.

---

## Decision

**Kilitli teknoloji yığını:**

| Katman | Teknoloji | Versiyon / Not |
|---|---|---|
| **Backend Runtime** | .NET | 8 LTS |
| **Backend Framework** | ASP.NET Core | Minimal API / Controller |
| **ORM** | EF Core | PostgreSQL provider |
| **Database** | PostgreSQL | `timestamptz`, `jsonb`, `xmin` concurrency |
| **Read Optimization** | Dapper | Ağır dashboard/rapor sorguları |
| **Cache** | Redis | L2 cache, session, rate limit |
| **Message Broker** | RabbitMQ / compatible | Outbox poller hedefi |
| **Application Mediator** | MediatR | CQRS Command/Query + pipeline behaviors |
| **Validation** | FluentValidation + Zod | Backend + frontend |
| **Frontend Framework** | Next.js | 16 (App Router) |
| **UI Components** | Shadcn UI | Skeleton, Dialog, form primitives |
| **Frontend i18n** | emare-i18n | Type-safe, zero dependency |
| **HTTP Client** | apiClient (axios wrapper) | `@/lib/api/client` |
| **Notifications (toast)** | sweetAlert | `@/lib/sweetalert` |
| **Charts** | Recharts | Control Tower grafikleri |
| **Auth** | JWT + BCrypt | Cookie storage (ADR-008) |
| **Container** | Docker | Multi-stage build |
| **Orchestration** | Kubernetes | Production hedef |
| **CI/CD** | GitHub Actions | Build, test, security scan |
| **Observability** | Serilog + OpenTelemetry | Structured logging, trace |
| **Testing** | xUnit, NSubstitute | Domain/Application/API test pyramid |

**Kritik kurallar:**

- PostgreSQL: tüm `DateTime` alanları **`DateTimeKind.Utc`** (`ANAYASA.md`).
- Frontend: business rule UI'da yok; DTO/Contract only.
- API response: `Result<T>` → `ApiResponse<T>` mapping (`API_STANDARDLARI.md`).
- Dual repository: kod private repo; mimari doküman public repo (`AGENTS.md`).

**Cloud native hedef:** Docker + Kubernetes; horizontal scaling; TLS 1.3; AES-256 at rest.

---

## Consequences

**Pozitif:**

- .NET 8 + PostgreSQL kurumsal ekosistem uyumu.
- Next.js 16 + Shadcn hızlı UI geliştirme.
- MediatR + EF Core + Outbox kanıtlanmış .NET pattern'leri.
- Tek stack ile hiring ve eğitim standardizasyonu.

**Negatif:**

- Microsoft + JavaScript ekosistem bağımlılığı.
- Next.js SSR + i18n hydration karmaşıklığı.
- Kubernetes operasyonel uzmanlık gerektirir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Node.js backend** | Mevcut .NET domain modeli ve EF Core yatırımı. |
| **MongoDB (primary)** | Transactional ERP finans/HR verisi için relational model gerekli. |
| **Angular / Vue frontend** | Next.js App Router + SSR + mevcut ekip yönelimi. |
| **Java/Spring Boot** | Mevcut Emare BOS .NET codebase ve agent runbook uyumu. |
| **Serverless-only (Lambda)** | Long-running workflow, outbox poller, WebSocket/SSE ihtiyaçları. |

---

## References

- [README.md](../../../README.md)
- [ORTAK_TEKNIK_PROTOKOL.md](../../../ORTAK_TEKNIK_PROTOKOL.md)
- [DEPLOYMENT_ARCHITECTURE.md](../../../DEPLOYMENT_ARCHITECTURE.md)
- [FRONTEND_STANDARDLARI.md](../../../FRONTEND_STANDARDLARI.md)
- [DATA_ARCHITECTURE.md](../../../DATA_ARCHITECTURE.md)
- [ANAYASA.md](../../../ANAYASA.md)
