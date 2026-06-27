# ADR-003 — Command Query Responsibility Segregation (CQRS)

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Control Tower dashboard'ları yoğun okuma (KPI aggregation, list projection, scorecard) ve nadir yazma (onay, karar kaydı) desenine sahiptir. Tek model üzerinden hem kompleks sorgular hem transactional yazma işlemleri aynı entity pipeline'ından geçerse N+1, lock contention ve performans bütçesi aşımları oluşur (`PERFORMANCE_GUIDE.md`). Application katmanında MediatR tabanlı Command/Query ayrımı zaten composition root'ta planlanmıştır.

---

## Decision

Platform **CQRS** destekler; ancak **tüm CRUD operasyonları için zorunlu değildir**.

**Uygulama kuralları:**

| Desen | Kullanım | Örnek |
|---|---|---|
| **Command** | Durum değiştiren işlemler | `CreateCrmProposalCommand`, `PostFinanceJournalEntryCommand` |
| **Query** | Salt okunur projection | `GetCeoExecutiveSnapshotQuery`, `GetSalesKpiWinRateQuery` |
| **MediatR Pipeline** | Validation, Authorization, Logging behaviors | `ValidationBehavior`, `AuthorizationBehavior` |
| **Read Optimization** | Dashboard/KPI için `.AsNoTracking()`, Dapper, read replica | CEO KPI aggregation, finansal raporlar |

**CQRS zorunlu olduğu alanlar:**

- Tüm Control Tower KPI ve snapshot endpoint'leri.
- Büyük listeleme ve rapor sorguları (keyset pagination).
- Onay workflow'larına bağlı Command'lar.

**CQRS opsiyonel olduğu alanlar:**

- Basit master data CRUD (lookup tabloları, küçük referans entity'ler).

**Yasak:**

- Query handler içinde doğrudan durum değiştirme (side effect).
- Command handler içinde raporlama aggregation (read concern ayrılmalı).

---

## Consequences

**Pozitif:**

- Okuma/yazma performansı bağımsız optimize edilir.
- Control Tower API'leri traceability matrisi ile Command/Query bazında izlenebilir.
- Testler use case bazında izole edilir.

**Negatif:**

- Handler sayısı artar; naming ve klasör disiplini gerekir.
- Read model eventual consistency gerektiren senaryolarda UI state yönetimi karmaşıklaşır.
- Aşırı CQRS basit CRUD'ta gereksiz boilerplate üretir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Full CQRS (her endpoint)** | Basit lookup'lar için maliyet/fayda düşük. |
| **Separate Read Database (başlangıç)** | Read replica + projection yeterli; dual-write riski erken aşamada gereksiz. |
| **Repository-only (no CQRS)** | Dashboard KPI yükü altında performans ve test izolasyonu zayıflar. |
| **Event Sourcing + CQRS** | Audit için cazip; MVP karmaşıklığı yüksek. |

---

## References

- [DOMAIN_MODEL.md](../../../DOMAIN_MODEL.md)
- [CONTROL_TOWER_FINAL_SCOPE.md](../../product/CONTROL_TOWER_FINAL_SCOPE.md)
- [FEATURE_TRACEABILITY_MATRIX.md](../../product/FEATURE_TRACEABILITY_MATRIX.md)
- [PERFORMANCE_GUIDE.md](../../project-management/performance/PERFORMANCE_GUIDE.md)
- [API_STANDARDLARI.md](../../../API_STANDARDLARI.md)
