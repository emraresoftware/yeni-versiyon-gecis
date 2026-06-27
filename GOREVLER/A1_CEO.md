# A1: CEO / Executive Control Tower Görev Kutusu

Bu dosya, **A1 (CEO / Executive)** modüllerini ve karar defterini geliştirecek olan ajanın rehberidir.

---

## 🎯 Modül Kapsamı: Karar Defteri (Decision Log) & Yönetici Raporları

CEO'nun şirket içindeki kritik kararları kaydedebileceği, durumunu takip edebileceği ve departman performans özetlerini izleyebileceği yapıdır.

---

## 💾 1. Veritabanı Şeması (Database Schema Specs)

Aşağıdaki entity sınıfı **`src/EmareTicket.Domain/Entities/Elyaf/DecisionLog.cs`** olarak oluşturulmalıdır:

```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class DecisionLog : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string Title { get; set; } = null!;
    public string Description { get; set; } = null!;
    public string Impact { get; set; } = null!; // High, Medium, Low
    public string Status { get; set; } = null!; // Draft, Approved, Implemented, Cancelled
    public DateTime? TargetedCompletionDate { get; set; }
    public DateTime? ActualCompletionDate { get; set; }
    public string? ResolutionNotes { get; set; }
}
```

> [!IMPORTANT]
> - PostgreSQL için tüm DateTime alanları `DateTimeKind.Utc` olmalıdır.
> - EF Core DbContext (`IElyafDbContext`) içerisine `DbSet<DecisionLog> DecisionLogs { get; set; }` kaydı eklenmeli ve migration oluşturulmalıdır.

---

## 🔌 2. REST API Sözleşmesi (Endpoints)

Tüm endpoints **`src/EmareTicket.API/Controllers/ControlTower/CeoDecisionsController.cs`** altında bulunmalıdır:

- **`GET /api/control-tower/ceo/decisions`**
  - **Query Params:** `int pageNumber`, `int pageSize`, `string? status`
  - **Response:** `Result<PagedList<DecisionLogDto>>`
- **`POST /api/control-tower/ceo/decisions`**
  - **Body:** `{ Title, Description, Impact, Status, TargetedCompletionDate }`
  - **Response:** `Result<Guid>`
- **`PUT /api/control-tower/ceo/decisions/{id}`**
  - **Body:** `{ Title, Description, Impact, Status, TargetedCompletionDate, ActualCompletionDate, ResolutionNotes }`
  - **Response:** `Result<bool>`
- **`DELETE /api/control-tower/ceo/decisions/{id}`**
  - **Response:** `Result<bool>`

---

## 🎨 3. Frontend Arayüz Gerekleri (Next.js 16)

Aşağıdaki sayfalar ve bileşenler geliştirilmelidir:

- **Sayfa Yolu:** `web/src/app/control-tower/ceo/decisions/page.tsx`
  - **Tasarım:** Sleek dark mode / modern responsive tablo. Karar kartları önem derecesine göre HSL Halka/Bant renkleriyle (Kırmızı: High, Sarı: Medium, Yeşil: Low) boyanmalıdır.
  - **Form:** Yeni karar ekleme ve düzenleme için modal form (Shadcn UI dialog bileşenleri).
- **Sayfa Yolu:** `web/src/app/control-tower/ceo/page.tsx`
  - **Özet:** Kararların durum dağılımını gösteren ufak bir grafik (Recharts kullanarak) ve en son 5 karar listesi widget'ı.

---

## ⚠️ İş Kuralları ve Doğrulama
- Karar oluşturulurken `Title` ve `Description` boş olamaz (C# FluentValidation ve frontend yup/zod şemalarında doğrulanmalıdır).
- Hata yönetiminde Result Pattern kullanılmalıdır (`Result.Success` veya `Result.Failure`).

---

## 🧪 Sıfır Hata (Zero-Defect) Kontrol Listesi

Ajan kodu tamamlayıp teslim etmeden önce aşağıdaki adımları sırayla doğrulamakla yükümlüdür:
1. [ ] **Veritabanı Migration:** `dotnet ef database update` sorunsuz çalıştı mı?
2. [ ] **Backend Testleri:** `tests/EmareTicket.Tests` altında en az 5 adet xUnit test senaryosu yazıldı ve `dotnet test` sıfır hata ile tamamlandı mı?
3. [ ] **Frontend Derleme:** `npm run build` ve `npm run lint` komutları sıfır uyarı/hata ile çalıştı mı?
