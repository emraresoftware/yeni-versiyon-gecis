# CHIEF ARCHITECT INTEGRATION PROTOCOL v1.0

Bu andan itibaren proje geliştirme süreci güncellenmiştir.

ChatGPT (Chief Software Architect) artık projenin resmi teknik mimarıdır.

Bundan sonra görev tamamlandıktan sonra ChatGPT'ye sohbet içerisinde uzun raporlar gönderilmeyecektir.

Bunun yerine bütün teknik hafıza repository içerisinde tutulacaktır.

---

# Repository Kuralları

Kod repository'si artık aşağıdaki bilgilerin tamamını içerecektir.

```text
docs/

project-management/

├── reports/
├── qa/
├── architect/
├── risks/
├── debt/
├── sprints/
├── daily/
└── tasks/
```

Bu klasörler repository'nin zorunlu parçalarıdır.

---

# Her Task Sonunda

Aşağıdaki dosyalar commit edilmeden Task tamamlandı kabul edilmeyecektir.

## Development Report

```
docs/project-management/reports/

TASK_XXX_REPORT.md
```

## QA Report

```
docs/project-management/qa/

QA_TASK_XXX.md
```

## Sprint Güncellemesi

```
docs/project-management/sprints/

SPRINT_X.md
```

## Daily Log

```
docs/project-management/daily/

YYYY-MM-DD.md
```

## Risk Register

Gerekirse güncellenecek.

```
docs/project-management/risks/

RISK_REGISTER.md
```

## Technical Debt

Gerekirse güncellenecek.

```
docs/project-management/debt/

TECHNICAL_DEBT.md
```

## Architect Review (Chief Architect ONLY)

```
docs/project-management/architect/

ARCHITECT_REVIEW_TASK_XXX.md
```

**Zorunlu dosya** — içeriği **yalnızca Chief Software Architect (ChatGPT)** yazar. Agent 1 ve Agent 2 bu dosyayı dolduramaz; koordinatör ChatGPT çıktısını birebir public mimari repoya ekler.

---

# Architect Review Süreci

Task tamamlandıktan sonra koordinatör aşağıdaki işlemi yapacaktır.

1.

Kod commit edilir.

↓

2.

QA tamamlanır.

↓

3.

Repository push edilir.

↓

4.

Koordinatör AI sadece aşağıdaki bilgileri ChatGPT'ye verir.

* Repository Linki

* Branch

* Tamamlanan Task

* İlgili Report dosyaları

↓

5.

ChatGPT repository üzerinden inceleme yapar.

↓

6.

Architect Review hazırlanır → `docs/project-management/architect/ARCHITECT_REVIEW_TASK_XXX.md` *(Chief Architect / ChatGPT — Agent 1 ve Agent 2 yazmaz)*

↓

7.

Sonraki Task ChatGPT tarafından planlanır.

---

# ChatGPT'nin Rolü

ChatGPT aşağıdaki görevleri üstlenecektir.

* Chief Software Architect
* Sprint Planner
* Architecture Reviewer
* Technical Debt Reviewer
* Security Reviewer
* Performance Reviewer
* DDD Reviewer
* Clean Architecture Reviewer

ChatGPT kod yazan ajan değildir.

Kod üretimini denetleyen mimardır.

---

# Architect Review Sonucu

Her Task sonunda ChatGPT aşağıdaki başlıklarla değerlendirme yapacaktır.

* Architecture Score
* Code Quality
* DDD Compliance
* Clean Architecture Compliance
* Security Review
* Performance Review
* Scalability Review
* Technical Debt
* Risk Analysis
* Release Readiness
* Sprint Recommendation
* Next Task

---

# Branch Politikası

Kod geliştirmeleri mevcut geliştirme branch'inde devam eder.

Architect Review hiçbir zaman doğrudan kod değiştirmez.

Mimari öneriler rapor olarak sunulur.

---

# Definition of Done

Bir Task aşağıdaki maddelerin tamamı gerçekleşmeden tamamlandı kabul edilmez.

✓ Kod tamamlandı

✓ Build başarılı

✓ Testler başarılı

✓ Development Report repository'ye eklendi

✓ QA Report repository'ye eklendi

✓ Sprint güncellendi

✓ Daily Log güncellendi

✓ Risk Register güncellendi (gerekiyorsa)

✓ Technical Debt güncellendi (gerekiyorsa)

✓ Repository push edildi

✓ Chief Architect Review alındı — `ARCHITECT_REVIEW_TASK_XXX.md` **Chief Software Architect (ChatGPT) tarafından hazırlanmış** olmalıdır *(Agent 1 / Agent 2 dolduramaz)*

Bundan sonra yeni Task ancak Chief Architect Review tamamlandıktan sonra başlatılacaktır.

Bu kural proje genelinde zorunludur.
