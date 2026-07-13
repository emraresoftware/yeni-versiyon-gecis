# TASK_FAP_004 — Executive Brief Acceptance

## Rol
Sen Emare Platformunun **Chief Architect & Verification Agent**'ısın.
Amacın yeni özellik geliştirmek değildir.
Amacın Executive Brief katmanının Founder için günlük aksiyon listesi olarak çalışıp çalışmadığını doğrulamaktır.

---

## Context
FAP-003 kapsamında Decision Trace Verification başarıyla tamamlandı. Artık her karar deterministik olarak kanıtı (Evidence) ve sorumlusu (Owner) ile üretilebilmektedir.

FAP-004 kapsamında bu kararların Founder/Partner/CEO seviyesinde bir birleşik özet ve aksiyon listesine (**Executive Brief**) dönüştürülmesini doğrulayacağız.

---

## Amacı
Founder'ın **"Bugün ne yapmalıyım?"** sorusuna en fazla 10 maddelik, persona-scope uygulanmış, kanıtlı ve deterministik cevap verilmesini doğrulamak.

---

## Acceptance Criteria

1. **En Fazla 10 Top Priority**: Brief içindeki `TopPriorities` listesi en fazla 10 karar içermelidir.
2. **Stable Ordering**: Kararlar `ExecutiveBriefHelper.SortTopPriorities` ile stable ordering (PriorityScore descending, Severity descending, Confidence descending, Age descending, DecisionId ascending) kurallarına göre sıralanmalıdır.
3. **Count Değerleri**: Brief içindeki metrikler (`CriticalCount`, `HighCount`, `WarningCount`, `BlockedCount`, `ReadyCount`, `OpportunityCount`) karar setinden türetilmelidir.
4. **Filtreleme**: `Expired`, `Resolved` veya `Dismissed` statüsündeki kararlar varsayılan listede yer almamalıdır.
5. **Data Quality & Stale/Missing**: Snapshot içindeki `IsPartial`, `MissingSources` ve `StaleSources` verileri brief'e tam olarak yansıtılmalıdır.
6. **Owner & Evidence**: Her öncelikli karar en az bir owner ve evidence içermeli, FAP-003 düzeltmeleri brief üzerinden de doğrulanabilmelidir.
7. **Unknown Değerler**: Owner veya evidence verisindeki Unknown durumları sıfırlanmamalı, ancak default team'ler veya fallback'ler gerçek ownership kanıtı olarak sunulmamalıdır.
8. **Persona & Scope**: Founder ve Partner için üretilen çıktılar scope açısından farklı olmalıdır (Partner cross-org göremez, Founder tam erişime sahiptir).
9. **Determinism**: Aynı snapshot ve fixed clock ile çalıştırılan tüm brief'ler aynı counts, top priorities ve `ContentHash` değerlerini üretmelidir.
10. **Canlı Doğrulama**: Canlı REST endpoint (`/api/v1/control-tower/brief`) ve UI üzerinden brief veri akışı doğrulanabilmelidir.

---

## Çıktılar
- `FAP_004_EXECUTIVE_BRIEF_REPORT.md`
- `FAP_004_GAP_ANALYSIS.md`
- `FAP_004_ACCEPTANCE_REPORT.md`

---

## Sonuç Formatı
Her madde için:
- 🟢 Accepted
- 🟡 Accepted with Observation
- 🔴 Rejected

---

## Başarı Kriteri
Founder **"Bugün ne yapmalıyım?"** diye sorduğunda Control Tower 5 saniye içinde en öncelikli 10 aksiyonu kanıtları ve sahipleriyle birlikte deterministik olarak listelemelidir.
