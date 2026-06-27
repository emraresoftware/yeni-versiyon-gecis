# EMARE BOS — WORKSPACE CUSTOMIZATION & RULES

Bu dosya, bu repoda çalışan tüm AI ajanları (geliştirici, test, QA ajanları vb.) için bağlayıcı kuralları barındırır. Her ajan işlem yapmadan önce bu kuralları eksiksiz incelemek ve uymak zorundadır.

---

# EMARE BOS — DUAL REPOSITORY MODEL PROTOCOL v1.1

## 🔒 1. Çift Repository Yapısı ve Görev Paylaşımı

Sistemde iki farklı repository ve bunlara ait kesin sınırlarla çizilmiş görev tanımları bulunur:

### 🔒 Repository 1 (Private): `emaredestek/emaredestek`
* **İçerik:** Sadece Kod, Testler, Deployment, Migration, Konfigürasyon, Docker ve CI/CD dosyaları.
* **Erişim:** Bu repository kesinlikle **Private (Gizli)** olarak kalacaktır. Herhangi bir public erişime açılmayacaktır.

### 🌍 Repository 2 (Public): `emraresoftware/yeni-versiyon-gecis`
* **İçerik:** Sadece Raporlar ve Mimari belgeler.
* **Erişim:** Bu repository **Public (Açık)** konumda olup, ChatGPT Chief Architect (ve diğer denetim birimleri) tarafından okunacaktır.
* **YASAK:** Bu depoya kesinlikle **KOD EKLENMEYECEKTİR.**
* **İzin Verilen Dosya Tipleri:**
  * `TASK_XXX_REPORT.md` (Geliştirici görev raporu)
  * `QA_TASK_XXX.md` (QA kalite raporu)
  * `SPRINT_X.md` (Sprint durum güncellemesi)
  * `RISK_REGISTER.md` (Risk kayıt defteri)
  * `TECHNICAL_DEBT.md` (Teknik borç defteri)
  * `daily/YYYY-MM-DD.md` (Günlük log)
  * `architect/ARCHITECT_REVIEW_TASK_XXX.md` (Chief Architect inceleme raporu)

---

## 🛠️ 2. Görev Sonu Çalışma Akışı (Ajan Sorumluluğu)

Bir görev (Task) bittikten sonra ajan sırasıyla şu adımları izlemek zorundadır:

1. **Adım (Private Repo):** Kod, test ve yapılandırma değişikliklerini `emaredestek/emaredestek` private reposuna commit edin ve pushlayın.
2. **Adım (Kopyalama):** `docs/project-management/` dizini altındaki rapor dosyalarını `/Users/emre/yeni-versiyon-gecis/docs/project-management/` dizinine kopyalayın.
3. **Adım (Public Repo):** Raporları `emraresoftware/yeni-versiyon-gecis` public reposuna commit edin ve pushlayın.
4. **Adım (Raporlama):** ChatGPT'ye **sadece** public repo linkini, branch ismini ve tamamlanan task numarasını verin.

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
* Task Report oluşturuldu ve public depoya aktarıldı.
* QA Report oluşturuldu ve public depoya aktarıldı.
* Sprint dosyası güncellendi.
* Risk Register & Technical Debt güncellendi (gerekliyse).
* Daily Log güncellendi.
* Raporlar public repository'ye push edildi.
* Chief Architect Review (ChatGPT) onaylandı.

Yeni Task ancak Chief Architect Review tamamlandıktan sonra başlatılacaktır.
Bu kural tüm ekip için zorunludur.

