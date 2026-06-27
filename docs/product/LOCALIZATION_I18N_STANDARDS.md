# 🌐 Çoklu Dil (i18n) ve Yerelleştirme Standartları

**Versiyon:** 1.0.0  
**Durum:** Approved  
**Sahip:** Architecture & Product Board  
**Son Güncelleme:** 2026-06-27  
**Bağımlı Dokümanlar:** FRONTEND_STANDARDLARI.md, DOMAIN_MODEL.md

---

## 1. Genel Bakış

Emare BOS platformu, küresel ölçeklenebilirlik ve çok dilli kullanıcı tabanlarını desteklemek amacıyla tasarlanmıştır. Sistemde hem kullanıcı arayüzü (frontend) hem de veri/iş mantığı katmanları (backend & database) çoklu dil desteğine (i18n) tam uyumlu olarak yapılandırılmıştır.

Platform genelinde kullanılan dil yönetim sisteminin üç ana sacayağı bulunmaktadır:
1. **`emare-i18n`:** Emare BOS için özel olarak geliştirilmiş, tamamen tip güvenli (type-safe) ve hafif i18n motoru.
2. **Arayüz Yerelleştirmesi:** Sayfa etiketleri, form alanları, hata mesajları ve genel arayüz metinleri.
3. **Veri Yerelleştirmesi (Dynamic Content):** Veritabanında saklanan dinamik verilerin (örn. kumaş türleri, ürün adları, departman açıklamaları) farklı dillerdeki karşılıkları.

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
        └── en.ts           ← İngilizce çeviri dosyası
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

---

## 4. Backend Yerelleştirme Standartları (.NET 8)

Backend servislerinin (API) istemciye döndüğü hata mesajları, e-posta şablonları ve bildirim metinleri de istemcinin talep ettiği dile göre yerelleştirilmelidir.

### 🌐 Dil Tercihinin Alınması (Accept-Language Header)
API katmanı, gelen HTTP isteklerinin başlığındaki `Accept-Language` değerini okur.
- Varsayılan dil: `tr-TR`
- Desteklenen diller: `tr-TR`, `en-US`
- İlgili Middleware (`RequestLocalizationMiddleware`) gelen dil kodunu iş parçacığı (Thread Culture) seviyesine set eder: `CultureInfo.CurrentCulture` ve `CultureInfo.CurrentUICulture`.

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
