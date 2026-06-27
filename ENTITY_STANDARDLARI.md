# Entity Standartları (ENTITY_STANDARDLARI.md)

Bu döküman, C# backend (.NET 8 EF Core) katmanında oluşturulacak tüm veritabanı entity sınıflarının ve veritabanı şemalarının uyması gereken kuralları tanımlar.

---

## 🏗️ 1. Temel Sınıf Yapısı (BaseAuditableEntity)

Tüm veritabanı tabloları, denetim izi (audit log) ve kimlik alanlarını içermek için `BaseAuditableEntity` sınıfından türetilmelidir.

`BaseAuditableEntity` sınıfı aşağıdaki alanları içerir ve otomatik güncellenir:
- `Guid Id` (Primary Key)
- `Guid TenantId` (Kiracı İzolasyon ID'si)
- `DateTime Created` (Oluşturulma Tarihi - UTC)
- `string? CreatedBy` (Oluşturan Kullanıcı ID/Username)
- `DateTime? LastModified` (Son Değişiklik Tarihi - UTC)
- `string? LastModifiedBy` (Son Değiştiren Kullanıcı)

---

## 🔒 2. Multi-Tenant İzolasyonu (TenantId Zorunluluğu)
- **Kural:** Sistemdeki tüm kalıcı veriler kiracı bazında izole edilmelidir. Bu nedenle, sisteme eklenen tüm yeni entity sınıflarında `Guid TenantId` alanı **zorunludur**.
- **Otomatik Filtreleme:** EF Core tarafındaki DbContext konfigürasyonunda (`OnModelCreating`), tüm sorgularda otomatik olarak aktif kiracı filtresi (`HasQueryFilter(x => x.TenantId == _tenantProvider.TenantId)`) uygulanmalıdır.

---

## 🗑️ 3. Yumuşak Silme (Soft Delete)
- Tüm ana veriler (Müşteri, Fırsat, Teklif, Fişler, Depo, Çalışan) silinirken fiziksel olarak veritabanından yok edilmemelidir.
- Sınıflarda `IsDeleted` (boolean) veya `DeletedAt` (DateTime?) alanları kullanılmalı; sorgularda silinen veriler otomatik elenmelidir (`HasQueryFilter(x => !x.IsDeleted)`).

---

## 🔢 4. Para ve Ondalık Sayı Standartları (Decimal Precision)
- **Kural:** Tutar, fiyat, bakiye, oran ve miktar gibi tüm ondalıklı alanlar için PostgreSQL veritabanında **`decimal(18,2)`** veri tipi kullanılacaktır.
- **Fluent API Konfigürasyonu:**
  ```csharp
  builder.Property(x => x.TotalAmount)
         .HasPrecision(18, 2);
  ```

---

## 🏷️ 5. Enum vs String Tercihleri
- **Kural:** Durum (Status), Tip (Type), Aşama (Stage) gibi sınırlı seçenekli alanlar C# kodunda **`Enum`** olarak tanımlanmalı; ancak veritabanına yazılırken veri tabanı okunabilirliğini artırmak amacıyla **`string` (varchar)** olarak kaydedilmelidir.
- **Dönüştürme Konfigürasyonu:**
  ```csharp
  builder.Property(x => x.Status)
         .HasConversion<string>();
  ```

---

## 🔢 6. Seri Numarası ve Kod Üretim Standartları
Müşteri kodları (`CR-000001`), yevmiye fiş numaraları (`YV-2026-00001`) gibi otomatik artan seri numaralarının üretimi için merkezi bir veritabanı sequence yapısı veya merkezi bir numaratör servisi (`INumberSequenceService`) kullanılacaktır. Ajanlar kendi sınıflarında statik sayaçlar kullanmamalı, merkezi servisi enjekte ederek numara almalıdır.
- **Servis Arayüzü:**
  ```csharp
  public interface INumberSequenceService
  {
      Task<string> GenerateNextNoAsync(string prefix, Guid tenantId);
  }
  ```
- **Örnek Prefixler:**
  - Satış/Cari: `CR-` (Cari Hesabı / Müşteri)
  - Teklifler: `PR-` (Teklif / Proposal)
  - Muhasebe Fişi: `YV-` (Yevmiye Fişi)
  - Stok Transferi: `TRF-` (Transfer)
