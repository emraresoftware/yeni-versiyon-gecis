# Legacy Database Patterns — Discovery Catalog

**Version:** 2.0 · **Task:** 022 · **Agent:** 6

---

## Özet

| Pattern | Elyafgroup BOS | Emare Finance | emare-crm |
|---------|----------------|---------------|-----------|
| Tenant isolation | Global query filter | BelongsToTenant trait | TenantScope |
| Soft delete | ISoftDelete + interceptor | SoftDeletes trait | SoftDeletes |
| Audit columns | AuditableEntity | timestamps + created_by | AuditLog JSON diff |
| Number sequence | NumberSequence | DocumentSeries ★ | Import serial only |
| Lot/batch | — | ProductBatch, ProductSerial | — |
| Archive/history | ElyafKpiSnapshot | Document versioning | Blueprint history |
| Composite key | UUID PK + tenant filter | Standard id | UUID HasUuids |

★ = birincil port adayı

---

## Pattern → BOS Eşlemesi

| ID | Pattern | Legacy en iyi kaynak | BOS hedef | Epic |
|----|---------|---------------------|-----------|------|
| DB-01 | Tenant global filter | Elyafgroup AppDbContext | `ITenantEntity` + filter | — (mevcut) |
| DB-02 | Soft delete interceptor | Elyafgroup SoftDeleteSaveChangesInterceptor | Platform interceptor | — (mevcut) |
| DB-03 | Field-level audit | emare-crm AuditLog | Rich audit for CRM entities | EPIC-LEG-002 |
| DB-04 | DocumentSeries atomic | Finance DocumentSeries.php | `DocumentSeries` aggregate | EPIC-LEG-022 |
| DB-05 | Simple NumberSequence | Elyafgroup NumberSequence | Merge into DocumentSeries | EPIC-LEG-022 |
| DB-06 | Product batch/lot | Finance ProductBatch | `InventoryLot` textile traceability | EPIC-LEG-016 |
| DB-07 | Product serial | Finance ProductSerial | `InventorySerial` | EPIC-LEG-010 |
| DB-08 | KPI time series | Elyafgroup ElyafKpiSnapshot | `KPIValue` projection | EPIC-LEG-007 |
| DB-09 | Outbox | Elyafgroup OutboxMessage | Mevcut | — |
| DB-10 | Reconciliation history | Finance Reconciliation | `BankReconciliation` | EPIC-LEG-021 |
| DB-11 | Document archive | Finance document management migration | `DocumentArchive` | EPIC-LEG-021 |
| DB-12 | Webhook delivery log | Finance WebhookLog | `IntegrationDeliveryLog` | EPIC-LEG-021 |

---

## DocumentSeries Detay (port spec)

Finance `DocumentSeries.generateNumber()`:

- prefix, suffix, padding
- yearly / monthly reset
- atomic increment
- per document type

**BOS event:** `DocumentNumberIssued`  
**Conflict:** Elyaf CR-/PR- simpler sequences → birleşim **Needs Architect Review**

---

## PostgreSQL Notları (BOS)

- `timestamptz` → `DateTimeKind.Utc` zorunlu (ANAYASA)
- Legacy Laravel `now()` local → port edilmez
- Precision: financial columns `decimal(18,2)` (Task 013 standard)

---

## Taşınmamalı DB Pattern

- SQLite single-tenant (Floragenix) — referans only
- emarecc init.sql tahsilat şeması — ayrı CC ürünü
