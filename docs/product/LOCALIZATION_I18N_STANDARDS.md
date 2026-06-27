# 🌐 Çoklu Dil (i18n) ve Yerelleştirme Standartları

**Versiyon:** 1.1.0  
**Durum:** Approved  
**Sahip:** Architecture & Product Board  
**Son Güncelleme:** 2026-06-27  
**Bağımlı Dokümanlar:** FRONTEND_STANDARDLARI.md, DOMAIN_MODEL.md, CONTROL_TOWER_FINAL_SCOPE.md

---

## 1. Genel Bakış ve Kilitli Diller

Emare BOS platformu, küresel ölçeklenebilirlik ve çok dilli kullanıcı tabanlarını desteklemek amacıyla tasarlanmıştır. Sistemde hem kullanıcı arayüzü (frontend) hem de veri/iş mantığı katmanları (backend & database) çoklu dil desteğine (i18n) tam uyumlu olarak yapılandırılmıştır.

### 🔒 Desteklenen Kilitli Diller
Platformun ilk sürümünde desteklenecek diller kesin olarak aşağıdaki gibi sınırlandırılmış ve kilitlenmiştir:

*   **`tr-TR`** (Türkçe - Türkiye) - Varsayılan Sistem Dili (defaultLocale)
*   **`en-US`** (İngilizce - Amerika Birleşik Devletleri)
*   **`de-DE`** (Almanca - Almanya)
*   **`ar-SA`** (Arapça - Suudi Arabistan) - *RTL Düzen Desteği ile*

Platform genelinde kullanılan dil yönetim sisteminin üç ana sacayağı bulunmaktadır:
1. **`emare-i18n`:** Emare BOS için özel olarak geliştirilmiş, tamamen tip güvenli (type-safe) ve hafif i18n motoru.
2. **Arayüz Yerelleştirmesi:** Sayfa etiketleri, form alanları, hata mesajları ve genel arayüz metinleri.
3. **Veri Yerelleştirmesi (Dynamic Content):** Veritabanında saklanan dinamik verilerin farklı dillerdeki karşılıkları.

---

## 2. Tip Güvenli `emare-i18n` Paketi

Arayüz yerelleştirmesinde standardizasyonu sağlamak ve derleme zamanında (compile-time) hataları önlemek amacıyla sıfır bağımlılıklı `emare-i18n` paketi kullanılmaktadır.

### 🛡️ Derleme Zamanı Tip Güvenliği (Type-Safety)
`emare-i18n`, dil dosyalarındaki nesne hiyerarşisini tarayarak geçerli tüm çeviri anahtarlarını birer TypeScript tipi (`LeafPath<T>`) haline getirir.
- **Avantajı:** Yanlış yazılan veya silinmiş bir dil anahtarı derleme esnasında hata verir (Build fail). Editör üzerinde otomatik tamamlama (IntelliSense) desteği sağlar.
- **Kısıt:** Maksimum nesne derinliği performans optimizasyonu açısından `6` seviye ile sınırlandırılmıştır.

### 🔄 SSR ve Hydration Güvenliği (`deferClientDetection`)
Sunucu Tarafı Render (SSR - Next.js) mekanizmalarında, sunucunun ürettiği HTML ile istemcinin (browser) ilk render ettiği HTML'in birebir uyuşması gerekir. Tarayıcı dilinin veya `localStorage` kayıtlarının sunucu tarafından bilinememesi durumunda **React Hydration Mismatch (#310)** hatası oluşur.

`emare-i18n` bu hatayı önlemek için **Defter Client Detection** özelliğini barındırır:
1. İstemci ilk render'ı sunucuyla aynı dilde (`defaultLocale` - varsayılan olarak `tr`) gerçekleştirir.
2. Sayfa tarayıcıya yerleştikten (mount olduktan) sonra `applyClientLocale()` metodu tetiklenir.
3. Kaydedilmiş dil (`localStorage`'taki `emare_ticket_lang` anahtarı) veya tarayıcı dili algılanarak arayüz sayfayı yenilemeden dinamik olarak güncellenir.

### 🧩 Zengin Biçimlendirmeli `<Trans>` Bileşeni
Düz metinlerin yanı sıra içinde HTML etiketleri veya React bileşenleri barındıran çeviriler için `<Trans>` bileşeni kullanılır.

**Dil Dosyası Tanımı:**
```typescript
export const tr = {
  welcome_message: "Sisteme hoş geldiniz. Lütfen <profileLink>profilinizi</profileLink> güncelleyin."
};
```

**Kullanım:**
```tsx
import { Trans } from 'emare-i18n/react';

<Trans 
  i18nKey="welcome_message" 
  components={{
    profileLink: <Link href="/profile" className="text-blue-500 underline" />
  }}
/>
```

---

## 3. Frontend İsimlendirme ve Dosya Yapısı Standardı

Tüm frontend projelerinde (Next.js Dashboard, Reseller Portal vb.) çeviri dosyaları aşağıdaki dizin yapısına uymak zorundadır:

```text
src/
└── config/
    ├── i18n.ts             ← i18n konfigürasyonu ve default ayarlar
    └── locales/
        ├── tr.ts           ← Türkçe ana dil şeması (Kanonik şema)
        ├── en.ts           ← İngilizce çeviri dosyası
        ├── de.ts           ← Almanca çeviri dosyası
        └── ar.ts           ← Arapça çeviri dosyası
```

### Kurallar:
1. **Kanonik Şema (TR):** Tüm geliştirme süreçlerinde Türkçe (`tr.ts`) dosyası ana şema kabul edilir. TypeScript tipleri bu dosyadan türetilir.
2. **Kategori Ayrımı:** Dil dosyası içindeki anahtarlar karmaşayı önlemek için kategorize edilmelidir:
   - `common`: Butonlar, genel etiketler (Kaydet, İptal, Düzenle vb.)
   - `navigation`: Menü başlıkları, breadcrumb alanları.
   - `validation`: Form doğrulama hata mesajları.
   - `pages`: Sayfa özelindeki benzersiz metinler.
3. **Pluralization (Çoğul Yapısı):** Sayısal ifadelerin çoğullandırılmasında sonek standardı uygulanır:
   - `_zero`: Sıfır durumunda gösterilecek metin.
   - `_one`: Tekil durumda gösterilecek metin.
   - `_other`: Çoğul durumda gösterilecek metin (örn. `{count} öğe var`).

### 🏰 3.1. Control Tower i18n Zorunluluğu
Tüm **Control Tower** ekranlarının (CEO, Sales, Finance vb.) geliştirilmesinde i18n desteği **ZORUNLUDUR**.
- Arayüzde yer alan hiçbir etiket, grafik başlığı, alert uyarısı, buton metni, tablo kolonu veya KPI açıklaması hardcoded olarak yazılamaz.
- Tüm statik ve yarı dinamik metinler `emare-i18n` kütüphanesinin `t()` fonksiyonu üzerinden geçirilmelidir.

### ⬅️ 3.2. RTL (Right-to-Left) Arayüz Desteği (Arapça - ar-SA)
Arapça (`ar-SA`) dil seçeneği seçildiğinde, uygulamanın tüm görsel düzeni (layout) sağdan sola (RTL) akacak şekilde değişmelidir.
- **HTML dir Özniteliği:** Arayüz dilinin `ar-SA` olması durumunda, root `<html>` veya `<body>` etiketine dinamik olarak `dir="rtl"` özniteliği eklenmelidir.
- **Mantıksal CSS Özellikleri (Logical Properties):** Tasarımlarda sağ/sol yön bağımlı CSS özellikleri (`margin-left`, `padding-right`, `left: 0`) yerine, metin yönüne göre otomatik yön değiştiren mantıksal CSS özellikleri (`margin-inline-start`, `padding-inline-end`, `inset-inline-start: 0`) kullanılmalıdır.
- **Görsel Objelerin Yönü:** İlerleme çubukları (progress bars), ok işaretleri ve kronolojik akış grafiklerinin yönü RTL modunda ayna görüntüsü alacak şekilde otomatik tersine dönmelidir (ancak video/ses oynatıcı kontrolleri ve global sayı formatları bu kuralın dışındadır).

---

## 4. Backend ve AI Copilot Yerelleştirme Standartları (.NET 8)

Backend servislerinin (API) istemciye döndüğü hata mesajları, e-posta şablonları, bildirim metinleri ve AI servis çıktıları dil kurallarına uymak zorundadır.

### 🌐 Dil Tercihinin Alınması (Accept-Language Header)
API katmanı, gelen HTTP isteklerinin başlığındaki `Accept-Language` değerini okur.
- Varsayılan dil: `tr-TR`
- Desteklenen diller: `tr-TR`, `en-US`, `de-DE`, `ar-SA`
- İlgili Middleware (`RequestLocalizationMiddleware`) gelen dil kodunu iş parçacığı (Thread Culture) seviyesine set eder: `CultureInfo.CurrentCulture` ve `CultureInfo.CurrentUICulture`.

### 🤖 4.1. AI Copilot Cevap Dili Öncelik Hiyerarşisi
AI Copilot veya Grok LLM / local fallback servisleri kullanıcıya yanıt üretirken, kullanılacak hedef dil aşağıdaki hiyerarşik öncelik sırasına göre belirlenir:

1.  **Aktif Kullanıcı Dili (User Profile/UI Select):** Kullanıcının o an arayüzde seçtiği veya profil ayarlarında kilitlediği dil tercihi (birincil öncelik).
2.  **Kiracı Varsayılan Dili (Tenant Default Language):** Kullanıcı tercihi belirtilmemişse, bağlı bulunulan Tenant'ın (SaaS organizasyonu) varsayılan dili (ikincil öncelik).
3.  **İstek Üstbilgisi (Accept-Language HTTP Header):** Yukarıdaki iki bilgiye de erişilemediğinde HTTP istek başlığında tarayıcıdan gelen Accept-Language kodu (üçüncül öncelik/fallback).

### 🗂️ Veritabanı Çoklu Dil Mimarisi (PostgreSQL JSONB)
Dinamik verilerin çoklu dil desteği için iki farklı yöntem uygulanır:

#### Yöntem A: JSONB Kolon Modeli (Tercih Edilen)
Sadece başlık, açıklama gibi sınırlı sayıda alanın yerelleştirileceği entity'lerde PostgreSQL `jsonb` veri tipi kullanılır.

**C# Sınıf Tanımı:**
```csharp
public class FabricMaterial : AuditableEntity
{
    public Guid Id { get; set; }
    
    // JSONB alan: {"tr": "Pamuklu Kumaş", "en": "Cotton Fabric"}
    public Dictionary<string, string> NameTranslations { get; set; } = new();

    // Kolay erişim için helper property
    public string GetName(string culture)
    {
        if (NameTranslations.TryGetValue(culture, out var name))
            return name;
            
        return NameTranslations.GetValueOrDefault("tr", string.Empty);
    }
}
```

#### Yöntem B: Çeviri Tablosu (Translation Table)
Arama, indeksleme veya karmaşık raporlama gerektiren büyük hacimli veri yapılarında her ana entity için ayrı bir translation entity'si oluşturulur.

**Şema Tasarımı:**
- `Product` (Ana Entity)
  - `Id`
  - `Sku`
  - `Price`
- `ProductTranslation` (Çeviri Entity)
  - `Id`
  - `ProductId` (Foreign Key)
  - `LanguageCode` (örn. "tr", "en")
  - `Name`
  - `Description`

---

## 5. Çoklu Dil Süreç Akışı ve CI/CD translation-hook

Repository üzerinde yapılan geliştirmelerde dil dosyalarının bütünlüğünü korumak için pre-commit veya push aşamalarında çalışan **translation-hook** devreye girer.

```text
[Geliştirici Kod Yazar]
         ↓
  [git commit]
         ↓
🤖 translation-hook Tetiklenir
  - tr.ts ile en.ts anahtarlarını kıyaslar
  - Eksik anahtar varsa commit işlemini engeller veya uyarır
         ↓
  [Commit Başarılı]
```

Bu kontrol mekanizması sayesinde canlı ortamda (production) arayüzde tanımsız anahtarların (`missing key`) görünmesi engellenir.

---

*Bu doküman platform standartlarını tanımlar. Değişiklikler Architecture Board onayı ile yapılır.*
