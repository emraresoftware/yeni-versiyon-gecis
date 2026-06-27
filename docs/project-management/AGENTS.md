# EMARE BOS — WORKSPACE CUSTOMIZATION & RULES

###############################
MANDATORY PRE-FLIGHT CHECK
###############################

Bu repository'de kod üretmeden önce aşağıdaki dosyaları okumak ZORUNLUDUR.

1. AGENTS.md
2. ANAYASA.md
3. SECURITY_AUTHORIZATION.md
4. DOMAIN_MODEL.md
5. EVENT_BUS.md

Bu dosyalar okunmadan kod üretmek yasaktır.

Kod üretmeden önce:

PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

şeklinde doğrulama yapılmalıdır.

---

## ARTICLE 1

No AI agent is allowed to generate code before reading AGENTS.md.

Violation of this rule invalidates the task.

---

Bu dosya, bu repoda çalışan tüm AI ajanları (geliştirici, test, QA ajanları vb.) için bağlayıcı kuralları barındırır. Her ajan işlem yapmadan önce bu kuralları eksiksiz incelemek ve uymak zorundadır.


---

# EMARE BOS — DUAL REPOSITORY MODEL PROTOCOL v1.2

## 🔒 1. Çift Repository Yapısı ve Görev Paylaşımı

Sistemde iki farklı repository ve bunlara ait kesin sınırlarla çizilmiş görev tanımları bulunur:

### 🔒 Repository 1 (Private): `emaredestek/emaredestek`
* **İçerik:** Sadece Kod, Testler, Deployment, Migration, Konfigürasyon, Docker ve CI/CD dosyaları.
* **Erişim:** Bu repository kesinlikle **Private (Gizli)** olarak kalacaktır. Herhangi bir public erişime açılmayacaktır.

### 🌍 Repository 2 (Public): `emraresoftware/yeni-versiyon-gecis`
* **İçerik:** Sadece Raporlar ve Mimari belgeler.
* **Erişim:** Bu repository **Public (Açık)** konumda olup, ChatGPT Chief Architect (ve diğer denetim birimleri) tarafından okunacaktır.
* **YASAK:** Bu depoya kesinlikle **KOD EKLENMEYECEKTİR.**
* **Her Task Sonunda Zorunlu Eklenecek Belgeler:**
  * `docs/project-management/reports/TASK_XXX_REPORT.md` (Geliştirici görev raporu)
  * `docs/project-management/qa/QA_TASK_XXX.md` (QA kalite raporu)
  * `docs/project-management/architect/ARCHITECT_REVIEW_TASK_XXX.md` (Chief Architect inceleme raporu)
* **İzin Verilen Diğer Dosya Tipleri:**
  * `SPRINT_X.md` (Sprint durum güncellemesi)
  * `RISK_REGISTER.md` (Risk kayıt defteri)
  * `TECHNICAL_DEBT.md` (Teknik borç defteri)
  * `daily/YYYY-MM-DD.md` (Günlük log)

---

## 🛠️ 2. Görev Sonu Çalışma Akışı (Ajan Sorumluluğu)

Bir görev (Task) bittikten sonra süreç sırasıyla şu şekilde işler:

1. **Agent 1 (Geliştirici Ajan):** Kod/test değişikliklerini tamamlar ve `docs/project-management/reports/TASK_XXX_REPORT.md` raporunu yazar.
2. **Agent 2 (QA Ajanı):** Kalite denetimini yapar ve `docs/project-management/qa/QA_TASK_XXX.md` raporunu yazar.
3. **Chief Software Architect (ChatGPT):** Değerlendirmeyi yaparak `docs/project-management/architect/ARCHITECT_REVIEW_TASK_XXX.md` raporunu hazırlar (veya ChatGPT'nin sağladığı içerik doğrudan/birebir buraya kaydedilir). Agent 1 ve Agent 2 bu dosyayı kendileri dolduramaz, sadece beklenen çıktı olarak referans gösterirler.
4. **Adım (Private Repo):** Tüm kod ve rapor değişikliklerini `emaredestek/emaredestek` private reposuna commit edin ve pushlayın.
5. **Adım (Kopyalama):** `docs/project-management/` dizini altındaki rapor dosyalarını `/Users/emre/yeni-versiyon-gecis/docs/project-management/` dizinine kopyalayın.
6. **Adım (Public Repo):** Raporları `emraresoftware/yeni-versiyon-gecis` public reposuna commit edin ve pushlayın.
7. **Adım (Raporlama):** ChatGPT'ye **sadece** public repo linkini, branch ismini ve tamamlanan task numarasını verin.

---

## 🛡️ 3. Güvenlik ve Hassas Veri Sınırı

Public raporlarda veya dokümanlarda kesinlikle aşağıdaki hassas veriler yer alamaz:
* Bağlantı dizgileri (Connection Strings)
* API Anahtarları, Token'lar ve Parolalar (Secrets)
* IP Adresleri ve Sunucu Alan Adları (Hostnames)
* Gerçek müşteri verileri veya ticari olarak kritik özel iş mantığı (Proprietary business logic)
* Kodun tamamı (Gerekirse sadece mimari yapıyı gösteren çok kısa kod örnekleri veya UML şemaları eklenebilir).

---

# AGENT 1 Sorumlulukları

Her Task sonunda oluştur:
`docs/project-management/reports/TASK_XXX_REPORT.md`

Format:
```md
# Task XXX Report

## Objective

## Scope

## Files Created

## Files Modified

## Architecture Decisions

## Dependencies Added

## Build Result

## Test Result

## Performance Notes

## Security Notes

## Technical Debt

## Risks

## Known Limitations

## Breaking Changes

## Next Recommended Task
```

Ayrıca `docs/project-management/sprints/SPRINT_X.md` dosyasını güncelleyin ve ilerleme yüzdesini güncel yazın.

---

# AGENT 2 Sorumlulukları

Kod değiştirmeyin, kod commit etmeyin. Sadece kalite raporu üretin.
Her Task sonunda oluştur:
`docs/project-management/qa/QA_TASK_XXX.md`

Format:
```md
# QA Review

## Build

## Tests

## Clean Architecture

## DDD Compliance

## Security

## Performance

## Persistence

## API

## Test Coverage

## Critical Issues

## Suggestions

## Final Verdict

PASS | CONDITIONAL PASS | FAIL
```

---

# Risk Yönetimi
Eğer yeni risk oluştuysa güncelle: `docs/project-management/risks/RISK_REGISTER.md`

Format:
| Id | Risk | Severity | Status | Owner |
| -- | ---- | -------- | ------ | ----- |

Severity: Critical | High | Medium | Low

---

# Technical Debt
Eğer bilinçli ertelenen geliştirme varsa güncelle: `docs/project-management/debt/TECHNICAL_DEBT.md`

Format:
| Id | Debt | Reason | Planned Sprint |
| -- | ---- | ------ | -------------- |

---

# Daily Log
Her çalışma gününün sonunda güncelle: `docs/project-management/daily/YYYY-MM-DD.md`

İçerik:
* Bugün yapılan işler
* Tamamlanan tasklar
* Açılan riskler
* Alınan kararlar
(Hassas veri yazmayın.)

---

# Tamamlanma Kriteri (Definition of Done)

Bir Task aşağıdaki maddelerin TAMAMI sağlanmadan tamamlandı kabul edilmez.
* Kod yazıldı, Build başarılı, Testler başarılı.
* Task Report (`TASK_XXX_REPORT.md`) Agent 1 tarafından oluşturuldu ve public depoya aktarıldı.
* QA Report (`QA_TASK_XXX.md`) Agent 2 tarafından oluşturuldu ve public depoya aktarıldı.
* Chief Architect Review Raporu (`ARCHITECT_REVIEW_TASK_XXX.md`) Chief Architect (ChatGPT) tarafından hazırlanarak public depoya eklenmiş/aktarılmış olmalıdır (Agent 1 ve Agent 2 bu dosyayı kendileri dolduramaz).
* Sprint dosyası güncellendi.
* Risk Register & Technical Debt güncellendi (gerekliyse).
* Daily Log güncellendi.
* Raporlar public repository'ye push edildi.
* Chief Architect Review (ChatGPT) onaylandı.

Yeni Task ancak Chief Architect Review tamamlandıktan sonra başlatılacaktır.
Bu kural tüm ekip için zorunludur.

