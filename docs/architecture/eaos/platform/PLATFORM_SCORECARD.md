# 📊 PLATFORM_SCORECARD.md (EAOS Platform Sağlık Karnesi)

Bu doküman, EAOS platformunun genel kalitesini, mimari temizliğini ve operasyonel sağlığını sürekli olarak 0-100 puan aralığında ölçen karne yapısını tanımlar. [OBSERVABILITY_CONSTITUTION.md](../constitutions/OBSERVABILITY_CONSTITUTION.md) belgesine doğrudan bağlıdır.

---

## 1. Puanlama Kategorileri (0 - 100)

| Kategori | Ölçüm Kriteri | Ağırlık |
|---|---|---|
| **Architecture** | Modüler monolit kuralları, gevşek bağlılık, CQRS uyumu. | %15 |
| **Security** | PII maskeleme, SQL Injection koruması, tenant izolasyon filtreleri. | %15 |
| **Performance** | `PERFORMANCE_BUDGET.md` limitlerine uyum oranı. | %15 |
| **Voice** | Sesli asistan gecikme ve kesinti (barge-in) kalitesi. | %15 |
| **AI** | Model bağımsızlık oranı ve uydurma (hallucination) sıklığı. | %10 |
| **UX / UI** | Dashboard hızı, tarayıcı performansı ve arayüz tutarlılığı. | %5 |
| **Monitoring** | Logların structured olma oranı ve metriklerin kapsama yüzdesi. | %5 |
| **DX (Dev Experience)**| Geliştirici başlangıç hızı ve CI/CD kalite kapısı süreleri. | %5 |
| **Maintainability** | Kod karmaşıklık skoru (Cyclomatic Complexity) ve test kapsama oranı. | %10 |

---

## 2. EAOS Platform Health Score (Genel Sağlık Puanı)

Platformun genel sağlık puanı, yukarıdaki kategorilerin ağırlıklı ortalaması alınarak hesaplanır:

$$\text{Health Score} = \sum (\text{Category Score} \times \text{Weight})$$

* **90 - 100:** **EXCELLENT (Yeşil)** - Platform stabil, borçsuz ve hızlı.
* **75 - 89:** **GOOD (Sarı)** - Kabul edilebilir ancak bazı refactoring adımları gerekli.
* **< 75:** **CRITICAL (Kırmızı)** - Geliştirme durdurulmalı, öncelik teknik borçlara verilmelidir.
