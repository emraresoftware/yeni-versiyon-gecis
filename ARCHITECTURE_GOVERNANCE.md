# 📚 Architecture Governance

## Amaç

Architecture Governance, Emare Business Operating System (BOS) mimarisinin tutarlılığını, bütünlüğünü, kalitesini ve sürdürülebilirliğini korumak amacıyla kurallar, süreçler, roller ve sorumluluklar tanımlayan merkezi yönetişim dökümanıdır.

Bu döküman;

* Mimari Karar Süreçlerini (ADR Yaşam Döngüsü)
* Teknik Döküman Standartlarını ve Yönetimini
* Sürüm Politikası ve Deprecation Süreçlerini
* Değişiklik Yönetimi ve Onay Mekanizmasını

belirler.

---

# Mimarinin Temel İlkeleri

Emare BOS mimarisi üzerinde yapılacak her türlü değişiklik veya ekleme aşağıdaki temel kurallara bağlı kalmak zorundadır:

1. **Geriye Dönük Uyumluluk (Backward Compatibility):** Mevcut çalışan API, Event veya Veri Modeli yapılarında geriye dönük kırıcı değişiklik (breaking change) yapılamaz. Değişiklik gerekliyse *Deprecation Yaşam Döngüsü* işletilir.
2. **Katman İzolasyonu:** Clean Architecture katman bağımlılık kuralları çiğnenemez. Gevşek bağlı (loose coupling) tasarım esastır.
3. **Tek Doğruluk Kaynağı (Single Source of Truth):** Her iş kuralı, veri alanı veya süreç tanımı yalnızca kendi sahibi olan Bounded Context içerisinde tanımlanmalıdır.

---

# Roller ve Sorumluluklar

Mimari kararların alınması ve denetlenmesi aşağıdaki roller tarafından yürütülür:

### 🏛️ Architecture Board (Mimari Kurul)
* **Tanım:** Kıdemli yazılım mimarları ve teknik liderlerden oluşan karar verici organdır.
* **Görevler:** Yeni ADR'lerin onaylanması, breaking change kararları, genel platform mimarisinin yönlendirilmesi.

### 🤖 AI Code & Architecture Reviewer (AI Denetçi Ajanı)
* **Tanım:** CI/CD pipeline'larında ve geliştirme ortamlarında çalışan statik/dinamik mimari denetleme aracıdır.
* **Görevler:** Kodun Clean Architecture standartlarına, isimlendirme konvansiyonlarına (Ubiquitous Language) ve Tenant izolasyon kurallarına uygunluğunu otomatik denetlemek.

### 👨‍💻 Module Owner (Modül Sorumlusu)
* **Tanım:** İlgili Bounded Context'in iş kurallarından ve implementasyonundan sorumlu kıdemli yazılımcıdır.
* **Görevler:** Modül bazlı mimari değişiklik önerilerini hazırlamak ve test etmek.

---

# Mimari Karar Süreçleri (ADR Yaşam Döngüsü)

Tüm kritik mimari kararlar **ADR (Architecture Decision Records)** dökümanları ile kayıt altına alınır. Bir ADR aşağıdaki aşamalardan geçer:

```text
Draft (Taslak)

↓

Proposed (Önerilen)

↓

Review (Değerlendirme)

↓

Accepted (Kabul) / Rejected (Red)

↓

Deprecated / Superseded (Geçersiz)
```

1. **Draft:** Modül Sorumlusu veya Mimar tarafından fikir dökümante edilir.
2. **Proposed:** Karar, Mimari Kurul'un incelemesine sunulur.
3. **Review:** Kurul ve ilgili teknik ekipler tarafından kararın etkileri tartışılır.
4. **Accepted / Rejected:** Karar ya kabul edilir ya da gerekçeleriyle reddedilir. Kabul edilen kararlar `docs/adr/` altına kaydedilir.
5. **Superseded:** Eğer yeni bir karar eski kararın yerini alırsa, eski karar "Superseded" durumuna getirilir ve yeni ADR'ye link verilir.

---

# Döküman Yönetimi ve Standartları

BOS içerisindeki tüm mimari ve teknik dökümanlar aşağıdaki standart üst bilgi (metadata) şablonunu taşımak zorundadır:

```markdown
# [Döküman Başlığı]

**Title:** [Döküman Başlığı]
**Version:** [X.Y.Z]
**Status:** [Draft | Under Review | Approved | Deprecated]
**Owner:** [Rol veya Bounded Context Sahibi]
**Last Updated:** [YYYY-MM-DD]
**Dependencies:** [Bağımlı Olunan Diğer Dökümanlar]
**Related Documents:** [İlgili Dökümanlar]

---
## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | ...  | ...    | ...         |
```

Herhangi bir teknik döküman güncelleneceği zaman sürüm numarası artırılmalı ve **Change History** tablosuna eklenmelidir.

---

# Sürüm Politikası ve Deprecation Süreci

Platform, SDK'lar ve Plugin Marketplace bileşenleri **Semantic Versioning (SemVer)** kurallarına göre sürümlenir:

```text
Major.Minor.Patch
```

* **Major:** Geriye dönük uyumsuz (kırıcı) değişiklikler.
* **Minor:** Geriye dönük uyumlu yeni özellikler.
* **Patch:** Geriye dönük uyumlu hata düzeltmeleri.

### ⚠️ Deprecation Süreci (Eski Yapıları Kaldırma)
Mevcut bir API, Event veya Veri Alanı kaldırılmak istendiğinde doğrudan silinemez. Şu adımlar izlenir:

1. **Sürüm N (Örn: v2.1.0):** İlgili yapı `[Obsolete]` veya `@deprecated` olarak işaretlenir. Loglama ve dökümantasyonda uyarı verilir. Yerine ne kullanılması gerektiği belirtilir.
2. **Sürüm N+1 (Örn: v2.2.0):** Eski yapı desteklenmeye devam eder ancak kullanımında uyarı verilir.
3. **Sürüm N+2 (Örn: v3.0.0 - Major Sürüm):** Eski yapı tamamen kod tabanından kaldırılır.

---

# Kırıcı Değişiklik (Breaking Change) Yönetimi

Eğer acil bir güvenlik veya performans sebebiyle SemVer deprecation süresi beklenemeyecek bir kırıcı değişiklik yapılması gerekiyorsa:

* Mimari Kurul'un oy birliğiyle onayı gerekir.
* Değişiklikten etkilenecek tüm modül sahiplerine en az 72 saat önce bildirim gönderilir.
* Değişiklik öncesi veri göçü (migration) ve geri alma (rollback) planı hazırlanmalıdır.
* Değişiklik canlıya alınmadan önce Staging ortamında tüm entegrasyon testlerinden başarıyla geçmelidir.

---

# Mimari Uyum Kontrolü (Governance Checklist)

Geliştirilen her yeni özellik veya modül canlıya alınmadan önce aşağıdaki uyum kontrolünden geçer:

* [ ] Yeni veri tabloları ve entity'ler `TenantId` alanını içeriyor mu?
* [ ] Tüm DateTime alanları `DateTimeKind.Utc` olarak tanımlanmış mı?
* [ ] Modüller arası doğrudan bağımlılık (Direct DB Query, Direct Link) yerine Event/API sözleşmesi kullanılmış mı?
* [ ] İş kuralları Domain/Application katmanında mı yazılmış? (Infrastructure veya Controller'a iş kuralı gömülmemiş olmalı)
* [ ] Hata yönetiminde Result Pattern (`Result<T>`) uygulanmış mı?
* [ ] Yeni endpoints API Gateway rate-limit ve yetkilendirme kurallarına tabi mi?
* [ ] Sistem genelinde loglama ve hata takibi için `CorrelationId` aktarımı sağlanmış mı?

---

# Nihai İlke

Architecture Governance, Emare Business Operating System (BOS) mimarisinin anayasasıdır.

Mimaride ve kodda yapılacak her değişiklik bu kurallara tabi olarak denetlenir.

Kurallara uymayan hiçbir geliştirme veya tasarım canlıya alınamaz.
