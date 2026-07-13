# FAP-003: Gap Analysis Report

**Task:** FAP-003 — Decision Trace Verification
**Agent:** Chief Architect & Verification Agent
**Date:** 2026-07-13

---

## Kritik Boşluklar (Founder Acceptance'ı engelleyen)

### GAP-001: Evidence Hiçbir Zaman Decision'a Bağlanmıyor 🔴

**Konum:** [DecisionRuleEngine.cs:293](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L293)

**Sorun:**
```csharp
// L194: evidenceInputs listesi oluşturuluyor ama hiçbir zaman populate edilmiyor
var evidenceInputs = new List<DecisionEvidenceReference>();
// ...
// L293: Boş liste Decision'a aktarılıyor
Evidence: evidenceInputs,
```

Decision üretilirken `evidenceInputs` listesi oluşturuluyor ama koşul değerlendirmesi sırasında hiçbir Evidence kaydı oluşturulmuyor. Sonuç: **Her Decision'ın Evidence[] alanı boş.**

**Etki:** Founder "Bu karar neye dayanıyor?" diye sorduğunda kanıt gösterilemiyor.

**Düzeltme:**
```csharp
// EvaluateRuleOnSubject içinde, her koşul değerlendirmesinde:
if (evalResult)
{
    evidenceInputs.Add(new DecisionEvidenceReference(
        EvidenceId: $"EVD-{cond.ConditionId}",
        SourceSystem: cond.EvidenceRequirement,
        EvidenceType: "ConditionMatch",
        RedactedReference: $"{cond.SourcePath} {cond.Operator} {cond.ExpectedValue}",
        ObservedAt: evalTime,
        FreshUntil: evalTime.AddHours(1),
        Confidence: 1.0,
        Reason: $"Condition {cond.ConditionId} triggered: actual={actualValue}",
        IsVerified: true
    ));
}
```

---

### GAP-002: Owner Hiçbir Zaman Atanmıyor 🔴

**Konum:** [DecisionRuleEngine.cs:292](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L292)

**Sorun:**
```csharp
Owners: new List<DecisionOwnerReference>(),  // Her zaman boş
```

Rule tanımında veya Subject'te owner bilgisi mevcut olsa bile Decision'a aktarılmıyor.

**Etki:** "Bu kararın sorumlusu kim?" sorusu yanıtsız kalıyor.

**Düzeltme:** Subject'teki scope bilgisinden veya Rule metadata'sından owner çıkarılmalı. İlk adımda Rule'un `Metadata` alanına `"DefaultOwner": "Engineering"` gibi bir değer koyulabilir.

---

## Orta Seviye Boşluklar

### GAP-003: PriorityScore Rule Engine Çıkışında null 🟡

**Konum:** [DecisionRuleEngine.cs:287](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L287)

**Sorun:**
```csharp
null, // Priority score remains null in this subtask.
```

Priority score yalnızca `DecisionPriorityEnricher` çalıştığında dolduruluyor. Eğer enrichment atlanırsa (örn. doğrudan RuleEngine sonucu tüketilirse), PriorityScore null kalır.

**Etki:** Enrichment pipeline'ı zorunlu bağımlılık. Tek başına Rule Engine çıktısı incomplete.

**Düzeltme:** Bu kasıtlı bir tasarım kararı. Ama **PriorityBreakdown.Explanation**'da bunu açıkça belirtmek gerekiyor: "Priority score will be computed during enrichment phase."

---

### GAP-004: Confidence Sabit 1.0 🟡

**Konum:** [DecisionRuleEngine.cs:288](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L288)

**Sorun:** Rule Engine her zaman `Confidence: 1.0` üretiyor. Gerçek confidence hesaplaması yalnızca PriorityEngine'de (`IEvidenceConfidenceResolver`) yapılıyor.

**Etki:** Enrichment öncesi tüketilirse yanıltıcı güven skoru.

**Düzeltme:** GAP-003 ile aynı — enrichment pipeline'ın zorunluluğu dokümante edilmeli.

---

### GAP-005: RecommendedAction Description'ları Jenerik 🟡

**Konum:** [DecisionRuleEngine.cs:256-273](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L256-L273)

**Sorun:**
```csharp
Title: $"Recommended Action: {actTemplate}",
Description: $"Recommended action template {actTemplate} generated for {subject.Name}",
Owner: null,
```

Action title ve description template'ten üretiliyor ama kontekstsiz. Owner null.

**Düzeltme:** Rule tanımındaki `OutputTemplate` pattern'i (`{SubjectName}`) kullanarak daha anlamlı description üretilebilir.

---

### GAP-006: CorrelationId Non-Deterministic 🟡

**Konum:** [DecisionRuleEngine.cs:282](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L282)

**Sorun:**
```csharp
CorrelationId: Guid.NewGuid(),  // Her çalıştırmada farklı
```

DeterminismHash'te CorrelationId kullanılmıyor (iyi) ama Trace karşılaştırmasında fark yaratıyor.

**Düzeltme:** CorrelationId request'ten geçirilmeli:
```csharp
CorrelationId: request.CorrelationId ?? Guid.NewGuid(),
```

---

## Düşük Seviye Boşluklar

### GAP-007: GetSubjectValue Hardcoded Dönüşler 🟡

**Konum:** [DecisionRuleEngine.cs:311-353](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/DecisionRuleEngine.cs#L311-L353)

**Sorun:**
```csharp
if (sourcePath.Equals("BuildStatus", ...))
    return "Failed"; // Her zaman Failed döner

if (sourcePath.Equals("TestStatus", ...))
    return "Failed"; // Her zaman Failed döner

if (sourcePath.Equals("EvidenceCount", ...))
    return "0"; // Her zaman 0

if (sourcePath.Equals("Ownership.OwnerName", ...))
    return "UNKNOWN"; // Her zaman UNKNOWN
```

Bu hardcoded değerler geliştirme aşamasında placeholder olarak bırakılmış. Canlı snapshot'taki gerçek değerlerle eşleşmiyor.

**Etki:** Rule'lar her zaman tetiklenir (false positive) veya hiç tetiklenmez (false negative).

**Düzeltme:** `ControlTowerSnapshot` içindeki gerçek verilere bağlanmalı (BuildStatus → `snapshot.BuildResults`, TestStatus → `snapshot.TestResults`, vb.)

---

### GAP-008: Catalog Rules 11-30 Dummy 🟡

**Konum:** [InitialRuleCatalog.cs:262-288](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Services/ControlTower/Decisions/InitialRuleCatalog.cs#L262-L288)

**Sorun:** 20 rule `DummyField` koşuluyla üretiliyor, hiçbiri tetiklenemez. Rule sayısını 30'a çıkarmak için eklenmiş placeholder'lar.

**Etki:** Gürültü üretmiyor (tetiklenmiyor) ama misleading `EvaluatedRuleCount`.

**Düzeltme:** Ya kaldır ya da gerçek koşullarla doldur (ikinci aşamada).

---

## Boşluk Özet Matrisi

| GAP | Severity | Alan | FAP Etkisi | Düzeltme Efortu |
|-----|----------|------|------------|-----------------|
| GAP-001 | 🔴 Critical | Evidence | Explainability kırık | ~30 dakika |
| GAP-002 | 🔴 Critical | Owner | Accountability kırık | ~30 dakika |
| GAP-003 | 🟡 Medium | PriorityScore | Pre-enrichment null | Dokümantasyon |
| GAP-004 | 🟡 Medium | Confidence | Pre-enrichment 1.0 | Dokümantasyon |
| GAP-005 | 🟡 Medium | Actions | Jenerik description | ~20 dakika |
| GAP-006 | 🟡 Medium | CorrelationId | Non-deterministic | ~5 dakika |
| GAP-007 | 🟡 Medium | GetSubjectValue | Hardcoded returns | ~1 saat |
| GAP-008 | 🟡 Low | Dummy Rules | Misleading count | ~10 dakika |
