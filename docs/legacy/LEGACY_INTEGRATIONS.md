# Legacy Integrations — Discovery Catalog

**Version:** 2.0 · **Task:** 022 · **Agent:** 6

---

## Özet

| Tip | Keşif |
|-----|-------|
| REST API | 8 |
| Webhook | 3 |
| Marketplace | 14 adapter |
| e-Belge (TR) | 3 |
| Ödeme gateway | 2 |
| SMS | 2 |
| Import (Excel/CSV/JSON/XML) | 4 |
| Banka ekstre | 1 |
| **Toplam entegrasyon noktası** | **37** |

---

## Entegrasyon Matrisi

| ID | Tip | Legacy | Protokol | BOS modül | Epic |
|----|-----|--------|----------|-----------|------|
| INT-01 | Marketplace | Finance TrendyolService | REST | `MarketplaceAdapter` | EPIC-LEG-021 |
| INT-02 | Marketplace | Finance HepsiburadaService | REST | `MarketplaceAdapter` | EPIC-LEG-021 |
| INT-03 | Marketplace | Finance N11Service | REST | `MarketplaceAdapter` | EPIC-LEG-021 |
| INT-04 | Marketplace hub | Emare Pazar registry.py | REST + Celery | `MarketplaceSyncService` | EPIC-LEG-021 |
| INT-05 | Webhook outbound | Finance WebhookDispatcher | HMAC REST | `WebhookDispatcher` | EPIC-LEG-021 |
| INT-06 | Webhook | emare-crm WebhookService | REST + retry | `IntegrationWebhook` | EPIC-LEG-021 |
| INT-07 | Webhook inbound | emare-crm WebhookReceiverController | REST | `WebhookReceiver` | EPIC-LEG-021 |
| INT-08 | e-Fatura | Finance EInvoiceController | GIB-oriented | `EInvoiceAdapter` | EPIC-LEG-021 |
| INT-09 | e-SMM | Finance ESmmServisi | TR e-belge | `ESmmAdapter` | EPIC-LEG-021 |
| INT-10 | GIB sorgu | Finance GibSorguServisi | REST/XML | `TaxpayerLookup` | EPIC-LEG-021 |
| INT-11 | SMS | Finance SmsService | HTTP provider | `SmsGateway` | EPIC-LEG-021 |
| INT-12 | SMS kampanya | Saloon ProcessCampaignQueue | Queue | `CampaignSms` | EPIC-LEG-021 |
| INT-13 | Import batch | raporlama-app DataImportService | CSV/JSON | `DataImportBatch` | EPIC-LEG-008 |
| INT-14 | Import/export | emare-crm ImportExportService | Excel/CSV/OFX | `DataImportBatch` | EPIC-LEG-008 |
| INT-15 | Bank statement | Finance BankStatementImportController | Excel/CSV | `BankReconciliation` | EPIC-LEG-021 |
| INT-16 | PayTR | Saloon PayTRGateway | REST | `PaymentGateway` | Defer (retail) |
| INT-17 | Iyzico | Saloon IyzicoGateway | REST | `PaymentGateway` | Defer (retail) |
| INT-18 | Report API | raporlama-app ReportApiController | REST JSON | `ReportingApi` | EPIC-LEG-008 |
| INT-19 | TCMB FX | emare-crm DovizService | XML | `CurrencyRateProvider` | EPIC-LEG-021 |
| INT-20 | Mail | Elyafgroup SMTP/IMAP | SMTP/IMAP | Mevcut | — |
| INT-21 | WhatsApp | Elyafgroup | Meta API | Mevcut | — |
| INT-22 | Asterisk | Elyafgroup + emarecc | SIP/AMI | Mevcut kısmi | EPIC-LEG-019 |

---

## Marketplace Adapter Registry (Emare Pazar)

14 adapter: Trendyol, Hepsiburada, N11, Amazon TR, PTT, Çiçeksepeti, vb.  
**BOS pattern:** `IMarketplaceAdapter` + tenant config + sync SLA job.

---

## Import Pipeline İlkeleri (raporlama-app)

- Column mapping
- Preview before commit
- Batch versioning
- Rollback on failure
- FIFO lot creation on stock import

→ `EPIC-LEG-008`

---

## Needs Architect Review

- e-Fatura adapter: Finance inline vs ayrı Integration bounded context — **Needs Architect Review**
- 14 marketplace: tek modül mü microservice mi? — ADR gerekli
