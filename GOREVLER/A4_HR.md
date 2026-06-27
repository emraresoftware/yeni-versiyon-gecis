# A4: Personel ve İK Görev Kutusu

Bu dosya, **A4 (Personel ve İK)** modüllerini geliştirecek olan ajanın rehberidir.

---

## 🎯 Modül Kapsamı: Personel Kartları, İzin Talepleri & Onay Akışları

Şirket personel kartları, izin tanımları, çalışan izin hak edişleri ve talep-onay iş akışlarını yönetir.

---

## 💾 1. Veritabanı Şeması (Database Schema Specs)

Aşağıdaki entity sınıfları **`src/EmareTicket.Domain/Entities/Elyaf/`** altında oluşturulmalıdır:

### HrEmployee.cs (Personel Kartı)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class HrEmployee : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string FirstName { get; set; } = null!;
    public string LastName { get; set; } = null!;
    public string IdentityNumber { get; set; } = null!; // TCKN veya Pasaport
    public string Email { get; set; } = null!;
    public string? Phone { get; set; }
    public string Department { get; set; } = null!;
    public string JobTitle { get; set; } = null!;
    public DateTime HireDate { get; set; }
    public bool IsActive { get; set; } = true;
    public decimal AnnualLeaveBalance { get; set; } // Kalan yıllık izin gün hak edişi
}
```

### HrLeaveType.cs (İzin Tipleri)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class HrLeaveType : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string Name { get; set; } = null!; // Yıllık İzin, Raporlu, Ücretsiz İzin vb.
    public int DaysPerYear { get; set; }
    public bool RequiresApproval { get; set; } = true;
    public string? Color { get; set; } // Takvimde gösterim için hex renk kodu
}
```

### HrLeave.cs (İzin Talepleri)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class HrLeave : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public Guid HrEmployeeId { get; set; }
    public HrEmployee HrEmployee { get; set; } = null!;
    public Guid HrLeaveTypeId { get; set; }
    public HrLeaveType HrLeaveType { get; set; } = null!;
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
    public decimal Days { get; set; } // Toplam gün (Örn: 2.5 gün)
    public string Status { get; set; } = "Pending"; // Pending, Approved, Rejected, Cancelled
    public string? Notes { get; set; }
    public string? RejectionReason { get; set; }
    public Guid? ApproverUserId { get; set; }
    public DateTime? ApprovedAt { get; set; }
}
```

---

## 🔑 2. İzin Hak Ediş Kuralları (Business Rules)

- **Bakiye Kontrolü:** Çalışan yıllık izin (yıllık izin tipi seçildiğinde) talebinde bulunduğunda, talep edilen gün sayısı çalışanın `AnnualLeaveBalance` değerinden fazla olamaz. Aksi halde talep onaylanamaz.
- **Bakiye Düşümü:** Talebin durumu `Approved` (Onaylandı) yapıldığında, çalışanın `AnnualLeaveBalance` değeri talep edilen gün sayısı kadar düşürülmelidir.
- **Tarih Geçerliliği:** Başlangıç tarihi bitiş tarihinden büyük veya eşit olamaz.

---

## 🔌 3. REST API Sözleşmesi (Endpoints)

Tüm endpoints **`src/EmareTicket.API/Controllers/ControlTower/HrController.cs`** altında bulunmalıdır:

- **`GET /api/control-tower/hr/employees`** -> `Result<PagedList<HrEmployeeDto>>`
- **`POST /api/control-tower/hr/employees`** -> body: `{ FirstName, LastName, IdentityNumber, Email, Department, JobTitle, HireDate }`
- **`GET /api/control-tower/hr/leaves`** -> `Result<PagedList<HrLeaveDto>>`
- **`POST /api/control-tower/hr/leaves`** -> body: `{ HrEmployeeId, HrLeaveTypeId, StartDate, EndDate, Days, Notes }`
- **`POST /api/control-tower/hr/leaves/{id}/approve`** -> Talebi onaylar ve bakiye günceller.
- **`POST /api/control-tower/hr/leaves/{id}/reject`** -> body: `{ Reason }` -> Talebi reddeder.

---

## 🎨 4. Frontend Arayüz Gerekleri (Next.js 16)

- **İK Paneli:** `web/src/app/control-tower/hr/page.tsx`
  - Çalışan kartları listesi, aktif izinliler listesi, onay bekleyen izin talepleri listesi.
- **İzin Takvimi:** `web/src/app/control-tower/hr/calendar/page.tsx`
  - Departman bazlı izinli personelleri gösteren FullCalendar/Shadcn Calendar görünümü.

---

## 🧪 Sıfır Hata (Zero-Defect) Kontrol Listesi
1. [ ] **Veritabanı Migration:** `dotnet ef database update` sorunsuz çalıştı mı?
2. [ ] **Hak Ediş Testleri:** Yıllık izin onaylandığında çalışanın kalan bakiye hesaplamalarını test eden en az 5 adet xUnit testi yazıldı mı?
3. [ ] **Frontend Derleme:** `npm run build` sıfır hata ile tamamlandı mı?
