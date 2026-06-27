# 🎨 Control Tower UX Review (UX_REVIEW.md)

**Title:** Control Tower UX Review  
**Version:** 1.0.0  
**Status:** Draft — Onay Bekliyor  
**Owner:** Product Board / Agent 5 (UX Review)  
**Last Updated:** 2026-06-27  
**Dependencies:** CONTROL_TOWER_FINAL_SCOPE.md, FRONTEND_STANDARDLARI.md, LOCALIZATION_I18N_STANDARDS.md, AI_ENGINE.md, FEATURE_TRACEABILITY_MATRIX.md  
**Related Documents:** SECURITY_REVIEW.md, FULL_REPO_REVIEW_CHECKLIST.md

---

## Amaç

Bu doküman, Elyaf Group 2.0 platformunun **16 Control Tower** ekranı için kullanıcı deneyimi (UX) standartlarını, mevcut tasarım kararlarını, boşlukları ve iyileştirme önerilerini tanımlar. İnceleme; [CONTROL_TOWER_FINAL_SCOPE.md](CONTROL_TOWER_FINAL_SCOPE.md) v1.1.0 kapsamı, görsel kabul kriterleri, frontend standartları ve i18n gereksinimleri doğrultusunda **Agent 5 (UX Review)** tarafından hazırlanmıştır.

> Bu doküman ürün ve tasarım kararları içerir. **Kod içermez.**

---

## 📊 Genel UX Özet Matrisi

| Denetim Alanı | Mevcut Tasarım Durumu | Öncelik |
|---|---|---|
| **Dashboard Layout Review** | 🟡 Kapsam tanımlı, bileşen grid standardı eksik | **CRITICAL** |
| **KPI Card Standards** | 🟡 Görsel kabul kriteri var, atomik bileşen spec yok | **CRITICAL** |
| **Widget Standards** | 🟡 15 standart blok listelenmiş, davranış spec kısmi | **HIGH** |
| **Mobile View** | 🔴 Responsive strateji dokümante edilmemiş | **CRITICAL** |
| **Tablet View** | 🔴 Breakpoint ve yoğunluk kuralları tanımsız | **HIGH** |
| **Accessibility (WCAG)** | 🔴 WCAG hedef seviyesi ve checklist yok | **CRITICAL** |
| **Dark Mode** | 🟡 CEO modülünde dark mode hedefi var, global token yok | **HIGH** |
| **Color Palette** | 🟡 HSL değişken yaklaşımı var, semantik renk matrisi eksik | **HIGH** |
| **Navigation Consistency** | 🟡 Sol menü + modül alt menüsü tanımlı, tutarlılık riski var | **HIGH** |
| **Notification UX** | 🟡 Toast (sweetAlert) + panel ayrımı belirsiz | **HIGH** |
| **AI Copilot UX** | 🟡 Mimari tanımlı, arayüz yerleşimi ve güven UX'i eksik | **HIGH** |

---

## Referans: Control Tower Arayüz Mimarisi

[CONTROL_TOWER_FINAL_SCOPE.md](CONTROL_TOWER_FINAL_SCOPE.md) her Control Tower için aşağıdaki **15 zorunlu UI bloğunu** kilitler:

1. Executive Snapshot  
2. KPI Kartları (en az 4, trend ok + periyot karşılaştırması)  
3. Today's Priorities  
4. Critical Alerts  
5. Notifications  
6. Risk / Health Score  
7. Customer / Supplier / Department Panel  
8. Message Drafts  
9. Calendar & Key Events  
10. Next 7 Days Focus  
11. Reports & Analytics  
12. Sol dikey menü (modül alt menüleri + geçiş bağlantıları)  
13. Rol bazlı kullanıcı/profil alanı  
14. Export / Filter / Date controls  
15. Legend / status açıklamaları  

Görsel kabul kriteri olarak müşteri paylaşılan `screenshots/*-ct.png` referansları final ürün standardı kabul edilir.

---

## 1. Dashboard Layout Review

### Current Design (Mevcut Tasarım)

* Her Control Tower aynı **15 bileşen alanı** ile tanımlanmış; üst satırda Executive Snapshot ve KPI kartları, alt bölgede öncelik/uyarı/bildirim panelleri, sağ veya alt bölgede takvim ve rapor bağlantıları yer alır.
* **Sol dikey menü** modül bazlı alt menüleri ve Control Tower'lar arası geçişi barındırır.
* Üst KPI satırı en az **4 kart** içermeli; trend yönü yeşil/kırmızı ok ile gösterilir.
* Export, filtre ve tarih aralığı kontrolleri global toolbar alanında toplanması beklenir; kesin grid yerleşimi (12 kolon, satır yüksekliği, panel genişlik oranları) henüz dokümante edilmemiştir.
* [FEATURE_TRACEABILITY_MATRIX.md](FEATURE_TRACEABILITY_MATRIX.md) CEO, Sales ve Finance için **92 widget** API izlenebilirliğini tanımlar; layout bileşenleri ile eşleşen görsel grid şeması yoktur.

### Recommendation (Öneri)

* **Kanonik dashboard grid** tanımlansın: 12 kolonlu responsive grid; KPI satırı `span-3 × 4` (desktop), Executive Snapshot `span-12` veya `span-8 + span-4` (özet + health score).
* **Bölge sırası sabitlensin:** (1) Toolbar → (2) KPI row → (3) Snapshot + Health → (4) Priorities + Alerts (2 kolon) → (5) Notifications + Message Drafts → (6) Calendar + Next 7 Days → (7) Entity panel + Reports.
* Her Control Tower aynı grid iskeletini kullansın; modüle özel içerik yalnızca widget verisi ve menü başlıklarında değişsin.
* **Sticky toolbar** (tarih aralığı, export, filtre) scroll sırasında erişilebilir kalsın.
* Layout şeması `docs/product/CONTROL_TOWER_LAYOUT_SPEC.md` (gelecek doküman) olarak görsel wireframe + breakpoint tablosu ile tamamlansın.

### Priority (Öncelik)

🔴 **CRITICAL** — Sprint 2A (CEO, Sales, Finance) implementasyonu öncesi grid standardı onaylanmalıdır.

---

## 2. KPI Card Standards

### Current Design (Mevcut Tasarım)

* Görsel kabul kriteri: sayısal değer, **trend ok** (yeşil yukarı / kırmızı aşağı), **periyot karşılaştırması** (ör. "vs geçen ay", "Gerçek vs Hedef").
* CEO Control Tower'da 10 KPI, Sales'te 8, Finance'te 8 metrik tanımlı; her biri ayrı API endpoint'ine bağlanır ([FEATURE_TRACEABILITY_MATRIX.md](FEATURE_TRACEABILITY_MATRIX.md)).
* [FRONTEND_STANDARDLARI.md](../../FRONTEND_STANDARDLARI.md) HSL renk değişkenleri (`text-muted-foreground`, `border-primary/10`) kullanımını önerir; KPI kart atomik bileşen API'si (props, varyantlar, loading/error) tanımlı değildir.
* Finansal metriklerde para birimi (₺, $, €) ve yüzde metriklerinde `%` suffix kuralları scope'ta var, UI format standardı yok.

### Recommendation (Öneri)

* Tek **`KpiCard`** bileşen sözleşmesi tanımlansın:

  | Prop | Açıklama |
  |---|---|
  | `label` | i18n anahtarı (`pages.ceo.kpi.monthlyRevenue`) |
  | `value` | Formatlanmış ana değer |
  | `comparison` | Karşılaştırma metni ve delta yüzdesi |
  | `trend` | `up` \| `down` \| `neutral` |
  | `variant` | `positive` \| `negative` \| `neutral` (renk semantiği trendden bağımsız olabilir — örn. gecikmiş alacak artışı kötü trend) |
  | `period` | Seçili tarih aralığı etiketi |
  | `href` | Opsiyonel detay sayfası linki |

* **Skeleton state:** 4 kartlı satır için eşzamanlı shimmer; tek kart hata durumunda satırın geri kalanı etkilenmesin.
* **Empty / N/A state:** Veri yoksa "—" ve açıklayıcı alt metin; sıfır değer ile veri eksikliği görsel olarak ayrışsın.
* **Erişilebilirlik:** Trend ok yalnızca renkle değil; `aria-label` ile "Geçen aya göre %12 artış" ifade edilsin.
* Para birimi locale'e göre `Intl.NumberFormat`; tüm KPI etiketleri `emare-i18n` üzerinden.

### Priority (Öncelik)

🔴 **CRITICAL** — KPI kartları tüm kulelerin ilk görünen yüzeyi; Sprint 2A blocker.

---

## 3. Widget Standards

### Current Design (Mevcut Tasarım)

* 15 standart widget bloğu scope'ta listelenmiş; Today's Priorities, Critical Alerts, Notifications vb. her kule için içerik farklı.
* [FRONTEND_STANDARDLARI.md](../../FRONTEND_STANDARDLARI.md) loading (Skeleton), empty ve error state'lerini zorunlu kılar.
* Widget başlıkları, "View all" bağlantıları ve tablo legend'ları modül görev dosyalarında (örn. `GOREVLER/A1_CEO.md`) parça parça tanımlı; ortak **`DashboardWidget`** kabuğu yok.
* Health / Risk Score widget'ı 1–100 veya A-F skala seçenekleri scope'ta belirsiz bırakılmış.

### Recommendation (Öneri)

* **`DashboardWidget`** kabuğu standartlaştırılsın: başlık, opsiyonel badge (sayı), collapse/expand, "View all" linki, footer legend alanı.
* Widget tipleri sınıflandırılsın:
  - **List widget** (Priorities, Notifications, Drafts)
  - **Score widget** (Health / Risk — gauge veya harf notu)
  - **Table widget** (Customer/Supplier/Department panel)
  - **Calendar widget** (Key Events)
  - **Link hub widget** (Reports & Analytics)
* Critical Alerts widget'ında **severity** seviyeleri: `critical` (kırmızı), `warning` (amber), `info` (mavi); yalnızca renkle değil ikon + metin ile.
* Tüm widget'larda maksimum liste yüksekliği + iç scroll; sayfa genel scroll'unu sınırsız uzatmayın.
* Health Score için **tek skala seçimi**: 0–100 sayısal gauge + A–F harf eşlemesi legend'da; kuleler arası tutarlılık zorunlu.

### Priority (Öncelik)

🟠 **HIGH** — Sprint 2A–2C widget implementasyonu ile paralel.

---

## 4. Mobile View

### Current Design (Mevcut Tasarım)

* Scope dokümanı mobil breakpoint, dokunmatik hedef boyutu veya mobil navigasyon stratejisi tanımlamaz.
* Sol dikey menü desktop-first varsayımına dayanır; mobilde hamburger / bottom nav alternatifi belirtilmemiştir.
* 4 KPI kartlı üst satır ve çoklu panel yoğunluğu küçük ekranda kaydırma yükü yüksek olacaktır.
* [LOCALIZATION_I18N_STANDARDS.md](LOCALIZATION_I18N_STANDARDS.md) RTL desteği mobil layout ile birlikte test edilmeli; mobil RTL kuralları ayrıca tanımsız.

### Recommendation (Öneri)

* **Breakpoint hedefi:** `<640px` mobil; KPI kartları **2×2 grid** veya yatay swipe carousel (tek seferde 1 kart görünür, dot indicator).
* Sol menü mobilde **drawer** (Sheet) olarak açılsın; profil ve dil seçici drawer üstünde sabitlensin.
* Today's Priorities ve Critical Alerts mobilde **üst öncelik** sırasına alınsın (KPI satırından hemen sonra); Calendar ve Reports accordion ile katlansın.
* Dokunmatik hedef minimum **44×44 px**; tablo widget'ları mobilde kart listesine dönüşsün.
* Sticky toolbar mobilde tek satır + "More filters" sheet pattern kullansın.

### Priority (Öncelik)

🔴 **CRITICAL** — Yönetici kullanıcıların mobil erişimi iş gereksinimi; MVP'de en az CEO ve Finance kuleleri mobil uyumlu olmalı.

---

## 5. Tablet View

### Current Design (Mevcut Tasarım)

* Tablet (`640px–1024px`) için ayrı layout tanımı yok; desktop grid'in küçültülmüş hali varsayılıyor.
* Landscape/portrait orientasyon davranışı belirtilmemiş.

### Recommendation (Öneri)

* Tablet portrait: **8 kolon grid** — KPI `span-4 × 2` (2 satır), paneller tek kolon stack.
* Tablet landscape: **12 kolon grid** — desktop layout'a yakın; sol menü daraltılmış (icon-only) mod desteklensin.
* Split-view: Priorities + Alerts yan yana; Calendar + Next 7 Days yan yana.
* iPad Pro gibi geniş tabletlerde Copilot paneli sağ dock olarak açılabilsin (desktop davranışı).

### Priority (Öncelik)

🟠 **HIGH** — Depo/üretim saha kullanımı için Production ve Logistics kulelerinde Sprint 3A öncesi.

---

## 6. Accessibility (WCAG)

### Current Design (Mevcut Tasarım)

* WCAG uyum seviyesi (A / AA / AAA) hiçbir mimari dokümanda hedeflenmemiş.
* Trend okları yeşil/kırmızı renk ayrımına dayanıyor; renk körlüğü alternatifi tanımsız.
* [FRONTEND_STANDARDLARI.md](../../FRONTEND_STANDARDLARI.md) Skeleton loader kullanımını önerir; `aria-busy`, focus trap (Dialog) kuralları yazılı değil.
* i18n zorunluluğu ekran okuyucu dilini kullanıcı locale'ine bağlar; RTL + screen reader birlikte test checklist'i yok.

### Recommendation (Öneri)

* **Hedef: WCAG 2.2 Level AA** — tüm Control Tower ekranları için minimum kabul kriteri.
* Renk kontrastı: metin/arka plan **4.5:1**, büyük metin **3:1**; KPI trend semantiği renk + ikon + metin üçlüsü.
* Klavye navigasyonu: menü, toolbar, widget içi listeler ve modal formlar tam Tab sırası; görünür focus ring (`ring-2 ring-ring`).
* `aria-live="polite"` Critical Alerts ve Notifications güncellemelerinde; toast bildirimleri kısa süreli `role="status"`.
* Grafikler (Recharts): `aria-label` + tablo alternatifi veya veri özeti metni.
* Form hataları `aria-describedby` ile alana bağlansın; Zod mesajları i18n anahtarından gelsin.
* QA checklist: axe-core otomasyonu CI'a; manuel NVDA/VoiceOver smoke test Sprint 2 çıkış kriteri.

### Priority (Öncelik)

🔴 **CRITICAL** — Regülasyon (KVKK/EAA) ve kurumsal müşteri RFP gereksinimleri; erken entegrasyon maliyeti düşürür.

---

## 7. Dark Mode

### Current Design (Mevcut Tasarım)

* CEO modül görev dosyası (`GOREVLER/A1_CEO.md`) **"sleek dark mode"** hedefi belirtir; diğer kuleler ve global tema stratejisi tanımsız.
* [FRONTEND_STANDARDLARI.md](../../FRONTEND_STANDARDLARI.md) HSL CSS değişkenleri kullanımını önerir — Shadcn UI dark/light class pattern ile uyumlu altyapı varsayılır.
* Sistem tercihi (`prefers-color-scheme`), kullanıcı profil tercihi ve tenant branding arasındaki öncelik hiyerarşisi belirsiz.

### Recommendation (Öneri)

* **Üç mod:** Light, Dark, System — profil ayarlarında kalıcı; `localStorage` anahtarı `emare_theme`.
* Tüm semantik renkler (background, foreground, card, destructive, success, warning) HSL token olarak tanımlansın; hardcoded hex yasak.
* KPI trend renkleri dark mode'da doygunluk azaltılsın (`success` / `destructive` token varyantları).
* Grafik (Recharts) grid çizgileri ve tooltip dark palette ile eşleşsin.
* Screenshot kabul kriterleri hem light hem dark referans içersin (`screenshots/ceo-ct-dark.png`).

### Priority (Öncelik)

🟠 **HIGH** — Sprint 2A design token paketi ile birlikte; CEO kulesi pilot.

---

## 8. Color Palette

### Current Design (Mevcut Tasarım)

* Renk yaklaşımı: Shadcn UI HSL değişkenleri (`border-primary/10`, `text-muted-foreground`).
* Scope'ta Critical Alerts kırmızı, trend ok yeşil/kırmızı, Decision Log impact renkleri (High=Kırmızı, Medium=Sarı, Low=Yeşil) modül bazlı tanımlı; merkezi **semantik renk matrisi** yok.
* 16 kule için modül accent rengi (CEO altın, Finance yeşil vb.) tanımsız; navigasyon ayırt edilebilirliği zayıf kalabilir.

### Recommendation (Öneri)

* **Katmanlı palet:**
  - **Core tokens:** `--background`, `--foreground`, `--primary`, `--muted`, `--destructive`, `--success`, `--warning`
  - **Semantic status:** `status-critical`, `status-warning`, `status-ok`, `status-neutral`
  - **Module accent (opsiyonel):** sidebar aktif menü vurgusu için hafif accent; dashboard içeriği nötr kalsın
* Renk körlüğü güvenli çiftler: kırmızı-yeşil yerine kırmızı-mavi veya şekil farkı zorunlu.
* Legend / status açıklamaları scope zorunluluğu — her tablo ve grafik altında token adı + örnek swatch.
* Tenant white-label gelecek faz; MVP'de tek Elyaf Group paleti, token mimarisi genişletilebilir olsun.

### Priority (Öncelik)

🟠 **HIGH** — Design token dokümanı Sprint 2A kickoff deliverable.

---

## 9. Navigation Consistency

### Current Design (Mevcut Tasarım)

* Her Control Tower **sol dikey menü** + modül alt menüleri + kuleler arası geçiş bağlantıları ile tanımlı ([CONTROL_TOWER_FINAL_SCOPE.md](CONTROL_TOWER_FINAL_SCOPE.md) Visual Acceptance Criteria).
* CEO menüsü: Executive Overview, Strategic Decisions, Company Health Score vb.; Sales, Finance, HR menü başlıkları scope'ta ayrı listelenmiş.
* Teknik borç: CDR modülü sidebar linki eksik ([TECHNICAL_DEBT.md](../project-management/debt/TECHNICAL_DEBT.md) TD-012); navigasyon tutarlılığı riski mevcut.
* Breadcrumb, aktif menü vurgusu ve Control Tower seçici (16 kule arası) davranışı dokümante edilmemiş.

### Recommendation (Öneri)

* **Global shell navigasyonu:**
  - Üst bar: tenant logosu, Control Tower seçici (combobox), global arama, bildirim zili, profil, dil, tema
  - Sol sidebar: seçili kuleye ait alt menü; en altta "Diğer Control Tower'lar" grubu
* Aktif route **çift vurgu:** sidebar item + breadcrumb son segment.
* Menü öğeleri yalnızca kullanıcının `*.ControlTower.View` permission'ı olan kuleleri göstersin.
* Tüm menü etiketleri `navigation.*` i18n anahtarları; 16 kule × ortalama 7 menü = ~112 anahtar kanonik TR şemasında.
* Sidebar collapse state kullanıcı tercihine kaydedilsin; mobil drawer ile aynı menü ağacı.

### Priority (Öncelik)

🟠 **HIGH** — Sprint 2A shell implementasyonu; TD-012 benzeri eksik linkler UX borcu olarak kapatılsın.

---

## 10. Notification UX

### Current Design (Mevcut Tasarım)

* İki kanal karışık tanımlı:
  - **Toast (sweetAlert):** anlık işlem sonucu ([FRONTEND_STANDARDLARI.md](../../FRONTEND_STANDARDLARI.md))
  - **Notifications paneli:** rol tabanlı sistem bildirimleri (scope widget #5)
* Scope'ta kule başına farklı bildirim türleri (onay bekleyen belge, fatura oluşturuldu, iş emri tamamlandı vb.); okundu/okunmadı, gruplama, sessize alma kuralları yok.
* [FEATURE_TRACEABILITY_MATRIX.md](FEATURE_TRACEABILITY_MATRIX.md) `GET /api/control-tower/{module}/notifications` endpoint'lerini tanımlar; push/real-time (WebSocket/SSE) stratejisi belirsiz.

### Recommendation (Öneri)

* **Bildirim hiyerarşisi:**
  | Katman | Kullanım | Örnek |
  |---|---|---|
  | Toast | Kullanıcı aksiyonu sonucu | "Kayıt oluşturuldu" |
  | Banner | Kritik sistem durumu | "Nakit açığı eşiği aşıldı" |
  | Notification panel | Async / rol bazlı | "Onay bekleyen teklif" |
  | Critical Alerts widget | İş kritik eşik | Dashboard içi kırmızı alarm |
* Header **zil ikonu** + unread badge; panel slide-over (Sheet) ile son 50 bildirim, "Tümünü gör" sayfası.
* Bildirim kartı: ikon, başlık, özet, zaman (`Intl.RelativeTimeFormat`), primary action (Onayla / Görüntüle).
* Toast süresi: success 3s, error manuel kapatma; aynı anda max 3 toast stack.
* Real-time: SSE veya SignalR; bağlantı kopunca panel polling fallback (60s).
* Tüm bildirim metinleri backend'den locale-aware; frontend hardcoded mesaj yok.

### Priority (Öncelik)

🟠 **HIGH** — Sprint 2B; Finance onay akışları bildirim UX'ine bağımlı.

---

## 11. AI Copilot UX

### Current Design (Mevcut Tasarım)

* [AI_ENGINE.md](../../AI_ENGINE.md): Copilot doğal dil arayüzü; veri kaydetme/silme yasak; `AI.Copilot.Use` permission.
* Mimari akış: Kullanıcı → Copilot → Context Engine → Reasoning → Business Engine → Workflow.
* [LOCALIZATION_I18N_STANDARDS.md](LOCALIZATION_I18N_STANDARDS.md) §4.1: yanıt dili önceliği — (1) kullanıcı dili, (2) tenant dili, (3) Accept-Language.
* IT & AI Digital Control Tower KPI'ları AI model durumunu gösterir; genel Copilot panel yerleşimi, komut paleti, öneri chip'leri ve human-in-the-loop onay UX'i tanımsız.
* [SECURITY_REVIEW.md](../project-management/security/SECURITY_REVIEW.md) AI privilege escalation ve prompt injection risklerini vurgular; kullanıcıya güven ve şeffaflık arayüzü gerekir.

### Recommendation (Öneri)

* **Copilot panel yerleşimi:**
  - Desktop: sağ dock (400px), collapse to floating button
  - Mobile: tam ekran sheet
  - Keyboard shortcut: `Cmd/Ctrl + K` komut paleti
* **Konuşma UX:**
  - Mesaj balonları: kullanıcı / copilot / sistem (tool call özeti)
  - Streaming yanıt cursor; iptal butonu
  - Öneri chip'leri: "Bugünkü önceliklerim", "Nakit pozisyonu özeti" (kule bağlamına göre)
* **Human-in-the-loop:** Copilot'un önerdiği aksiyonlar (onay, e-posta gönderimi) ayrı **onay kartı** ile; kullanıcı tek tıkla onaylamadan işlem yürütülmesin.
* **Şeffaflık:** "Bu yanıt hangi verilere dayanıyor?" expandable kaynak listesi; audit linki (`AIAuditLogs`).
* **Güven sinyalleri:** Veri dışı LLM uyarısı, PII maskelenmiş alan göstergesi, düşük güven skorunda sarı banner.
* **Erişilebilirlik:** Copilot panel focus trap; ekran okuyucu için streaming metin `aria-live` kontrollü güncelleme.
* Copilot arayüz metinleri i18n; CEOAgent / SalesAgent vb. agent adları kullanıcı dilinde görüntülensin.

### Priority (Öncelik)

🟠 **HIGH** — Sprint 2C sonrası IT kulesi ile pilot; MVP'de salt okunur soru-cevap, aksiyon önerisi Sprint 3.

---

## Uygulama Yol Haritası

| Sprint | UX Deliverable | Kapsam |
|---|---|---|
| **Sprint 2A öncesi** | Layout grid spec + KPI card spec + color tokens | CEO, Sales, Finance |
| **Sprint 2A** | Dashboard shell + navigation + WCAG axe baseline | 3 kritik kule |
| **Sprint 2B–2C** | Notification panel + widget kabuğu + dark mode | Finance, HR |
| **Sprint 3** | Mobile/tablet responsive + Copilot panel pilot | Production, Logistics, IT |
| **Sprint 4–5** | Kalan 10 kule UX parity + screenshot kabul testi | Tüm 16 kule |

---

## Kabul Kriterleri (UX Review Exit)

Aşağıdakiler tamamlanmadan UX Review **Approved** sayılmaz:

- [ ] 12 kolon grid wireframe tüm 15 widget bölgesini kapsar
- [ ] `KpiCard` ve `DashboardWidget` bileşen sözleşmeleri yazılı ve onaylı
- [ ] WCAG 2.2 AA checklist CI'da otomatik tarama ile desteklenir
- [ ] Light/dark token seti ve semantik status renkleri dokümante edilir
- [ ] Mobil (<640px) CEO dashboard interaktif prototype veya screenshot kabul testi geçer
- [ ] Bildirim hiyerarşisi (toast vs panel vs alert) ekip içi onaylı
- [ ] Copilot panel wireframe + human-in-the-loop onay akışı onaylı
- [ ] 16 kule menü yapısı `navigation.*` i18n anahtarları ile eşleştirilmiş matris

---

## Revizyon Geçmişi

| Versiyon | Tarih | Yazar | Açıklama |
|---|---|---|---|
| 1.0.0 | 2026-06-27 | Agent 5 (UX Review) | TASK 012 — İlk UX inceleme taslağı |

---

*Bu doküman ürün UX kararları içerir. Kod içermez.*  
*Güncellemeler Product Board onayı ile yapılır.*
