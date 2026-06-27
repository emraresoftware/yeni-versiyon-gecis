# ADR-006 — Multi-Tenant Architecture

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS SaaS olarak birden fazla organizasyona (tenant) hizmet verir. Kiracılar arası veri sızıntısı kurumsal platform için en kritik güvenlik ihlalidir. `SECURITY_ARCHITECTURE.md` tenant izolasyonunu database, storage, cache, queue, search, AI context ve audit katmanlarında zorunlu kılar. `DOMAIN_MODEL.md` tüm tenant-scoped entity'lerde `TenantId` alanını standartlaştırır.

---

## Decision

Platform **shared database, shared schema, tenant-discriminator** modelini kullanır.

**Zorunlu kurallar:**

1. **TenantId alanı:** Kiracı verisi taşıyan tüm entity'ler `Guid TenantId` içerir (`ITenantScoped` arayüzü).
2. **Global Query Filter:** EF Core `HasQueryFilter(e => e.TenantId == _tenantProvider.TenantId)` otomatik uygulanır.
3. **Fail-Fast:** Geçerli `TenantId` yoksa işlem reddedilir; cross-tenant erişim engellenir.
4. **JWT Claims:** Token içinde `TenantId` claim zorunlu; middleware request context'e set eder.
5. **Outbox / Event / Cache / RAG:** Tüm async ve cache katmanlarında tenant discriminator taşınır.
6. **Ham SQL / Dapper:** Global filter çalışmaz; `TenantId` parametresi manuel zorunlu.

**İzolasyon kapsamı:**

| Katman | Mekanizma |
|---|---|
| Database | Global query filter + TenantId index |
| Storage | Tenant-prefixed path / container |
| Cache | Tenant-scoped key prefix |
| Queue / Outbox | TenantId metadata |
| AI Context / RAG | Metadata filter by TenantId |
| Audit | TenantId + UserId |

**Sistem entity'leri:** `Tenant`, `User`, `Role` tenant-specific değil; kernel seviyesinde yönetilir.

---

## Consequences

**Pozitif:**

- Tek deployment ile çok kiracı; operasyonel maliyet düşük.
- Standart EF Core pattern ile hızlı implementasyon.
- Integration test ile tenant leakage otomatik doğrulanabilir.

**Negatif:**

- "Noisy neighbor" riski; büyük tenant performansı diğerlerini etkileyebilir.
- Global filter bypass (raw SQL) insan hatasına açık.
- Dedicated tenant (single-tenant DB) talebi için ek model gerekir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Database-per-Tenant** | İzolasyon güçlü; operasyonel/migration maliyeti MVP için yüksek. |
| **Schema-per-Tenant** | Orta yol; PostgreSQL schema yönetimi karmaşık. |
| **Application-level filter only** | Bypass riski yüksek; defense-in-depth ihlali. |
| **Row-Level Security (RLS) only** | EF filter + RLS çift katman gelecekte değerlendirilebilir; şimdilik EF filter kanonik. |

---

## References

- [DOMAIN_MODEL.md](../../../DOMAIN_MODEL.md)
- [SECURITY_ARCHITECTURE.md](../../../SECURITY_ARCHITECTURE.md)
- [SECURITY_AUTHORIZATION.md](../../../SECURITY_AUTHORIZATION.md)
- [EVENT_BUS.md](../../../EVENT_BUS.md)
- [SECURITY_REVIEW.md](../../project-management/security/SECURITY_REVIEW.md)
