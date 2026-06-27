# 📋 Elyaf Group 2.0 — Full Repository Review Checklist

**Versiyon:** 1.0.0  
**Durum:** Approved  
**Sahip:** Chief Software Architect & Architecture Board  
**Son Güncelleme:** 2026-06-27  
**Kanonik Konum:** `docs/project-management/reviews/FULL_REPO_REVIEW_CHECKLIST.md`  
**İlgili Dokümanlar:** CHIEF_ARCHITECT_INTEGRATION_PROTOCOL.md, MANDATORY_DOCUMENTATION_PROTOCOL.md, SECURITY_AUTHORIZATION.md, EVENT_BUS.md, LOCALIZATION_I18N_STANDARDS.md

---

## Amaç

Bu doküman, private kod reposu (`emaredestek/emaredestek`) Chief Software Architect (ChatGPT) tarafından tam denetime açıldığında yapılacak mimari ve güvenlik denetiminin kapsamını ve kontrol listesini belirler. Denetimlerin standardizasyonu ve hiçbir kritik açığın gözden kaçmaması için bu kontrol listesindeki her madde tek tek doğrulanacaktır.

---

## 🛡️ 1. Repository Security Review
*   [ ] **Secret ve Token Kontrolü:** Kod tabanında (C# sınıfları, Next.js bileşenleri, SQL scriptleri vb.) sabit yazılmış (hardcoded) API anahtarları, şifreler, JWT secret key'ler veya SaaS credential'ları bulunuyor mu?
*   [ ] **Çevre Değişkenleri (Environment Variables):** `.env`, `.env.local`, `appsettings.json` gibi yapılandırma dosyalarında canlı ortama ait hassas bilgiler yer alıyor mu? Bu dosyaların örnek şablonları (`.env.example` vb.) güvenli şekilde yapılandırılmış mı?
*   [ ] **Sunucu ve IP Bilgileri:** Kodda veya dokümanlarda canlı (production) sunucu IP adresleri, SSH anahtarları, sunucu dizin yolları veya veri tabanı connection string'leri açıkça yazılmış mı?
*   [ ] **Git Geçmişi Denetimi:** Git commit geçmişi (`git log`) tarandığında geçmiş commit'lerde kalmış secret sızıntıları mevcut mu?
*   [ ] **Rapor Güvenliği:** Public mimari repoda paylaşılan raporlarda (`TASK_XXX_REPORT.md`, `QA_TASK_XXX.md` vb.) gizliliği ihlal eden veri bulunuyor mu?

---

## 🏛️ 2. Architecture Compliance (Temiz Mimari Uyumluluğu)
*   [ ] **Bağımlılık Yönü (Dependency Direction):** Temiz Mimari katmanları arasındaki bağımlılık yönü içeriden dışarıya doğru mu? (Domain -> Application -> Infrastructure & Persistence -> API)
*   [ ] **DbContext Sızıntısı:** API/Controller katmanı veya Application katmanı doğrudan `DbContext` çağrısı yapıyor mu? (DbContext sadece Persistence katmanında encapsulate edilmelidir).
*   [ ] **Domain Bağımsızlığı:** Domain katmanında, `Infrastructure` veya `Persistence` katmanlarından herhangi bir paket referansı veya dependency injection (DI) bağımlılığı var mı?
*   [ ] **Soyutlama (Abstraction) Uyumu:** Application katmanı, `Infrastructure` veya `Persistence` implementasyon detaylarına (somut sınıflara) doğrudan bağımlı mı? (`IOutboxWriter`, `IEmailService` gibi arayüzler üzerinden haberleşme sağlanıyor mu?)
*   [ ] **UI & Entity Sızıntısı:** Frontend Next.js bileşenleri doğrudan backend domain entity'lerini mi kullanıyor, yoksa DTO/Contract sınıfları üzerinden mi haberleşiyor?
*   [ ] **Shared Kernel Büyüklüğü:** `Shared` veya `Common` katmanı gereğinden fazla büyüyerek diğer modüllerin bağımsızlığını zedeliyor mu?

---

## 🧬 3. DDD / Domain Review
*   [ ] **Aggregate Root Sınırları:** Domain entity'leri içindeki Aggregate Root sınırları doğru belirlenmiş mi? Her aggregate kendi iş kurallarından ve tutarlılığından sorumlu mu?
*   [ ] **Entity Matrix Hizalaması:** Kodlanan entity'ler, `DOMAIN_MODEL.md` dosyasındaki Entity Matrix şemasıyla birebir uyumlu mu?
*   [ ] **Value Object Kullanımı:** `Money`, `Address`, `Quantity` gibi kavramlar veritabanına ve koda Value Object olarak mı yansıtılmış?
*   [ ] **Cross-Context FK İlişkileri:** Farklı bounded context'ler (örn. CRM ve Finance) arasındaki ilişkiler doğrudan EF Core düzeyinde Physical Foreign Key'ler yerine logical FK (Guid Id) üzerinden mi kurulmuş?
*   [ ] **Domain Event İsimleri:** Tetiklenen domain event adları `EVENT_BUS.md` standartlarındaki `EntityAction` (örn. `CrmOpportunityCreated`) formatına uygun mu?

---

## 🚦 4. Multi-Tenant Review
*   [ ] **TenantId Varlığı:** SaaS mimarisinde tenant bazlı olması gereken tüm entity'lerde `TenantId` alanı bulunuyor mu ve `RowVersion` / concurrency token alanları tanımlanmış mı?
*   [ ] **Global Query Filters:** EF Core `DbContext` üzerinde `HasQueryFilter` kullanılarak tenant izolasyonu otomatikleştirilmiş mi?
*   [ ] **Fail-Safe Davranış:** İstek atan kullanıcıda geçerli bir TenantId bulunmadığında sistem güvenli bir şekilde işlemi sonlandırıyor mu (Fail-fast)?
*   [ ] **Tenant Leakage (Veri Sızıntısı):** Ham SQL sorgularında (`FromSqlRaw`) veya tenant filter interceptor'larının devre dışı kaldığı durumlarda çapraz kiracı veri erişimi riski var mı?
*   [ ] **Sistem Entity Ayrımı:** Sistem geneli tablolar (`Tenant`, `User`, `Role` vb.) ile tenant-specific tablolar doğru ayrıştırılmış mı?

---

## 🔑 5. Identity & Authorization Review
*   [ ] **JWT Claims Doğruluğu:** Üretilen JWT token'lar içinde `UserId`, `TenantId`, `roles` ve `permissions` claim'leri standartlara uygun taşınıyor mu?
*   [ ] **Password Hashing:** Şifreler `BCrypt` veya güçlü bir PBKDF2 algoritması ile güvenli şekilde hash'leniyor mu? Salt mekanizması doğru çalışıyor mu?
*   [ ] **Permission Sabitleri:** Kodda kullanılan yetki tanımları `SECURITY_AUTHORIZATION.md` dosyasındaki `Module.Resource.Action` standardıyla (örn. `CRM.Proposal.Approve`) uyumlu mu?
*   [ ] **401 vs 403 Ayrımı:** Kimlik doğrulaması başarısız olan istekler (Unauthorized - 401) ile yetkisi yetersiz olan istekler (Forbidden - 403) doğru HTTP durum kodlarıyla mı dönüyor?
*   [ ] **AI Permission Bypass:** AI Ajanlarının ve Copilot mekanizmalarının yetkilendirme bypass etme riski var mı? AI, sistemi çağırdığında tetikleyen kullanıcının yetki sınırlarına tabi tutuluyor mu?

---

## 🗄️ 6. Persistence Review
*   [ ] **EF Configuration Standartları:** Tablo kolon tipleri, uzunluk sınırları ve indeks tanımları EF Core Configuration sınıflarında (`IEntityTypeConfiguration<T>`) açıkça belirtilmiş mi?
*   [ ] **PostgreSQL Uyumu:** Kod PostgreSQL'e özgü veri tipleri (örn. `timestamptz`, `jsonb`) ile uyumlu mu? `DateTimeKind.Utc` kuralı tüm tarih alanlarında uygulanmış mı?
*   [ ] **SQLite vs PostgreSQL Tutarlılığı:** InMemory/SQLite test sağlayıcılarının PostgreSQL'e özgü yapıları (örn. `xmin`, JSONB kolonları) desteklememesinden kaynaklanan test yanılgıları giderilmiş mi?
*   [ ] **Concurrency Kontrolü:** Concurrency kontrolleri EF Core tarafında `RowVersion` veya PostgreSQL `xmin` token mekanizmalarıyla doğru kurgulanmış mı?
*   [ ] **Soft Delete:** Entity'ler silindiğinde `IsDeleted = true`, `DeletedAt` ve `DeletedBy` alanları otomatik güncelleniyor mu?
*   [ ] **Audit Interceptor:** `CreatedBy`, `CreatedAt`, `UpdatedBy` ve `UpdatedAt` alanları EF Core Interceptor katmanında otomatik dolduruluyor mu?
*   [ ] **Migration Stratejisi:** Yeni tablolar ve kolon değişiklikleri için migration dosyaları ve DB update betikleri sürüm kontrollü olarak hazır mı?

---

## ⚡ 7. Event Bus & Outbox Review
*   [ ] **Dışarıya Doğrudan Publish Yasağı:** Domain event'ler dış sistemlere (RabbitMQ, Kafka vb.) veya harici broker'lara doğrudan publish ediliyor mu? (Outbox aşaması kesinlikle atlanmamalıdır).
*   [ ] **OutboxMessage Entity:** `OutboxMessage` tablosunda `tenantId` ve `correlationId` alanları doğru şekilde atanıyor mu ve payload serialize ediliyor mu?
*   [ ] **SaveChangesAsync -> Outbox Akışı:** DbContext seviyesinde `SaveChangesAsync` çağrıldığında, Aggregate'lerin domain event'leri intercept edilip outbox mesajlarına dönüştürülerek aynı veritabanı transaction'ı içerisinde yazılıyor mu?
*   [ ] **Background Worker:** Outbox mesajlarını okuyup dış sisteme iletecek olan arka plan işçisi (Relay Worker) kod tabanında doğru soyutlanmış mı?
*   [ ] **Transactional Outbox Eksikleri:** Transaction sınırlarının dışında kalan asenkron süreçler ve hata durumlarında tekrar deneme (retry) stratejisi planlanmış mı?

---

## 🔌 8. API Review
*   [ ] **ApiResponse Standardı:** Tüm API endpoint'leri `{ success: boolean, data: T, message: string }` formatındaki ortak `ApiResponse` zarfını kullanıyor mu?
*   [ ] **ProblemDetails ve Exception Middleware:** Uygulama genelinde fırlatılan tüm istisnalar (Exceptions) merkezi bir middleware ile yakalanıp standart `ProblemDetails` formatında dönüyor mu?
*   [ ] **Swagger Güvenliği:** API Swagger dökümantasyonu yetkilendirme (Bearer Token) desteği sunuyor mu? Production ortamında swagger kapatılmış mı?
*   [ ] **Health Endpoints:** Uygulama ve veritabanı sağlık durumunu izlemek için `HealthChecks` API uçları tanımlanmış mı?
*   [ ] **Validation Pipeline:** Request DTO'ları FluentValidation ile doğrulanıyor mu ve hatalar API seviyesine otomatik yansıtılıyor mu?
*   [ ] **CancellationToken Kullanımı:** API Controller metotlarından veritabanı sorgularına kadar tüm asenkron operasyonlarda `CancellationToken` taşınıyor mu?

---

## 🧪 9. Testing Review
*   [ ] **Unit Tests:** Domain katmanındaki iş kuralları ve value object'ler unit testler ile kapsanmış mı?
*   [ ] **Integration Tests:** Veritabanı okuma/yazma, EF Core konfigürasyonları ve interceptor akışları entegrasyon testleriyle doğrulanmış mı?
*   [ ] **API / Endpoint Tests:** Controller katmanı, JWT auth ve yetki kısıtlamaları API testleriyle kapsanmış mı?
*   [ ] **Negative Tests:** Hatalı girdiler, geçersiz token'lar ve yetkisiz erişimler için negatif test senaryoları mevcut mu?
*   [ ] **Tenant Isolation Tests:** Bir tenant'ın verisine başka bir tenant kimliğiyle erişim denemeleri yapılıp engellendiği test edilmiş mi?
*   [ ] **Auth & Event/Outbox Tests:** JWT üreteci, Outbox yazıcı ve Domain Event Dispatcher akışları testler ile güvenceye alınmış mı?
*   [ ] **Gerçekçi Davranış Doğrulaması:** Testlerdeki mock (NSubstitute vb.) kullanımı aşırıya kaçarak gerçek iş mantığının test edilmesini engelliyor mu?

---

## 👁️ 10. Observability Review
*   [ ] **Logging Standardı:** Loglama altyapısı (Serilog vb.) doğru kurgulanmış mı? Log formatı structured (JSON) mı?
*   [ ] **CorrelationId Takibi:** HTTP isteklerinden Event Bus ve arka plan işlerine kadar tüm akışta tek bir `CorrelationId` taşınıp loglara basılıyor mu?
*   [ ] **OpenTelemetry Planı:** Gelecekteki APM (Application Performance Monitoring) entegrasyonu için OpenTelemetry metrik ve trace altyapısı hazır mı?
*   [ ] **Audit vs Operational Logs:** Güvenlik/Denetim logları ile teknik operasyon logları veritabanında veya log sunucusunda doğru ayrıştırılmış mı?

---

## 🌐 11. Localization / i18n Review
*   [ ] **Hardcoded Metinler:** Frontend tarafında dil dosyalarına çıkarılmamış sabit Türkçe veya İngilizce arayüz metinleri bulunuyor mu?
*   [ ] **Çeviri Anahtar Standardı:** Dil anahtarları `common.save` gibi kategorize ve küçük harf camelCase standartlarına uygun mu?
*   [ ] **Kilitli Dil Paketleri:** `tr-TR`, `en-US`, `de-DE` ve `ar-SA` dil dosyaları eksiksiz oluşturulmuş mu?
*   [ ] **Arapça RTL Yerleşimi:** Arapça dil seçeneğinde `dir="rtl"` özniteliğinin dinamik eklenmesi ve mantıksal CSS özellikleri (`margin-inline-start` vb.) uygulanmış mı?
*   [ ] **AI Copilot Dil Hiyerarşisi:** AI Copilot veya Grok API'leri yanıt dönerken sırasıyla; 1. Aktif Kullanıcı Dili, 2. Tenant Dili, 3. Accept-Language hiyerarşisine uyuyor mu?

---

## 🏰 12. Control Tower Scope Alignment
*   [ ] **Yol Haritası Uyumu:** Mevcut kod geliştirmeleri `CONTROL_TOWER_FINAL_SCOPE.md` dokümanındaki 16 Control Tower hedefiyle uyumlu mu?
*   [ ] **Backend Boşluk Analizi:** 16 Control Tower ekranı için gerekli olan veritabanı tabloları ve API uçlarındaki eksikler kod seviyesinde listelenmiş mi?
*   [ ] **KPI - API Bağlantısı:** Arayüzdeki KPI kartlarının besleneceği backend metrik ve aggregation servisleri tanımlanmış mı?
*   [ ] **Traceability:** Gereksinimler ile kodlanmış servisler/entity'ler arasında izlenebilirlik matrisi kurgulanmış mı?

---

## 🛠️ 13. CI/CD & DevOps Review
*   [ ] **GitHub Actions / Pipeline:** Kod pushlandığında otomatik derleme (build) ve testleri çalıştıran CI pipeline tanımları mevcut mu?
*   [ ] **Docker Compose:** Geliştiricilerin yerelde hızlıca ayağa kalkabilmesi için PostgreSQL, Redis ve diğer bağımlılıkları barındıran `compose.dev.yml` dosyası güncel mi?
*   [ ] **Dependabot / Güvenlik Taramaları:** Bağımlılıkların güncelliğini ve güvenlik açıklarını (CVE) denetleyen araçlar aktif mi?
*   [ ] **Branch Protection:** `main` veya `gece-otonom` branch'leri için doğrudan push yasağı ve pull request onay zorunluluğu gibi branch koruma kuralları planlanmış mı?

---

## 📝 14. Technical Debt & Risk Review
*   [ ] **TECHNICAL_DEBT.md Güncelliği:** Bilinçli olarak ertelenen veya refactor edilmesi gereken teknik borçlar güncel olarak listelenmiş mi?
*   [ ] **RISK_REGISTER.md Güncelliği:** Projedeki mimari, takvimsel veya operasyonel riskler kayıt altında mı?
*   [ ] **Blocker Kontrolü:** Bir sonraki geliştirme sprintine (Sprint 2) geçişi engelleyen kritik mimari eksikler bulunuyor mu?

---

## 📄 15. Review Output Format (Denetim Çıktı Standardı)

Chief Software Architect (ChatGPT) tarafından yapılan tam denetim (review) sonucunda aşağıdaki şablona sahip rapor oluşturulup public mimari repoya eklenecektir:

**Dosya Yolu:** `docs/project-management/architect/FULL_REPO_ARCHITECT_REVIEW.md`

### Rapor Şablonu:
```markdown
# 🏛️ Full Repository Architect Review

## 📊 Overall Score: [X / 100]

## 🚨 Critical Blockers (Sprint 2'ye geçmeden önce Çözülmesi Zorunlu Hatalar)
*   ...

## 🔴 High Priority Issues (Yüksek Öncelikli Sorunlar)
*   ...

## 🟡 Medium Priority Issues (Orta Öncelikli Sorunlar)
*   ...

## 📦 Accepted Technical Debt (Kabul Edilen Teknik Borçlar)
*   ...

## 🚦 Sprint 2 Readiness Status
*   [ ] READY / [ ] CONDITIONAL READY / [ ] NOT READY

## 🏁 Recommended Next Tasks
1.  ...

## ⚖️ Final Verdict
*   **PASS** | **CONDITIONAL PASS** | **FAIL**
```

---

*Bu doküman Chief Architect'in yapacağı tam kod denetiminin sınırlarını ve kapsamını belirler. Güncellemeler Architecture Board onayı ile yapılır.*
