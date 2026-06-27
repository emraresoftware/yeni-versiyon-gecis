# ADR-010 — Workflow Engine

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS'ta onay süreçleri (teklif, yevmiye fişi, izin, stok transferi, CAPA, karar defteri) modül koduna gömülmemelidir. Gömülü onay mantığı tekrar eder, SLA/eskalasyon kuralları tutarsızlaşır ve event-driven mimari ile uyumsuz kalır. `WORKFLOW_ENGINE.md` merkezi workflow motorunu tanımlar.

---

## Decision

Tüm iş süreçleri, onay mekanizmaları, görev atamaları, SLA kuralları ve eskalasyonlar **Workflow Engine** tarafından yönetilir.

**Sorumluluk ayrımı:**

| Motor | Rol |
|---|---|
| **Rule Engine** | Eşik/limit değerlendirmesi (karar verici) |
| **Workflow Engine** | Adım koordinasyonu, SLA, insan görevleri, eskalasyon (süreç işletici) |
| **Event Bus** | Tamamlanan adım event'lerini dağıtır (sonuç dağıtıcı) |

**Standart workflow tanımları (örnek):**

| Workflow | Trigger | SLA | Output Events |
|---|---|---|---|
| `CrmProposalApproval` | `CrmProposalSent` | 24h | `CrmProposalApproved`, `CrmProposalDeclined` |
| `FinanceJournalEntryPosting` | Fiş onay talebi | 48h | `FinanceJournalEntryPosted` |
| `HrLeaveApproval` | `HrLeaveRequested` | 72h | `HrLeaveApproved`, `HrLeaveRejected` |
| `LogisticsStockTransferApproval` | `StockTransferRequested` | 12h | `LogisticsStockTransferCompleted` |
| `QcClaimResolution` | `QcClaimCreated` | 5 iş günü | `QcClaimResolved` |
| `DecisionLogApproval` | `DecisionLogCreated` | 24h | `DecisionLogApproved` |

**AI sınırları:**

- AI risk analizi ve onay **önerisi** sunabilir.
- AI **nihai onay veremez**; human-in-the-loop zorunlu.
- AI yalnızca `AI.Agent.Execute` ve kullanıcı context permission'ları ile workflow tetikleyebilir.

**Workflow tanımı:** Metadata-driven workflow definition (adımlar, koşullar, atanan rol) veritabanında saklanır; kod içi hardcoded onay zinciri yasaktır.

---

## Consequences

**Pozitif:**

- Onay süreçleri merkezi yönetilir ve değiştirilebilir.
- SLA/eskalasyon tutarlı; Notification Engine ile entegre.
- Event Bus ile modüller arası gevşek coupling korunur.

**Negatif:**

- Workflow engine altyapısı MVP'de significant investment.
- Metadata-driven tanım UI/admin tooling gerektirir.
- Karmaşık süreçlerde debug zorluğu.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Hardcoded approval in handlers** | Tekrar, tutarsız SLA, test zorluğu. |
| **External BPM only (Camunda)** | Entegrasyon maliyeti; BOS-native engine tercih edildi. |
| **Email-only approval chain** | Audit, SLA, permission entegrasyonu zayıf. |
| **Rule Engine only (no workflow)** | Adım sırası, insan görevi, eskalasyon eksik kalır. |

---

## References

- [WORKFLOW_ENGINE.md](../../../WORKFLOW_ENGINE.md)
- [EVENT_BUS.md](../../../EVENT_BUS.md)
- [RULE_ENGINE.md](../../../RULE_ENGINE.md)
- [CONTROL_TOWER_FINAL_SCOPE.md](../../product/CONTROL_TOWER_FINAL_SCOPE.md)
- [AI_ENGINE.md](../../../AI_ENGINE.md)
