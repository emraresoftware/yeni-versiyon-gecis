# ADR-002 — Domain-Driven Design (DDD)

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS; CRM, Finance, HR, Production, Logistics, QC ve 16 Control Tower modülünü tek platformda birleştirir. Modüller arası kavram çakışması (ör. generic `Order` vs `SalesOrder`), yanlış aggregate sınırları ve cross-context FK bağımlılıkları uzun vadede veri tutarsızlığı ve refactoring maliyeti üretir. `DOMAIN_MODEL.md` ve `BOUNDED_CONTEXTS.md` bu riskleri tanımlar.

---

## Decision

Platform **Domain-Driven Design** prensiplerini uygular:

1. **Bounded Context:** Her Business Engine kendi context'inde çalışır; hiçbir context başka context'in iç modeline doğrudan bağımlı olamaz.
2. **Aggregate Root:** Tutarlılık sınırı aggregate root üzerinden yönetilir (ör. `CrmAccount`, `FinanceJournalEntry`, `SalesOrder`).
3. **Ubiquitous Language:** Entity, event ve permission adları `UBIQUITOUS_LANGUAGE.md` ve modül prefix standardına uyar (`CrmAccount`, `FinanceInvoice`, `HrLeave`).
4. **Cross-Context İletişim:** Yalnızca Domain Events, Integration Events, Application Contracts ve logical FK (`Guid`) ile; physical FK across contexts yasaktır.
5. **Ortak Entity Kuralları:** Tenant-scoped entity'ler `Id`, `TenantId`, audit alanları, `IsDeleted`, `RowVersion` taşır; tüm `DateTime` alanları UTC'dir.
6. **Shared Kernel:** Minimal tutulur; genişleyen shared kernel modül bağımsızlığını zedeler.

**Context haritası (özet):**

```text
Kernel → Shared Kernel → Business Contexts → Integration Events → Other Contexts
```

---

## Consequences

**Pozitif:**

- Modüller bağımsız geliştirilebilir ve test edilebilir.
- Domain event'ler gevşek coupling sağlar.
- Entity Matrix ile kod-domain hizalaması denetlenebilir.

**Negatif:**

- Context sınırları disiplin gerektirir; cross-context shortcut cazip gelir.
- Logical FK ile referential integrity DB seviyesinde zorlanmaz; application katmanı sorumluluğu artar.
- Ubiquitous language eğitimi ve dokümantasyon yükü vardır.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Database-First Modeling** | İş kuralları DB şemasına hapsolur; bounded context ayrımı zayıflar. |
| **Single Unified Domain Model** | 16+ modülde kavram karmaşası; değişiklik maliyeti katlanır. |
| **CRUD-Centric Anemic Model** | İş kuralları service katmanına dağılır; aggregate tutarlılığı kaybolur. |
| **Event Sourcing (tüm domain)** | Audit avantajı var; operasyonel karmaşıklık MVP için aşırı. |

---

## References

- [DOMAIN_MODEL.md](../../../DOMAIN_MODEL.md)
- [BOUNDED_CONTEXTS.md](../../../BOUNDED_CONTEXTS.md)
- [UBIQUITOUS_LANGUAGE.md](../../../UBIQUITOUS_LANGUAGE.md)
- [EVENT_BUS.md](../../../EVENT_BUS.md)
- [ENTITY_STANDARDLARI.md](../../../ENTITY_STANDARDLARI.md)
