# FAP-003: Decision Trace Verification Report

**Task:** FAP-003 — Decision Trace Verification
**Agent:** Chief Architect & Verification Agent
**Date:** 2026-07-13
**Scope:** `EmareTicket.Application.Services.ControlTower.Decisions.*`

---

## 1. Decision Chain Verification

### Zincir: `Snapshot → Evidence → Rule → Priority → Decision → Recommended Action`

| # | Zincir Adımı | Uygulama | Dosya | Durum |
|---|-------------|----------|-------|-------|
| 1 | **Snapshot** girişi | `GenerateBriefAsync(snapshot, request)` | [ExecutiveBriefGenerator.cs:26-31](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/ExecutiveBriefGenerator.cs#L26-L31) | 🟢 |
| 2 | **Rule Evaluation** | `_ruleEngine.EvaluateAsync(snapshot, ruleRequest)` | [ExecutiveBriefGenerator.cs:37-38](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/ExecutiveBriefGenerator.cs#L37-L38) | 🟢 |
| 3 | **Subject Extraction** | `BuildSubjects(snapshot)` — Org/WS/Domain/Module/Feature/Capability | [DecisionRuleEngine.cs:63-181](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L63-L181) | 🟢 |
| 4 | **Condition Evaluation** | `EvaluateRuleOnSubject()` — TriggeredConditions + RejectedConditions | [DecisionRuleEngine.cs:184-308](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L184-L308) | 🟢 |
| 5 | **Decision Proposal** | `ProposedDecision` üretilir, DecisionId/TraceId/RuleId bağlanır | [DecisionRuleEngine.cs:248-298](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L248-L298) | 🟡 |
| 6 | **Priority Enrichment** | `_priorityEnricher.EnrichAsync()` → `_priorityEngine.ScoreAsync()` | [DecisionPriorityEnricher.cs:35-46](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionPriorityEnricher.cs#L35-L46) | 🟢 |
| 7 | **Recommended Actions** | Template'ten üretilir, ActionId atanır | [DecisionRuleEngine.cs:254-273](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L254-L273) | 🟡 |
| 8 | **Executive Brief** | Aggregated brief + ContentHash | [ExecutiveBriefGenerator.cs:157-185](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/ExecutiveBriefGenerator.cs#L157-L185) | 🟢 |

---

## 2. Acceptance Criteria — Alan Bazlı Doğrulama

Her `DecisionContract` aşağıdaki alanlara sahip olmalıdır:

| # | Alan | Tipi | Dolduruluyor mu? | Detay | Durum |
|---|------|------|-------------------|-------|-------|
| 1 | `DecisionId` | `CanonicalId` | ✅ | `DECISION-{RuleId}-{SubjectId}` formatında deterministik üretilir | 🟢 |
| 2 | `Category` | `DecisionCategory` | ✅ | Rule tanımından alınır (`rule.Category`) | 🟢 |
| 3 | `Severity` | `DecisionSeverity` | ✅ | Rule tanımından alınır (`rule.DefaultSeverity`) | 🟢 |
| 4 | `PriorityScore` | `int?` | ⚠️ | **Rule Engine `null` üretir** (L287). Priority Enricher sonradan doldurur. Enrichment öncesi tüketilirse boş kalır | 🟡 |
| 5 | `Confidence` | `double` | ⚠️ | Rule Engine sabit `1.0` verir (L288). Enrichment sonrası güncellenir ama sabit kalabilir | 🟡 |
| 6 | `Owner` | `List<DecisionOwnerReference>` | ❌ | **Boş liste** — `new List<DecisionOwnerReference>()` (L292). **Owner hiçbir zaman atanmıyor** | 🔴 |
| 7 | `Persona` | `PersonaVisibility[]` | ✅ | Rule tanımındaki `PersonaVisibility` aktarılır | 🟢 |
| 8 | `Evidence[]` | `DecisionEvidenceReference[]` | ❌ | **Boş liste** — `evidenceInputs` hiçbir zaman populate edilmiyor (L293). Evidence yalnızca Trace'te `StatusInputs` olarak geçiyor | 🔴 |
| 9 | `RuleId` | `CanonicalId` | ✅ | `rule.RuleId` doğrudan aktarılır | 🟢 |
| 10 | `RuleVersion` | `string` | ✅ | `rule.RuleVersion` Trace'te mevcut | 🟢 |
| 11 | `DecisionTrace` | `DecisionTraceContract` | ✅ | Tam trace üretilir: TriggeredConditions, RejectedConditions, SnapshotId, CorrelationId, DeterminismHash | 🟢 |
| 12 | `RecommendedAction[]` | `RecommendedActionContract[]` | ⚠️ | Template'ten üretilir ama `Owner` alanı **null**, `Description` jenerik | 🟡 |
| 13 | `GeneratedAt` | `DateTime` | ✅ | `evalTime` olarak atanır | 🟢 |

---

## 3. Explainability Test

**Senaryo:** Founder soruyor: *"Neden bu karar Critical?"*

### Mevcut Yanıt Yeteneği

| Soru | Kaynak | Cevap Verilebiliyor mu? |
|------|--------|------------------------|
| Hangi Rule tetikledi? | `DecisionContract.RuleId` + `Trace.RuleId` | ✅ |
| Rule versiyonu nedir? | `Trace.RuleVersion` | ✅ |
| Hangi koşullar tetiklendi? | `Trace.TriggeredConditions[]` | ✅ |
| Hangi koşullar reddedildi? | `Trace.RejectedConditions[]` | ✅ |
| Priority Score nasıl hesaplandı? | `Trace.PriorityBreakdown.Explanation` | ✅ (enrichment sonrası) |
| Evidence nedir? | `Decision.Evidence[]` | ❌ **Boş — kanıt bağlanmıyor** |
| Kimin sorumluluğunda? | `Decision.Owners[]` | ❌ **Boş — owner atanmıyor** |
| Ne yapılmalı? | `Decision.RecommendedActions[]` | ⚠️ Var ama jenerik |

### Explainability Verdict

Founder'a Rule + Condition + Priority açıklanabiliyor ama **Evidence ve Owner gösterilemiyor**.

**Durum:** 🟡 Accepted with Observation

---

## 4. Determinism Test

### Test Edilen Noktalar

| # | Test | Kaynak | Deterministik mi? | Durum |
|---|------|--------|-------------------|-------|
| 1 | DecisionId üretimi | `DECISION-{RuleId}-{SubjectId}` | ✅ Aynı input → aynı ID | 🟢 |
| 2 | TraceId üretimi | `TRACE-{RuleId}-{SubjectId}` | ✅ Deterministik | 🟢 |
| 3 | Condition evaluation | `EvaluateConditionOperator()` | ✅ Saf fonksiyon | 🟢 |
| 4 | Rule ordering | `.OrderBy(RuleId).ThenBy(SubjectCanonicalId)` | ✅ Stable sort | 🟢 |
| 5 | DeterminismHash (Rule) | MD5(`ruleId\|version\|subjectId\|status`) | ✅ | 🟢 |
| 6 | DeterminismHash (Priority) | MD5(`decisionId\|score\|confidence\|formulaVersion`) | ✅ | 🟢 |
| 7 | ContentHash (Brief) | SHA256(summary + counts + decisions) | ✅ | 🟢 |
| 8 | Priority ranking | `OrderByDescending(Score).ThenByDescending(Severity).ThenBy(DecisionId)` | ✅ Tie-break rules deterministik | 🟢 |
| 9 | `DateTime.UtcNow` in Trace | `Trace.EvaluatedAt` = `evalTime` (parametrik) | ✅ Request'ten gelir | 🟢 |
| 10 | `DateTime.UtcNow` in Brief | `GeneratedAt = DateTime.UtcNow` (L161) | ⚠️ **Non-deterministic** — her çalıştırmada farklı | 🟡 |
| 11 | `Guid.NewGuid()` in Trace | `CorrelationId = Guid.NewGuid()` (L282) | ❌ **Non-deterministic** — her çalıştırmada farklı GUID | 🔴 |

### Determinism Verdict

**Karar içeriği** (Decision + Priority + Conditions) deterministik.
**Metadata** (GeneratedAt, CorrelationId) non-deterministic.

**Durum:** 🟡 Accepted with Observation — CorrelationId request'ten geçirilmeli, GeneratedAt fixedClock ile kontrol edilmeli.
