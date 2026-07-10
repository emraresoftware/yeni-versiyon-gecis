# Sprint 3 — Omnichannel Messaging Core (OMC)

**Başlangıç:** Sprint 2 (Control Tower) tamamlandı  
**Son güncelleme:** 2026-07-10  
**İlerleme:** **55%** (Messaging Gateway, Conversation Store, Message Normalizer, Batch Normalization ve Batch Result Model/Telemetry tamamlandı)

---

## Hedef

Emare BOS üzerinde çalışan yapay zeka ajanlarının ve insan operatörlerin müşteriyle iletişim kurduğu tüm kanalları tek bir çatı altında birleştiren kanal bağımsız **Omnichannel Messaging Core (OMC)** altyapısının kurulması.

---

## Tamamlanan Tasklar

| Task | Ajan | Rapor | Çıktı | Durum |
|------|------|-------|-------|-------|
| **TASK_MSG_001** | A11 Bridge | [TASK_MSG_001_REPORT.md](../reports/TASK_MSG_001_REPORT.md) | Messaging Gateway (Webhook payload validation, normalization, tenant resolution, idempotency deduplication, and boundary dispatching) | ✅ Tamamlandı |
| **TASK_MSG_002_PRE_FREEZE** | A11 Bridge | [TASK_MSG_002_PRE_ARCHITECTURE_FREEZE_REPORT.md](../reports/TASK_MSG_002_PRE_ARCHITECTURE_FREEZE_REPORT.md) | Architecture Freeze (Events, ID standards, attachments, handoff & microservice boundary specifications) | ✅ Tamamlandı |
| **TASK_MSG_002** | A11 Bridge | [TASK_MSG_002_REPORT.md](../reports/TASK_MSG_002_REPORT.md) | Conversation Store (Relational PostgreSQL schema, index optimization, repository store persistence for messages, threads, and attachments) | ✅ Tamamlandı |
| **TASK_MSG_003** | A11 Bridge | [TASK_MSG_003_IMPLEMENTATION_REPORT.md](../reports/TASK_MSG_003_IMPLEMENTATION_REPORT.md) | Message Normalizer (Unified adapter parsing, safe attachment URI parsing, spoofing protection) | ✅ Tamamlandı |
| **TASK_MSG_004** | A11 Bridge | [TASK_MSG_004_BATCH_WEBHOOK_NORMALIZATION.md](../reports/TASK_MSG_004_BATCH_WEBHOOK_NORMALIZATION.md) | Batch Webhook Normalization (Preserved ordering, duplicate deduplication, mixed payloads) | ✅ Tamamlandı |
| **TASK_MSG_005** | A11 Bridge | [TASK_MSG_005_IMPLEMENTATION_REPORT.md](../reports/TASK_MSG_005_IMPLEMENTATION_REPORT.md) | Batch Result Model & Telemetry (Item-level stopwatch telemetry, PII-masked metrics, safe error codes) | ✅ Tamamlandı |

---

## Backlog (Sıradaki)

| # | Task | Sorumlu Ajan | Bağımlılık | Durum |
|---|------|--------------|------------|-------|
| 1 | **TASK_MSG_006** — Distributed Locking & Redlock | A11 Bridge | TASK_MSG_005 | ⏳ Bekliyor |
| 2 | **TASK_MSG_007** — Messenger Adapter | A11 Bridge | TASK_MSG_006 | ⏳ Bekliyor |
| 3 | **TASK_MSG_008** — Instagram Adapter | A11 Bridge | TASK_MSG_007 | ⏳ Bekliyor |
| 4 | **TASK_MSG_009** — WhatsApp Adapter | A11 Bridge | TASK_MSG_008 | ⏳ Bekliyor |
| 5 | **TASK_MSG_010** — Web Chat Adapter | A11 Bridge | TASK_MSG_009 | ⏳ Bekliyor |
| 6 | **TASK_MSG_011** — Human Inbox | A11 Bridge | TASK_MSG_010 | ⏳ Bekliyor |
| 7 | **TASK_MSG_012** — Audit Log | A11 Bridge | TASK_MSG_011 | ⏳ Bekliyor |
| 8 | **TASK_MSG_013** — Timeline Sync | A11 Bridge | TASK_MSG_012 | ⏳ Bekliyor |

