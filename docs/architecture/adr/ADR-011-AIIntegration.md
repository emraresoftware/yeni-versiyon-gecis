# ADR-011 — AI Integration (AI Native Architecture)

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS "AI Native" platform olarak tasarlanmıştır; AI sonradan eklenen bir chatbot değil, mimari çekirdeğin parçasıdır. CEOAgent, SalesAgent, FinanceAgent gibi otonom ajanlar iş süreçlerini destekler; ancak güvenlik (prompt injection, tenant leakage, privilege escalation) ve uyumluluk (KVKK/GDPR) riskleri kontrolsüz AI entegrasyonunda kritiktir. `AI_ENGINE.md` ve `SECURITY_ARCHITECTURE.md` bu sınırları tanımlar.

---

## Decision

**AI Engine** merkezi platform bileşeni olarak tüm modüllerin AI yeteneklerini yönetir.

**Mimari akış:**

```text
Kullanıcı → AI Copilot → Context Engine → Reasoning Engine
    → Business Engine (MediatR) → Workflow Engine → Event Bus → Business Modules
```

**Bileşenler ve sınırlar:**

| Bileşen | İzin | Yasak |
|---|---|---|
| **AI Copilot (UI)** | Soru-cevap, komut önerisi | Doğrudan veri kaydetme/silme |
| **AI Agent** | Analiz, öneri, asistan işlem | Nihai onay, yetki aşımı |
| **Context Engine** | Tenant/rol/permission context enjeksiyonu | İzin bypass |
| **RAG** | Tenant-scoped belge arama | Cross-tenant belge erişimi |
| **AI Gateway** | Model routing, kota, güvenlik filtre | Token/izin limiti aşımı |

**Kilitli kurallar:**

1. AI **doğrudan DbContext/raw SQL** kullanamaz; yalnızca Application Command/Query (MediatR).
2. AI **nihai onay veremez**; human-in-the-loop zorunlu (ADR-010).
3. Her AI aksiyonu **audit log** (`AIAuditLogs`) bırakır.
4. AI tenant isolation, RBAC ve ABAC'e tabidir; tetikleyen kullanıcının permission context'i taşınır.
5. Dış LLM'e gönderilen veride **PII maskeleme** zorunlu.
6. RAG sorgularında **TenantId metadata filter** zorunlu.
7. Copilot yanıt dili: ADR-007 hiyerarşisi.

**Kilitli ajan listesi:** CEOAgent, SalesAgent, FinanceAgent, HRAgent, ProductionAgent, QCAgent, LogisticsAgent, AnalyticsAgent, LegalAgent, ComplianceAgent, AIOrchestrator.

---

## Consequences

**Pozitif:**

- AI tüm modüllerde tutarlı güvenlik sınırları ile çalışır.
- Copilot Control Tower KPI/snapshot verilerine bağlanabilir.
- Event-driven mimari ile AI reaktif otomasyon sağlar.

**Negatif:**

- AI Gateway, Context Engine, audit altyapısı yatırım gerektirir.
- Prompt injection savunması sürekli güncelleme ister.
- LLM maliyeti ve latency operasyonel bütçe kalemi.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Chatbot-only (no agents)** | İş süreci otomasyonu ve Control Tower entegrasyonu zayıf. |
| **Direct DB access for AI** | Tenant leakage ve audit bypass riski. |
| **Fully autonomous AI approvals** | Regülasyon ve iş güvenliği kabul edilemez. |
| **Single monolithic LLM call from UI** | Context, permission, audit katmanları atlanır. |

---

## References

- [AI_ENGINE.md](../../../AI_ENGINE.md)
- [SECURITY_ARCHITECTURE.md](../../../SECURITY_ARCHITECTURE.md)
- [SECURITY_AUTHORIZATION.md](../../../SECURITY_AUTHORIZATION.md)
- [LOCALIZATION_I18N_STANDARDS.md](../../product/LOCALIZATION_I18N_STANDARDS.md)
- [WORKFLOW_ENGINE.md](../../../WORKFLOW_ENGINE.md)
- [UX_REVIEW.md](../../product/UX_REVIEW.md)
