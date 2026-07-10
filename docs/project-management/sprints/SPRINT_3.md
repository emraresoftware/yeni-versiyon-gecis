# Sprint 3 — Omnichannel Messaging Core (OMC)

**Başlangıç:** Sprint 2 (Control Tower) tamamlandı  
**Son güncelleme:** 2026-07-10  
**İlerleme:** **25%** (Messaging Gateway, Mimari Sözleşmeler ve Conversation Store tamamlandı)

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

---

## Backlog (Sıradaki)

| # | Task | Sorumlu Ajan | Bağımlılık | Durum |
|---|------|--------------|------------|-------|
| 1 | **TASK_MSG_003** — Message Normalizer | A11 Bridge | TASK_MSG_002 | ⏳ Bekliyor |
| 2 | **TASK_MSG_004** — Agent Router | A11 Bridge | TASK_MSG_003 | ⏳ Bekliyor |
| 3 | **TASK_MSG_005** — Policy Guard | A11 Bridge | TASK_MSG_004 | ⏳ Bekliyor |
| 4 | **TASK_MSG_006** — Messenger Adapter | A11 Bridge | TASK_MSG_005 | ⏳ Bekliyor |
| 5 | **TASK_MSG_007** — Instagram Adapter | A11 Bridge | TASK_MSG_006 | ⏳ Bekliyor |
| 6 | **TASK_MSG_008** — WhatsApp Adapter | A11 Bridge | TASK_MSG_007 | ⏳ Bekliyor |
| 7 | **TASK_MSG_009** — Web Chat Adapter | A11 Bridge | TASK_MSG_008 | ⏳ Bekliyor |
| 8 | **TASK_MSG_010** — Human Inbox | A11 Bridge | TASK_MSG_009 | ⏳ Bekliyor |
| 9 | **TASK_MSG_011** — Audit Log | A11 Bridge | TASK_MSG_010 | ⏳ Bekliyor |
| 10 | **TASK_MSG_012** — Timeline Sync | A11 Bridge | TASK_MSG_011 | ⏳ Bekliyor |

