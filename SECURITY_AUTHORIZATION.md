# Güvenlik ve Yetkilendirme Standartları (SECURITY_AUTHORIZATION.md)

Bu döküman, ERP platformundaki verilerin güvenliğini, rol bazlı erişim denetimlerini (RBAC) ve kiracılar arası (multi-tenant) veri izolasyonunun kod seviyesindeki kurallarını tanımlar.

---

## 🔒 1. Kiracı İzolasyonu (Tenant Isolation Enforcement)
- **Kural:** Hiçbir kullanıcı kendi kiracısına (Tenant) ait olmayan verilere erişemez, ekleme veya silme yapamaz.
- **Zorunlu Filtre (DbContext Filter):**
  ```csharp
  // AppDbContext.cs
  builder.Entity<CrmAccount>().HasQueryFilter(x => x.TenantId == _tenantProvider.TenantId);
  ```
- **Zorunlu Controller Filtresi (`[RequireTenant]`):**
  Tüm yeni eklenen API Controller sınıflarının tepesinde `[RequireTenant]` veya `[Authorize]` filtreleri yer almalıdır. Bu filtreler, kullanıcının JWT token'ı içerisindeki `tenant_id` claim'inin doğruluğunu kontrol eder.

---

## 👥 2. Rol Bazlı Yetkilendirme (RBAC - Role-Based Access Control)

Sistemdeki kullanıcılar aşağıdaki rollere sahip olabilir ve bu roller bazında erişim kısıtlamalarına tabi tutulmalıdır:

| Rol Adı | İzin Verilen Modüller / Controller Uçları | Kısıtlamalar / Göremeyeceği Veriler |
|---|---|---|
| **CEO / Executive** | Tüm Modüller (`GET`, `POST`, `PUT`, `DELETE` - Karar Defteri dâhil) | Kısıtlama yok, her şeyi görebilir. |
| **Sales Manager** | `CrmController`, `LogisticsController` (`GET` - Stok Durumu) | Finansal Muhasebe Fişlerini ve İK/Personel maaş verilerini göremez. |
| **Finance Manager** | `FinanceController`, `CrmController` (`GET` - Müşteriler & Faturalar) | İK/Personel maaş detaylarını göremez (Sadece genel gider toplamını görür). |
| **HR Manager** | `HrController` | Finansal Muhasebe detaylarını ve Satış/Müşteri datalarını göremez. |
| **QC Manager** | `QcController`, `LogisticsController` (`GET`) | Finans ve Satış teklif tutarlarını göremez. |
| **Logistics Manager** | `LogisticsController`, `QcController` (`GET` - Test Sonuçları) | Finans, Satış Teklifleri ve İK verilerini göremez. |

---

## 🛠️ 3. Kod Seviyesinde Rol Denetimi

Ajanlar API uçlarını korumak için ASP.NET Core rol denetim attribute'larını (`[Authorize]`) kullanacaktır:

```csharp
[ApiController]
[Route("api/control-tower/finance")]
[Authorize(Roles = "Ceo,FinanceManager")] // Sadece CEO ve Finans Yöneticisi erişebilir
public class FinanceController : ControllerBase
{
    // ...
}
```

Arayüz tarafında da (Next.js) `canAccessElyafTower` fonksiyonu kullanılarak kullanıcının rol yetkisi olmayan yan menü linkleri ve sayfaları gizlenmeli, sunucu tarafında (Server Components) yetki kontrolleri yapılmalıdır.
- **Frontend Yetki Yardımcısı:** `@/features/elyaf-control-tower/utils/elyafAccess.ts`
