# Test Stratejisi (TEST_STRATEJISI.md)

Bu döküman, ERP modüllerinin hatasız ve kararlı bir şekilde geliştirilmesi amacıyla uygulanacak olan test standartlarını tanımlar.

---

## 🧪 1. Test Piramidi ve Kapsamları

### A. Birim Testleri (Unit Tests)
- **Kapsam:** Business logic içeren Domain entity metotları, CQRS Command/Query validation kuralları ve domain event'ler.
- **Teknoloji:** xUnit, FluentAssertions, NSubstitute.
- **Kural:** Her modül için yazılan kurallar (Örn: "İzin onaylandığında bakiye düşürülür") birim testleri ile izole edilerek test edilmelidir.

### B. Entegrasyon ve Veritabanı Testleri (Integration Tests)
- **Kapsam:** EF Core DbContext, repository sorguları, transactional durumlar ve veri tabanı kısıtları.
- **Veritabanı:** In-Memory database (`Microsoft.EntityFrameworkCore.InMemory`) veya geçici SQLite/Postgres şemaları test tohumlama (seed) ile ayağa kaldırılır.

### C. Denetleyici Testleri (Controller/API Tests)
- **Kapsam:** HTTP Status kodları, model binding validation'ları, JWT/Claim yetkilendirmeleri.
- **Test Sınıfı:** `tests/EmareTicket.Tests/Elyaf/ElyafApiControllerTests.cs` benzeri entegrasyon test yardımcıları kullanılmalıdır.

---

## ⚠️ 2. PostgreSQL DateTimeKind.Utc Testi (Kritik)

Npgsql veritabanı sürücüsü, `timestamptz` sütunları için yalnızca **`DateTimeKind.Utc`** tipindeki tarihleri kabul eder. Aksi halde PostgreSQL runtime 500 hatası üretir.
- **Kural:** Entity oluşturulurken veya veritabanına veri yazılmadan önce tarih alanlarının `DateTimeKind.Utc` olduğu xUnit testlerinde Assert edilmelidir:
  ```csharp
  // Test içerisinde:
  entity.CreatedAt.Kind.Should().Be(DateTimeKind.Utc);
  ```

---

## 🔒 3. Kiracı İzolasyon Testleri (Multi-Tenant Tests)
Multi-tenant veri izolasyonunun doğrulanması amacıyla her entegrasyon testinde şu senaryo koşulmalıdır:
1. **Tenant A** ile bir kayıt oluşturun.
2. Aktif kiracıyı **Tenant B** yapın.
3. Tenant A'nın verisini okumaya çalışın.
4. Okuma sorgusunun **`null`** veya boş liste döndüğünü Assert edin.
   ```csharp
   // Örnek:
   var result = await repository.GetByIdAsync(tenantA_RecordId);
   result.Should().BeNull(); // Tenant B bu kayda erişememelidir.
   ```

---

## ⚙️ 4. Test Çalıştırma Protokolü
Tüm testler yerel ortamda ve sunucu dağıtımları öncesinde otomatik çalıştırılmalıdır:
```bash
dotnet test
```
Tüm test vakaları (tests PASSED) başarıyla yeşil yanmadan kod teslimi yapılamaz.
