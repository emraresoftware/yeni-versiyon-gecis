# EMARE BOS — Mandatory Documentation Protocol v1.0

**Durum:** Zorunlu proje standardı — Agent 1, Agent 2, Architect ve tüm ekip  
**Kanonik konum:** `docs/project-management/MANDATORY_DOCUMENTATION_PROTOCOL.md`  
**Sohbet geçmişi referans değildir.** Repository teknik hafızadır.

---

## Amaç

Bu repository yalnızca kaynak kod deposu değildir. Aynı zamanda projenin:

- Teknik hafızası
- Mimari hafızası
- QA hafızası
- Sprint geçmişi
- Risk yönetimi
- Technical Debt yönetimi

olarak kullanılır.

**Her görev sonunda** aşağıdaki dokümanların oluşturulması **ZORUNLUDUR**.  
Görev, bu dosyalar repository'ye commit edilmeden **tamamlandı kabul edilmez**.

---

## Repository yapısı

```text
docs/project-management/
├── MANDATORY_DOCUMENTATION_PROTOCOL.md   ← bu dosya
├── DEVELOPMENT_PROTOCOL.md
├── reports/          ← Agent 1: TASK_XXX_REPORT.md
├── qa/               ← Agent 2: QA_TASK_XXX.md
├── architect/        ← Chief Architect ONLY: ARCHITECT_REVIEW_TASK_XXX.md
├── risks/            ← RISK_REGISTER.md
├── debt/             ← TECHNICAL_DEBT.md
├── sprints/          ← SPRINT_N.md
├── tasks/            ← task tanımları / backlog (opsiyonel)
└── daily/            ← YYYY-MM-DD.md
```

---

## Task yaşam döngüsü

```text
1. Kod              (Agent 1)
2. Build + Test     (Agent 1)
3. Task Report      (Agent 1)  → reports/TASK_XXX_REPORT.md
4. QA Report        (Agent 2)  → qa/QA_TASK_XXX.md
5. Architect Review (Chief Software Architect / ChatGPT ONLY) → architect/ARCHITECT_REVIEW_TASK_XXX.md
6. Commit + push    (private kod + public raporlar)
7. Sonraki Task     (Architect onayı sonrası)
```

**Architect Review tamamlanmadan sonraki Task başlatılamaz.**

> **Önemli:** `ARCHITECT_REVIEW_TASK_XXX.md` dosyası **zorunludur**, ancak içeriğini **Agent 1 veya Agent 2 yazamaz**. Yalnızca Chief Software Architect (ChatGPT) hazırlar; koordinatör verilen metni **birebir** public mimari repoya ekler. Agent 1/2 bu dosyayı yalnızca **beklenen çıktı** olarak referans gösterebilir.

---

## Agent 1 sorumlulukları

Her Task sonunda oluştur:

**Dosya:** `docs/project-management/reports/TASK_XXX_REPORT.md`  
**Şablon:** [`reports/TASK_REPORT_STANDARD.md`](reports/TASK_REPORT_STANDARD.md)

Ayrıca güncelle:

**Dosya:** `docs/project-management/sprints/SPRINT_N.md` — sprint ilerleme yüzdesi

Agent 1 **yapmaz:** QA raporu (Agent 2), **`ARCHITECT_REVIEW_TASK_XXX.md` yazmak/doldurmak** (Chief Architect).

---

## Agent 2 sorumlulukları

- Kod değiştirme
- Kod commit etme
- Sadece kalite raporu ve proje kayıtları

Her Task sonunda oluştur:

**Dosya:** `docs/project-management/qa/QA_TASK_XXX.md`  
**Şablon:** [`qa/QA_REPORT_STANDARD.md`](qa/QA_REPORT_STANDARD.md)

Gerekirse güncelle:

- `risks/RISK_REGISTER.md`
- `debt/TECHNICAL_DEBT.md`
- `daily/YYYY-MM-DD.md`

Agent 2 **yapmaz:** Kod, commit, feature geliştirme, **`ARCHITECT_REVIEW_TASK_XXX.md` yazmak/doldurmak** (Chief Architect).

## Risk yönetimi

Yeni risk oluştuysa güncelle: `docs/project-management/risks/RISK_REGISTER.md`

| Id | Risk | Severity | Status | Owner |
| -- | ---- | -------- | ------ | ----- |

**Severity:** Critical · High · Medium · Low  
**Status:** Open · Mitigated · Resolved

---

## Technical Debt

Bilinçli ertelenen geliştirme varsa güncelle: `docs/project-management/debt/TECHNICAL_DEBT.md`

| Id | Debt | Reason | Planned Sprint |
| -- | ---- | ------ | -------------- |

---

## Daily Log

Her çalışma günü sonunda: `docs/project-management/daily/YYYY-MM-DD.md`

İçerik:

- Bugün yapılan işler
- Tamamlanan tasklar
- Açılan riskler
- Alınan kararlar

**Hassas veri yazma** (şifre, token, tam connection string, kişisel e-posta).

---

## Commit kuralı

Kod commit edilirken zorunlu dokümanlar **aynı commit** içinde eklenir.

Örnek:

```text
feat(platform): implement Identity module

TASK_006_REPORT.md
QA_TASK_006.md
SPRINT_1.md
RISK_REGISTER.md          (gerekliyse)
TECHNICAL_DEBT.md         (gerekliyse)
2026-06-27.md             (daily)
```

---

## Definition of Done (DoD)

Bir Task aşağıdakilerin **TAMAMI** sağlanmadan tamamlandı kabul edilmez:

- [ ] Kod yazıldı
- [ ] Build başarılı
- [ ] Testler başarılı
- [ ] Task Report oluşturuldu (`TASK_XXX_REPORT.md`)
- [ ] QA Report oluşturuldu (`QA_TASK_XXX.md`)
- [ ] Sprint dosyası güncellendi
- [ ] Risk Register güncellendi (gerekliyse)
- [ ] Technical Debt güncellendi (gerekliyse)
- [ ] Daily Log güncellendi
- [ ] **Architect Review tamamlandı** — `architect/ARCHITECT_REVIEW_TASK_XXX.md` **Chief Software Architect (ChatGPT) tarafından** hazırlanmış ve public mimari repoya eklenmiş olmalıdır *(Agent 1 / Agent 2 bu dosyayı dolduramaz)*
- [ ] Tüm dokümanlar ilgili repolara commit/push edildi

---

## Mimari yönetim (Chief Architect)

**Sahip:** Chief Software Architect (ChatGPT) — Agent 1 ve Agent 2 **değil**.

Girdi (repository'den okunur):

- `reports/TASK_XXX_REPORT.md`
- `qa/QA_TASK_XXX.md`

Zorunlu çıktı:

- `architect/ARCHITECT_REVIEW_TASK_XXX.md`

İçerik yalnızca Chief Architect tarafından üretilir veya ChatGPT'nin verdiği metin **değiştirilmeden** public mimari repoya eklenir. Agent 1/2 placeholder, taslak veya özet architect review yazamaz.

**Architect Review tamamlanmadan sonraki Task başlatılmaz.**

---

## İlgili dokümanlar

| Doküman | Açıcı |
|---------|--------|
| [`README.md`](README.md) | Proje yönetimi indeks |
| [`DEVELOPMENT_PROTOCOL.md`](DEVELOPMENT_PROTOCOL.md) | ADD özet |
| [`reports/TASK_REPORT_STANDARD.md`](reports/TASK_REPORT_STANDARD.md) | Agent 1 şablonu |
| [`qa/QA_REPORT_STANDARD.md`](qa/QA_REPORT_STANDARD.md) | Agent 2 şablonu |
| `emare-dashboard/docs/adr/` | Mimari karar kayıtları (ADR) |

---

*v1.1 — 2026-06-27 (Architect Review sahipliği: yalnızca Chief Architect)*
