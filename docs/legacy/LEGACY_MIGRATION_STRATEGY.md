# Legacy Migration Strategy — Knowledge, Not Code

**Version:** 2.0 · **Task:** 022 · **Agent:** 6

---

## İlke

Emare BOS migrasyonu **kod kopyalama değildir**. Laravel/PHP legacy → .NET 8 BOS taşıması:

1. **Domain spec** çıkar (aggregate, invariant, event)
2. **Test port** (invariant → xUnit)
3. **Handler implement** (Clean Architecture)
4. **Control Tower projection** (read model)

---

## Taşıma Modelleri

| Model | Ne zaman | Örnek |
|-------|----------|-------|
| **A — Spec port** | İş kuralı kanıtlı, stack farklı | Finance JournalEntry borç=alacak |
| **B — Pattern adopt** | Mimari pattern, farklı domain | Saloon SaleObserver → Outbox handler |
| **C — UI shell retain** | CT mock → API bağlantısı | Elyaf FabricDashboard |
| **D — Consolidate** | Duplicate model birleşimi | Customer → CrmAccount |
| **E — Defer / ayrı ürün** | Kapsam dışı | emarepos restoran POS |

---

## Birincil Bilgi Kaynakları (öncelik sırası)

| Sıra | Kaynak | Modül |
|------|--------|-------|
| 1 | yeni-versiyon-gecis ADR + traceability | Hedef blueprint |
| 2 | Emare Finance standalone | Finance, BOM, MRP, stok, HR |
| 3 | emare-crm | CRM workflow, OnayMotoru, Blueprint |
| 4 | Emare Saloon + raporlama-app | Perakende observer, FIFO import |
| 5 | Elyafgroup | Platform kernel, CT UI, omnichannel |
| 6 | Emare Pazar | Marketplace adapter registry |
| 7 | translation-manager | Merkezi i18n |

---

## Faz Planı

### Faz 0 — Platform (mevcut)
Tenant, RBAC, audit, outbox, i18n paketi. Kaynak: Elyafgroup Platform.

### Faz 1 — CRM + Sales + Workflow
- CrmAccount/Contact/Opportunity/Proposal API
- OnayMotoru → `ApprovalWorkflow` engine
- Kaynak: Elyafgroup + emare-crm

### Faz 2 — Finance Core
AccountPlan, JournalEntry, Invoice, Payment. Kaynak: **Emare Finance**.

### Faz 3 — Inventory + Purchasing
StockMovement, PO, GoodsReceipt. Kaynak: Finance + emare-crm Satinalma.

### Faz 4 — Production + MRP
BOM, BomOperation, Workstation, MrpRule. Kaynak: **Emare Finance**.

### Faz 5 — Textile Extension
Sample/Collection/Style genişletme + yeni fabric/yarn domain. Kaynak: Elyaf UI spec + SME workshop.

### Faz 6 — Control Tower Data Layer
Mock→DB KPI projection. Kaynak: FEATURE_TRACEABILITY + CONTROL_TOWER scope.

### Paralel — Entegrasyon & Rapor
Import batch, marketplace, e-belge. Kaynak: raporlama-app, Emare Pazar, Finance EInvoice.

---

## Birleştirme Kararları

| Konu | Karar | Gerekçe |
|------|-------|---------|
| CRM müşteri | Platform `CrmAccount` canonical | DOMAIN_MODEL + duplicate risk |
| Onay motoru | Tek ERP workflow engine | OnayMotoru + ExpenseReport + Blueprint approval |
| Numara serisi | Finance `DocumentSeries` + Elyaf `NumberSequence` birleşimi | DocumentSeries daha olgun (yıllık reset, prefix) |
| Ticket vs ERP workflow | Ticket ayrı kalır; ERP onay ayrı engine | Farklı bounded context |
| UTC DateTime | ANAYASA zorunlu | Legacy Laravel `now()` ihlalleri port edilmez |

---

## Taşınmamalı

- Dervişler / worktree duplicate kopyalar
- emarerp gömülü obsolete Finance
- Desktop Ticket snapshot
- emarepos (ayrı restoran ürünü)
- emareciftlik (tarım vertical)

---

## Doğrulama Kapıları

Her faz sonunda:

- [ ] İş kuralları `BUSINESS_RULE_MIGRATION_MATRIX.md`'de "Ported" veya "Spec ready"
- [ ] Domain event `EVENT_BUS.md` ile hizalı
- [ ] Permission `SECURITY_AUTHORIZATION.md` ile hizalı
- [ ] CT widget en az 1 gerçek veri kaynağına bağlı
- [ ] Chief Architect Review (public repo)

---

## Conflict Kayıtları

| ID | Konu | Legacy A | Legacy B | Karar |
|----|------|----------|----------|-------|
| C-01 | Müşteri entity | Ticket `Customer` | Platform `CrmAccount` | CrmAccount canonical — **Needs Architect Review** birleşim zamanlaması |
| C-02 | Numara serisi | Elyaf CR-/PR- basit | Finance DocumentSeries zengin | Birleşik `DocumentSeries` aggregate — EPIC-LEG-022 |
| C-03 | Stok yöntemi | Finance hareket tabanlı | raporlama-app FIFO lot | BOS: FIFO lot + movement — **Needs Architect Review** |
