# 🏰 Architecture Audit Report v1

**Title:** Architecture Audit Report v1  
**Version:** 1.0.0  
**Status:** Approved  
**Owner:** CTO & Chief Software Architect  
**Last Updated:** 2026-07-01  
**Dependencies:** SPRINT_2.md, CONTROL_TOWER_FINAL_SCOPE.md, 00_MASTER_GAP_ANALYSIS.md  
**Related Documents:** AGENTS.md, ANAYASA.md, DOMAIN_MODEL.md, SYSTEM_ARCHITECTURE.md  

---

# 1. Executive Summary

Bu rapor, Emare Workspace (Emare BOS) altyapısının mevcut mimari ve kod olgunluk durumunu teknik, operasyonel ve organizasyonel açılardan analiz etmek amacıyla hazırlanmıştır. Projenin genel durumu; olgun, test edilmiş ve sağlam bir platform çekirdeği ile neredeyse tamamen statik, entegrasyonu yapılmamış mockup arayüzlerden oluşan bir iş katmanı (Elyaf Control Tower) arasındaki derin uçurumu ortaya koymaktadır.

* **Projenin Mevcut Olgunluk Seviyesi:** **%45**
  * **Platform Çekirdeği (Auth, Tenant, RBAC, Core CRM):** %85
  * **Telephony / Voice Bridge (Asterisk + standalone Python):** %70
  * **Elyaf Control Tower İşlevselliği (16 Rol & 150+ KPI):** %15 (Frontend UI %90 mock/statik, Backend veri ve entegrasyon katmanı %0)

---

# 2. Mevcut Varlıklar

Yeniden yazılmaması, korunması ve üzerine inşa edilmesi gereken hazır sistemler:

* **CRM Core Modülü:** `CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal` ve `CrmProposalItem` entity'leri; CQRS handler'ları, akıcı validation kuralları, REST API uç noktaları ve %100 başarılı olan xUnit entegrasyon testleri.
* **Tenant & Dynamic Host Çözümleme:** Çoklu kiracı (multi-tenant) sistem mimarisinde host domain üzerinden dinamik Tenant bulma, caching mekanizması ve SuperAdmin/Reseller bypass kuralları.
* **Email & Background Processing:** SMTP/IMAP altyapısı, `ImapPollerBackgroundService` ile asenkron arka plan e-posta senkronizasyonu ve biletlere (tickets) bağlama akışları.
* **Telephony Standalone Audio Socket Kütüphanesi:** Python tabanlı Asterisk AudioSocket ses köprüsü, Gemini Live API ve Cartesia TTS entegrasyonları.
* **Control Tower UI Statik Arayüzleri:** 16 farklı rolün tüm görsel şablonlarını, kart yerleşimlerini ve mock grafiklerini içeren ~10.000 satırlık Next.js bileşen arayüzü.

---

# 3. Eksikler

Ürünün canlıya geçebilmesi için tamamlanması gereken kritik mimari, kullanıcı arayüzü ve entegrasyon açıkları:

### 3.1 Eksik Mimari
* **KPI Snapshot & Hesaplama Motoru:** 150+ KPI'ın zaman serisi (MTD/YTD) verilerini veritabanında saklayacak `KpiSnapshot` şeması, hesaplama arayüzleri ve bunları tetikleyen zamanlanmış arka plan işleri (Background Workers).
* **Karar Defteri (DecisionLog) & Şirket Sağlık Skoru (CompanyHealthScore):** `DOMAIN_MODEL.md` içinde Aggregate Root olarak tanımlanmış olmalarına rağmen, veritabanı şemaları, migration'ları, CQRS handler'ları ve EF Core konfigürasyonları tamamen eksiktir.

### 3.2 Eksik UI
* **Sol Dikey Navigasyon Menüsü:** PNG mockup'larda tanımlanan ancak Next.js tarafında implemente edilmeyip yerine geçici yatay buton barı kullanılan dikey sol sidebar navigasyonu.
* **Health / Risk Score Dial Widget:** Sağlık skorunu görsel olarak gösteren gauge/dial grafik bileşeni (sadece metin olarak render edilmektedir).
* **Bağsız Buton ve Linkler:** Dashboard'lar üzerinde bulunan ve tıklandığında yalnızca `alert()` simülasyonu çalıştıran 80'den fazla butonun drill-down sayfalarına/modallara bağlanması.

### 3.3 Eksik Backend
* **Dış Sistem Entegrasyon Katmanı (ERP / Sheets):** Üretim verimliliği, sipariş backlog değerleri ve OTD (On-Time Delivery) verilerini canlı çekebilecek ERP / Google Sheets API bağlayıcıları (Connectors).
* **12 Rol için Seed Data API:** Pilot roller (CEO, Sales, Finance, PI) dışındaki 12 rolün dashboard API uç noktaları.

### 3.4 Eksik AI
* **AI Metin Taslak Üretim Motoru:** Arayüzde bulunan 3 farklı tonda (Soft/Balanced/Firm) mesaj taslağı oluşturma ve doğrudan WhatsApp/Email kanallarına basma motoru.
* **Ask Elyaf / RAG Entegrasyonu:** Kurumsal bilgi bankası dokümanlarının yerel LLM / Grok üzerinden sorgulanmasını sağlayan RAG (Retrieval-Augmented Generation) katmanı.

### 3.5 Eksik Güvenlik
* **Rol Bazlı Dashboard Erişim Sınırlandırması:** Şu anda her kullanıcının tüm rolleri (özellikle CEO ve Finance) görebilmesini engelleyecek sayfa düzeyi erişim kontrolü (Route Guards).
* **SuperAdmin Alt Kiracı (Tenant) CRUD Koruması:** Reseller yetki hiyerarşisinde Tenant CRUD yetki sınırlarının netleştirilmesi.

---

# 4. Çakışmalar

Projede karmaşaya neden olan, birleştirilmesi veya güncellenmesi gereken yapılar ve belgeler:

* **Çoklu `AGENTS.md` ve `CLAUDE.md` Dosyaları:** Proje kökünde, `web/` klasöründe, `gemini-live-standalone/` altında ve `.claude/worktrees/` içinde birden fazla talimat dosyası bulunmakta, bu durum yapay zeka ajanlarının çalışma kurallarında kafa karışıklığına ve kural çelişkilerine yol açmaktadır.
* **CRM Kanonik Model Çiftliği:** `docs/CRM_CANONICAL_MODEL.md` ile `Yeni versiyon geçiş/DOMAIN_MODEL.md` dosyalarındaki CRM modelleri birbiriyle örtüşmekte fakat ayrı yerlerde güncellenmektedir.
* **`yeni-versiyon-gecis` vs `Yeni versiyon geçiş` Klasör Çiftliği:** Yerel geliştirme klasörü içindeki isimlendirme farkları ve repolardaki dosya kopyaları sürüm takibini zorlaştırmaktadır.

---

# 5. Workspace Readiness Score

| Kategori | Puan (10) | Gerekçe |
|----------|-----------|---------|
| **Design System** | **8 / 10** | CSS token'ları, primitifler ve tipografi kuralları tanımlı fakat backend temalarıyla bağsız. |
| **Information Architecture** | **7 / 10** | 16 rolün bilgi mimarisi spesifikasyonlarda tam; Next.js tarafında aşırı yüklenmiş durumda. |
| **Navigation** | **4 / 10** | Sol dikey sidebar tamamen eksik, geçici yatay butonlarla geçiş sağlanıyor. |
| **Component Library** | **6 / 10** | Statik dashboard kartları var ama bağımsız, modüler paketler halinde değil, hardcoded. |
| **Theme Engine** | **5 / 10** | Token'lar mevcut ancak light/dark mode geçişleri ve kiracı bazlı CSS yüklemeleri bitirilmemiş. |
| **Widget Engine** | **3 / 10** | Dinamik widget yükleyici, widget registry veya sürükle-bırak motoru yok, hepsi statik grid. |
| **AI Integration** | **3 / 10** | Telephony modülü AI-ready; CRM asistanı, RAG ve e-posta taslak üretimleri tamamen statik stub. |
| **Browser Platform** | **6 / 10** | Next.js build sorunsuz, token yenileme ve retries çalışıyor; state senkronizasyonu eksik. |
| **White Label** | **4 / 10** | Arayüzde hardcoded marka isimleri ve asset bağımlılıkları mevcut, tam soyutlama sağlanmamış. |
| **Security** | **5 / 10** | Impersonation ve JWT yenileme hazır ancak rol bazlı sayfa yetki kontrolleri (guards) zayıf. |

---

# 6. Technical Debt (En Büyük 20 Teknik Borç)

1. **Monolitik Dashboard Sayfası:** `web/src/app/(dashboard)/dashboard/[roleId]/page.tsx` (veya elyafdashboards bileşenleri) içindeki ~10.000 satırlık aşırı yüklü, bölünmemiş Next.js kod tabanı.
2. **Statik mockData Dosyası:** `mockData.ts` içindeki ~3.500 satırlık statik JSON veri yapısı. Değişikliklerde performans ve bellek yükü oluşturmaktadır.
3. **Widget Soyutlama Eksikliği:** Kartların, grafiklerin ve listelerin reusable bileşenler (shared widgets) yerine her panel görünümünde kopyalanarak yazılmış olması.
4. **Olmayan Database Modelleri:** `DecisionLog`, `KpiSnapshot` ve `CompanyHealthScore` tablolarının PostgreSQL veritabanında olmaması.
5. **Eksik KPI Hesaplama Motoru (Analytics Engine):** 150+ KPI metrik formülünün veritabanı düzeyinde hesaplanması yerine arayüze mock veri olarak basılması.
6. **Simüle Edilmiş Butonlar:** `handleAction` içindeki tek satırlık `alert()` çağrısıyla geçiştirilen 80'den fazla kullanıcı aksiyon noktası.
7. **Erişim Kontrol (Guard) Eksikliği:** İstemci tarafında `/control-tower/ceo` gibi kritik rotalara rol kontrolü yapılmaksızın doğrudan URL üzerinden erişilebilmesi.
8. **Çoklu Dil (i18n) Hardcoding:** Bazı metrik kartlarında ve durum mesajlarında Türkçe/İngilizce dil anahtarlarının doğrudan kod içine yazılmış olması.
9. **Farklı Metrik Değerleri (KPI Tutarsızlığı):** CEO ekranındaki OTD değeri ile PI ekranındaki OTD değerinin mock verilerdeki senkronizasyon eksikliğinden dolayı çelişmesi.
10. **Statik Dashboard Tarihi:** Tüm panellerin sağ üst köşesinde "12 May 2024" tarihinin sabitlenmiş olması, gerçek `lastRefreshedAt` değerinin kullanılmaması.
11. **Eksik PDF/Excel Export Servisi:** Frontend tarafında rapor indirme butonlarının backend'de Puppeteer/Dapper Excel export servislerine bağlanmamış olması.
12. **Çoklu `AGENTS.md` Kural Drifti:** Farklı dizinlerdeki ajan kurallarının zamanla birbirinden sapması (drift) ve çelişmesi.
13. **Hardcoded Tenant Rotaları:** URL rotalarında white-label standartlarına aykırı olarak doğrudan kiracı ismine veya statik slug'a bağımlı kalma riski.
14. **Yetersiz Entegrasyon Testleri:** Veritabanı testlerinin yalnızca SQLite in-memory üzerinde çalıştırılması, PostgreSQL runtime'a özel farkların test edilmemesi.
15. **Hata Yakalama (Result Pattern) Eksikliği:** Eski entegrasyon controller'larında hata kontrolü yerine doğrudan `throw` yapılması riskleri.
16. **Telephony Modülü Entegrasyon Kopukluğu:** Python ses köprüsünün .NET monolit içindeki bilet (ticket) ve cari (account) kartlarıyla bağlantısının gevşek (loosely coupled) olması.
17. **Merkezi Hook ve Cache Yönetimi Eksikliği:** Her sayfa/widget için ayrı `useQuery` tanımlanması, caching stratejisinin kurulmaması.
18. **Loki/Promtail Enstrümantasyon Eksikliği:** Docker compose katmanında Loki bulunmasına rağmen, .NET 8 API içinde yapılandırılmış telemetry loglarının Loki'ye akıtılmaması.
19. **Row-Level Security (RLS) Açıkları:** Base repository düzeyinde kiracı ID filtresinin bazı custom SQL sorgularında bypass edilme riski.
20. **Google Sheets Sync Arka Plan Servisi Eksikliği:** KPI verilerini güncelleyecek Sheets entegrasyonunun iş kurallarının yazılmamış olması.

---

# 7. Roadmap Review

Mevcut V3 Yol Haritası (`06_DELIVERY_ROADMAP.md`):
* **F0 (2 hafta):** Analiz, KPI katalog, mock→entity mapping
* **F1 (4 hafta):** Shell, widget registry, mock adapter (Frontend Refactor)
* **F2 (6 hafta):** API + 4 rol canlı (seed data) (Backend Pilot)
* **F3 (8 hafta):** 12 rol + Sheets sync + drill-down
* **F4 (4 hafta):** Go-live (ERP, PDF, AI drafts, health score, sidebar)

### CTO ve Chief Architect Değerlendirmesi:
Mevcut yol haritası **yanlıştır**. 
F1 (Frontend Refactor) fazının, backend API kontratları (DTO'lar ve Swagger) belirlenmeden önce yapılması **çift işe (double work)** neden olur. Frontend tarafında mock veri adaptörü kurup sayfayı refactor etmek, backend veri modelleri ortaya çıktığında frontend modellerini yeniden değiştirmek anlamına gelecektir.

### Önerilen Yeni Yol Haritası Sırası (CTO Target Roadmap):

```text
  [F0: Kontrat & Katalog] (2 Hafta)
            │
            ▼
  [F1: Backend Pilot API & DB] (4 Hafta) ───► Veritabanı şeması ve DTO'lar netleşir
            │
            ▼
  [F2: Frontend Refactor & Shell] (4 Hafta) ───► API DTO'larına göre arayüz refactor edilir
            │
            ▼
  [F3: Entegrasyon & Rollout] (8 Hafta) ───► Pilot 4 rol + Sheets Sync + Drill-down bağlanır
            │
            ▼
  [F4: Go-Live & AI & Export] (6 Hafta) ───► ERP Sync, AI Message Drafts, PDF, Gauge Dials
```

---

# 8. Recommendations (İlk Yapılacak 10 İş)

1. **Ajan Talimat Temizliği (P0):** Repository içindeki tüm mükerrer `AGENTS.md` ve `CLAUDE.md` dosyalarını silip, kuralları tek bir master `AGENTS.md` dosyasında birleştirin.
2. **Dashboard Sayfasının Bölünmesi (P0):** ~10.000 satırlık dev Next.js dashboard kodunu, rol bazlı modüler widget dosya yapısına dönüştürün (`features/elyaf-control-tower/components/roles/*`).
3. **Database Şemasının Çıkartılması (P1):** `DecisionLog`, `KpiSnapshot` ve `CompanyHealthScore` entity'leri için migration oluşturup PostgreSQL veritabanına uygulayın.
4. **KPI Katalog Dosyasının İmzalanması (P1):** `Elyaf_KPI_Katalog.csv` dosyasını doldurup iş biriminden formül ve veri kaynağı onaylarını alın.
5. **Sol Sidebar Navigasyonunun Yapılması (P1):** Geçici yatay barı kaldırıp, visual spec belgelerinde tanımlanan dikey sol navigasyonu kodlayın.
6. **Erişim Route Guard'larının Eklenmesi (P1):** Next.js tarafında kullanıcı rolü ile erişmeye çalıştığı dashboard rolünü (`/control-tower/[slug]`) eşleştiren route guard middleware ekleyin.
7. **Merkezi Veri Getirme Hook'u (`useElyafDashboard`) (P2):** Caching, background refresh ve invalidation mekanizmalarını yönetecek tek bir React Query custom hook'u yazın.
8. **i18n Localization Temizliği (P2):** Dashboard bileşenlerindeki tüm hardcoded Türkçe kelimeleri `emare-i18n` JSON dosyalarına taşıyarak i18n standartlarını uygulayın.
9. **KpiValidationJob Background Service (P2):** Departmanlar arası KPI tutarlılığını günlük olarak kontrol edip sapma durumunda alert fırlatan arka plan işini kodlayın.
10. **PDF / Excel Export API (P3):** Gösterge paneli ve detay tabloları için sunucu taraflı export uç noktalarını backend `ReportingModule` altında implemente edin.

---

# 9. Files To Remove (Silinebilecek Eski Dosyalar)

* `web/AGENTS.md` (kök dizindeki ana dosya ile çelişiyor)
* `web/CLAUDE.md` (kök dizindeki ana dosya ile çelişiyor)
* `gemini-live-standalone/AGENTS.md` (gereksiz talimat kopyası)
* `web/docs/MODULE_MAP.md` (INDEX.md ile çakışıyor, sürümü eski)

---

# 10. Files To Merge (Birleştirilmesi Gereken Dokümanlar)

* `docs/CRM_CANONICAL_MODEL.md` ➡️ `Yeni versiyon geçiş/DOMAIN_MODEL.md` (Tek bir kanonik veri modeli dokümanı olmalı)
* `Yeni versiyon geçiş` altındaki tüm kural ve standartlar (`ANAYASA.md`, `API_STANDARDLARI.md` vb.) kök dizindeki `docs/` klasörü altına taşınmalı ve çift repository yapısında tek bir güncel dizin olarak referans gösterilmelidir.

---

# 11. Final Verdict

"Bu proje şu anda, çekirdek altyapı ve veri tabanı katmanlarında olgun ve derli toplu bir C#/.NET 8 monolit yapısına sahip olmakla birlikte; ana ticari çıktı olan **Elyaf Control Tower** tarafında henüz veritabanı entegrasyonu, veri hesaplama motoru ve yapay zekâ entegrasyonları başlatılmamış, tamamen statik mockup'lardan oluşan bir **görsel prototip (frontend mockup)** seviyesindedir."
