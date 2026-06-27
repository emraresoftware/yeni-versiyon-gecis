# EMARE BOS — Mandatory Documentation Protocol v1.1

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

**Her görev sonunda** aşağıdaki dokümanların oluşturulması ve repository'ye eklenmesi **ZORUNLUDUR**.  
Görev, bu dosyalar repository'ye commit edilip push edilmeden **tamamlandı kabul edilmez**.

---

## Repository yapısı

```text
docs/project-management/
├── MANDATORY_DOCUMENTATION_PROTOCOL.md   ← bu dosya
├── DEVELOPMENT_PROTOCOL.md
├── reports/          ← Agent 1: TASK_XXX_REPORT.md
├── qa/               ← Agent 2: QA_TASK_XXX.md
├── architect/        ← Chief Architect: ARCHITECT_REVIEW_TASK_XXX.md
├── risks/            ← RISK_REGISTER.md
├── debt/             ← TECHNICAL_DEBT.md
├── sprints/          ← SPRINT_N.md
├── tasks/            ← task tanımları / backlog (opsiyonel)
└── daily/            ← YYYY-MM-DD.md
```

---

## Task yaşam döngüsü

```text
1. Kod          (Agent 1)
2. Build
3. Test
4. Task Report  (Agent 1)
5. QA Report    (Agent 2)
6. Architect Review (Chief Architect) -> Rapor üretimi (Agent 1 ve Agent 2 dolduramaz)
7. Commit & Push (kod + tüm zorunlu dokümanlar, review dahil)
8. Sonraki Task (Architect onayı sonrası)
```

**Architect Review tamamlanıp ARCHITECT_REVIEW_TASK_XXX.md Chief Architect tarafından repoya commit edilmeden sonraki Task başlatılamaz.**

---

## Agent 1 sorumlulukları

Her Task sonunda oluştur:

**Dosya:** `docs/project-management/reports/TASK_XXX_REPORT.md`  
**Şablon:** [`reports/TASK_REPORT_STANDARD.md`](reports/TASK_REPORT_STANDARD.md)

Ayrıca güncelle:

**Dosya:** `docs/project-management/sprints/SPRINT_N.md` — sprint ilerleme yüzdesi

Agent 1 **yapmaz:** QA raporu yazmak (Agent 2), kod dışı kalite denetimi.

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

---

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
ARCHITECT_REVIEW_TASK_006.md
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
- [ ] Task Report oluşturuldu (`TASK_XXX_REPORT.md` — Agent 1)
- [ ] QA Report oluşturuldu (`QA_TASK_XXX.md` — Agent 2)
- [ ] Architect Review Raporu oluşturuldu (`ARCHITECT_REVIEW_TASK_XXX.md` — Chief Architect tarafından)
- [ ] Sprint dosyası güncellendi
- [ ] Risk Register güncellendi (gerekliyse)
- [ ] Technical Debt güncellendi (gerekliyse)
- [ ] Daily Log güncellendi
- [ ] Architect Review tamamlandı ve onaylandı
- [ ] Tüm dokümanlar repository'ye commit ve push edildi

---

## Mimari yönetim

Her Task sonrası Chief Software Architect inceler:

- `TASK_XXX_REPORT.md`
- `QA_TASK_XXX.md`

Çıktı: `architect/ARCHITECT_REVIEW_TASK_XXX.md` — **Approved** / **Approved with conditions** / **Rejected** (Sadece Chief Architect tarafından yazılır)

**Architect Review tamamlanıp ARCHITECT_REVIEW_TASK_XXX.md Chief Architect (ChatGPT) tarafından repoya eklenmeden sonraki Task başlatılmaz.** Tüm ekip için zorunludur.

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

*v1.1 — 2026-06-27*
