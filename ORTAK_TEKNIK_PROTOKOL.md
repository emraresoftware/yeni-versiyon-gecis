# Ortak Teknik Protokol (ORTAK_TEKNIK_PROTOKOL.md)

Bu protokol, tüm paralel çalışan yapay zeka ajanlarının (A1-A7) kod geliştirirken uyması gereken teknik sınırları ve operasyonel iş kurallarını tanımlar.

---

## 🌳 1. Git & Branching Standardı
- **Aktif Geliştirme Branch'i:** Tüm çalışmalar yalnızca **`gece-otonom`** branch'i üzerinde yürütülür.
- **Push Kuralı:** Ajanlar doğrudan kendi başlarına `push` işlemi yapmazlar. Değişiklikleri yerel repository'e commit edip bıraktıktan sonra push işlemi kullanıcı veya orkestratör agent tarafından tetiklenmelidir.
- **Commit Formatı:** Tüm commit mesajları konvansiyonel commit standardına uymalıdır:
  - `feat(<modül_adı>): <açıklama>`
  - `fix(<modül_adı>): <açıklama>`
  - `docs(<modül_adı>): <açıklama>`
  - Örnek: `feat(crm): add CrmAccount database models and config`

---

## 🚫 2. Dosya Değiştirme ve Sınır Kuralları (Conflict Önleme)
- **Çakışma (Conflict) Önleme Kuralı:** Ajanlar sadece kendi rollerine atanan dizin ve dosyalarda değişiklik yapmalıdır.
- **Ortak Dosyalarda Düzenleme:** `Program.cs`, `AppDbContext.cs` gibi paylaşımlı dosyalarda değişiklik yapılacağı zaman, sadece kendi servislerinin enjeksiyon kayıtları veya `DbSet` tanımları satırları eklenmeli; diğer kod bloklarına kesinlikle dokunulmamalıdır.
- **Arayüz Sınırları:** Her ajan sadece kendisine tahsis edilen Next.js sayfa yollarında (`web/src/app/control-tower/<kendi_rolü>/`) çalışmalıdır. Ortak `layout.tsx` veya `Sidebar.tsx` düzenlemeleri orkestratör gözetiminde yapılmalıdır.

---

## 🗄️ 3. Migration Standartları
- Migration dosyaları kesinlikle **`src/EmareTicket.API`** dizininden çalıştırılarak üretilmelidir.
- Ortam değişkenleri (`.env`) yüklenerek komut verilmelidir.
- **Migration Ekleme Komutu:**
  ```bash
  cd src/EmareTicket.API
  dotnet ef migrations add <MigrationName> --project ../EmareTicket.Persistence --startup-project .
  ```
- **Veritabanı Güncelleme Komutu:**
  ```bash
  dotnet ef database update
  ```

---

## 🧪 4. Test Standardı
- Tüm iş kuralları (business logic) için xUnit test sınıfı yazılması zorunludur.
- Test projeleri: `tests/EmareTicket.Tests` altında, modül adına uygun klasörlerde (Örn: `tests/EmareTicket.Tests/Crm/`) konumlandırılmalıdır.
- Test metodu adlandırma standardı: `MetotAdi_Senaryo_BeklenenSonuc`
  - Örnek: `PostJournalEntry_WhenUnbalanced_ReturnsFailureResult`

---

## ⚙️ 5. Build Kontrol Standartları
- Kodların doğruluğu için teslimat öncesinde hem backend hem de frontend tarafında build alınmalıdır.
- **Backend Derleme:** `dotnet build` sıfır hata ve sıfır uyarı hedefiyle tamamlanmalıdır.
- **Frontend Derleme:** `npm run build` ve `npm run lint` komutları sıfır hata ile tamamlanmalıdır.
