# A6: Kalite Kontrol Görev Kutusu

Bu dosya, **A6 (Kalite Kontrol)** modüllerini geliştirecek olan ajanın rehberidir.

---

## 🎯 Modül Kapsamı: Kalite Standartları, Müşteri Şikayetleri & Test Raporları

Ürün kalite kontrol test tanımları, üretim bantlarındaki test sonuçları ve müşterilerden gelen kalite/hata şikayet iadelerini yönetir.

---

## 💾 1. Veritabanı Şeması (Database Schema Specs)

Aşağıdaki entity sınıfları **`src/EmareTicket.Domain/Entities/Elyaf/`** altında oluşturulmalıdır:

### QcStandard.cs (Ürün Kalite Standardı)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class QcStandard : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string ProductCode { get; set; } = null!;
    public string TestType { get; set; } = null!; // TensileStrength, ColorMatch, Thickness, WeightConsistency
    public string ExpectedValue { get; set; } = null!; // Beklenen test değeri veya aralığı
    public string ToleranceRange { get; set; } = null!; // Hata tolerans aralığı (+-%5, Min/Max)
}
```

### QcTestResult.cs (Üretim Kalite Test Sonucu)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class QcTestResult : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string BatchNumber { get; set; } = null!; // Üretim lot/parti numarası
    public string ProductCode { get; set; } = null!;
    public int TestedQuantity { get; set; }
    public int FailedQuantity { get; set; }
    public string Result { get; set; } = "Pass"; // Pass, Fail, Rework
    public string? Notes { get; set; }
    public string? InspectorName { get; set; }
}
```

### QcClaim.cs (Müşteri Kalite Şikayeti / İade Talebi)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class QcClaim : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public Guid CrmAccountId { get; set; } // Şikayetçi Müşteri (CrmAccount)
    public string OrderNo { get; set; } = null!; // İlişkili Sipariş No
    public string ProductCode { get; set; } = null!;
    public decimal ClaimQuantity { get; set; }
    public string IssueDescription { get; set; } = null!;
    public string Status { get; set; } = "Pending"; // Pending, Investigating, Approved, Rejected, Resolved
    public string? ActionTaken { get; set; } // Uygulanan çözüm aksiyonu (Hurda, İade Faturası vb.)
}
```

---

## 🔌 2. REST API Sözleşmesi (Endpoints)

Tüm endpoints **`src/EmareTicket.API/Controllers/ControlTower/QcController.cs`** altında bulunmalıdır:

- **`GET /api/control-tower/qc/standards`** -> `Result<List<QcStandardDto>>`
- **`POST /api/control-tower/qc/standards`** -> body: `{ ProductCode, TestType, ExpectedValue, ToleranceRange }`
- **`GET /api/control-tower/qc/tests`** -> `Result<PagedList<QcTestResultDto>>`
- **`POST /api/control-tower/qc/tests`** -> body: `{ BatchNumber, ProductCode, TestedQuantity, FailedQuantity, Result, Notes }`
- **`GET /api/control-tower/qc/claims`** -> `Result<PagedList<QcClaimDto>>`
- **`POST /api/control-tower/qc/claims`** -> body: `{ CrmAccountId, OrderNo, ProductCode, ClaimQuantity, IssueDescription }`
- **`PUT /api/control-tower/qc/claims/{id}/status`** -> body: `{ Status, ActionTaken }`

---

## 🎨 3. Frontend Arayüz Gerekleri (Next.js 16)

- **Kalite Şikayetleri:** `web/src/app/control-tower/qc/claims/page.tsx`
  - Müşteri şikayet ve iade talep formu. Şikayet durumuna göre (Örn: Investigating: Sarı, Approved: Yeşil, Rejected: Kırmızı) HSL renk etiketleri.
- **Üretim Test Sonuçları (ASR / QC Tests):** `web/src/app/control-tower/qc/tests/page.tsx`
  - Hatalı üretim oranlarını (Fail rate) gösteren mini analitik kartlar, lot numarası bazlı arama.

---

## 🧪 Sıfır Hata (Zero-Defect) Kontrol Listesi
1. [ ] **Veritabanı Migration:** `dotnet ef database update` sorunsuz çalıştı mı?
2. [ ] **Hata Oranı Testleri:** Test sonuçlarında `FailedQuantity` > `TestedQuantity` olamayacağını denetleyen xUnit testi yazıldı mı?
3. [ ] **Frontend Derleme:** `npm run build` sıfır hata ile tamamlandı mı?
