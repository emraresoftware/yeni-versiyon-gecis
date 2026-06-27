# A7: Lojistik ve Sevkiyat Görev Kutusu

Bu dosya, **A7 (Lojistik ve Sevkiyat)** modüllerini geliştirecek olan ajanın rehberidir.

---

## 🎯 Modül Kapsamı: Stok Hareketleri, Depolar Arası Transferler & Sevkiyatlar

Depo tanımları, depo stok seviyeleri, FIFO stok giriş/çıkış hareketleri ve çift onay gerektiren depolar arası ürün transferlerini yönetir.

---

## 💾 1. Veritabanı Şeması (Database Schema Specs)

Aşağıdaki entity sınıfları **`src/EmareTicket.Domain/Entities/Elyaf/`** altında oluşturulmalıdır:

### LogisticsWarehouse.cs (Depolar)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class LogisticsWarehouse : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string Code { get; set; } = null!; // Örn: DEP-01
    public string Name { get; set; } = null!;
    public string? Address { get; set; }
    public bool IsActive { get; set; } = true;
}
```

### LogisticsStockMovement.cs (Stok Hareketleri)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class LogisticsStockMovement : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public Guid LogisticsWarehouseId { get; set; }
    public LogisticsWarehouse LogisticsWarehouse { get; set; } = null!;
    public string ProductCode { get; set; } = null!;
    public string MovementType { get; set; } = null!; // In (Giriş), Out (Çıkış)
    public decimal Quantity { get; set; }
    public string ReferenceNo { get; set; } = null!; // İrsaliye No, Fiş No vb.
    public string? Description { get; set; }
}
```

### LogisticsStockTransfer.cs (Depolar Arası Transfer Başlığı)
```csharp
using System;
using System.Collections.Generic;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class LogisticsStockTransfer : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string TransferNo { get; set; } = null!; // TRF-00001
    public Guid SourceWarehouseId { get; set; }
    public LogisticsWarehouse SourceWarehouse { get; set; } = null!;
    public Guid TargetWarehouseId { get; set; }
    public LogisticsWarehouse TargetWarehouse { get; set; } = null!;
    public string Status { get; set; } = "Pending"; // Pending, Approved, Completed, Rejected
    public string? Reason { get; set; }

    public ICollection<LogisticsStockTransferLine> Lines { get; set; } = new List<LogisticsStockTransferLine>();
}
```

### LogisticsStockTransferLine.cs (Transfer Kalemleri)
```csharp
using System;

namespace EmareTicket.Domain.Entities.Elyaf;

public class LogisticsStockTransferLine
{
    public Guid Id { get; set; }
    public Guid LogisticsStockTransferId { get; set; }
    public LogisticsStockTransfer LogisticsStockTransfer { get; set; } = null!;
    public string ProductCode { get; set; } = null!;
    public decimal Quantity { get; set; }
}
```

---

## 🔑 2. Depo Transfer Onay Mantığı (Business Rules)

- **Stok Bakiye Kontrolü:** Transfer onaylandığında, kaynak depoda (`SourceWarehouseId`) gönderilmek istenen miktarda yeterli stok bakiye (`LogisticsStockMovement` toplamları) bulunup bulunmadığı kontrol edilmelidir. Yetersiz stokta `Result.Failure("Insufficient stock in source warehouse")` dönmelidir.
- **Çift Onay Akışı:** 
  1. Transfer `Pending` (Beklemede) başlar.
  2. Kaynak depo sorumlusu onaylayınca `Approved` olur.
  3. Hedef depo sorumlusu teslim aldığında `Completed` yapılır ve stok hareketleri (`Out` kaynak depoya, `In` hedef depoya) otomatik yazılır.

---

## 🔌 3. REST API Sözleşmesi (Endpoints)

Tüm endpoints **`src/EmareTicket.API/Controllers/ControlTower/LogisticsController.cs`** altında bulunmalıdır:

- **`GET /api/control-tower/logistics/warehouses`** -> `Result<List<LogisticsWarehouseDto>>`
- **`POST /api/control-tower/logistics/warehouses`** -> body: `{ Code, Name, Address }`
- **`GET /api/control-tower/logistics/transfers`** -> `Result<PagedList<LogisticsStockTransferDto>>`
- **`POST /api/control-tower/logistics/transfers`** -> body: `{ SourceWarehouseId, TargetWarehouseId, Reason, Lines: [{ ProductCode, Quantity }] }`
- **`POST /api/control-tower/logistics/transfers/{id}/approve`** -> Kaynak onay
- **`POST /api/control-tower/logistics/transfers/{id}/complete`** -> Hedef teslim onay (stok hareketlerini yazar).

---

## 🎨 4. Frontend Arayüz Gerekleri (Next.js 16)

- **Depolar ve Stok Durumu:** `web/src/app/control-tower/logistics/warehouses/page.tsx`
  - Depo bazlı ürün stok miktarlarını gösteren responsive listeler.
- **Stok Transferleri:** `web/src/app/control-tower/logistics/transfers/page.tsx`
  - Transfer talep formu ve onay bekleyen transferleri karşılayan yönetim paneli.

---

## 🧪 Sıfır Hata (Zero-Defect) Kontrol Listesi
1. [ ] **Veritabanı Migration:** `dotnet ef database update` sorunsuz çalıştı mı?
2. [ ] **Stok Entegrasyon Testleri:** Transfer `Completed` yapıldığında kaynak ve hedef depolardaki stok hareketlerinin doğru yazıldığını doğrulayan en az 6 adet xUnit testi yazıldı mı?
3. [ ] **Frontend Derleme:** `npm run build` sıfır hata ile tamamlandı mı?
