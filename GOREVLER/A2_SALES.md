# A2: Satış ve CRM Görev Kutusu

Bu dosya, **A2 (Satış ve CRM)** modüllerini geliştirecek olan ajanın rehberidir.

---

## 🎯 Modül Kapsamı: Müşteriler (Cariler), Fırsatlar ve Teklif Yönetimi

Müşteri profilleri, bu profiller altındaki ilgili kişiler, satış fırsatları ve fiyat teklifleri süreçlerini kapsar.

---

## 💾 1. Veritabanı Şeması (Database Schema Specs)

Aşağıdaki entity sınıfları **`src/EmareTicket.Domain/Entities/Elyaf/`** altında oluşturulmalıdır:

### CrmAccount.cs (Cari Hesaplar / Müşteriler)
```csharp
using System;
using System.Collections.Generic;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class CrmAccount : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string Code { get; set; } = null!; // CR-000001 formatında otomatik üretilir.
    public string Name { get; set; } = null!;
    public string? CommercialTitle { get; set; }
    public string Type { get; set; } = null!; // Musteri, Tedarikci, Partner, Rakip
    public string? TaxOffice { get; set; }
    public string? TaxNumber { get; set; }
    public string? Phone { get; set; }
    public string? Email { get; set; }
    public string? Address { get; set; }
    public string? City { get; set; }
    public string? Country { get; set; }
    public decimal CreditLimit { get; set; }
    public string CurrencyCode { get; set; } = "TRY";
    public bool IsActive { get; set; } = true;

    public ICollection<CrmContact> Contacts { get; set; } = new List<CrmContact>();
    public ICollection<CrmOpportunity> Opportunities { get; set; } = new List<CrmOpportunity>();
}
```

### CrmContact.cs (İlgili Kişiler)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class CrmContact : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public Guid CrmAccountId { get; set; }
    public CrmAccount CrmAccount { get; set; } = null!;
    public string FirstName { get; set; } = null!;
    public string LastName { get; set; } = null!;
    public string? Email { get; set; }
    public string? Phone { get; set; }
    public string? JobTitle { get; set; }
    public bool IsActive { get; set; } = true;
}
```

### CrmOpportunity.cs (Fırsatlar)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class CrmOpportunity : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public Guid CrmAccountId { get; set; }
    public CrmAccount CrmAccount { get; set; } = null!;
    public string Title { get; set; } = null!;
    public string Stage { get; set; } = null!; // New, Qualification, ProposalSent, Negotiation, Won, Lost
    public decimal Amount { get; set; }
    public string Currency { get; set; } = "TRY";
    public int Probability { get; set; } // Olasılık Yüzdesi (0-100)
    public DateTime? CloseDate { get; set; }
    public string? Description { get; set; }
}
```

### CrmProposal.cs (Teklifler)
```csharp
using System;
using System.Collections.Generic;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class CrmProposal : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string ProposalNo { get; set; } = null!; // PR-YYYY-00001 formatında otomatik üretilir.
    public Guid CrmAccountId { get; set; }
    public CrmAccount CrmAccount { get; set; } = null!;
    public string Title { get; set; } = null!;
    public string Status { get; set; } = null!; // Draft, Sent, Approved, Declined
    public DateTime ExpiryDate { get; set; }
    public decimal SubTotal { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal TotalAmount { get; set; }
    public string Currency { get; set; } = "TRY";
    public string? Terms { get; set; }

    public ICollection<CrmProposalItem> Items { get; set; } = new List<CrmProposalItem>();
}
```

### CrmProposalItem.cs (Teklif Kalemleri)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class CrmProposalItem
{
    public Guid Id { get; set; }
    public Guid CrmProposalId { get; set; }
    public CrmProposal CrmProposal { get; set; } = null!;
    public string Description { get; set; } = null!;
    public decimal Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal LineTotal { get; set; }
}
```

---

## 🔌 2. REST API Sözleşmesi (Endpoints)

Tüm endpoints **`src/EmareTicket.API/Controllers/ControlTower/CrmController.cs`** altında bulunmalıdır:

- **`GET /api/control-tower/crm/accounts`** -> `Result<PagedList<CrmAccountDto>>`
- **`POST /api/control-tower/crm/accounts`** -> body: `{ Name, CommercialTitle, Type, ... }`
- **`GET /api/control-tower/crm/opportunities`** -> `Result<PagedList<CrmOpportunityDto>>`
- **`POST /api/control-tower/crm/opportunities`** -> body: `{ CrmAccountId, Title, Stage, Amount, Probability, ... }`
- **`GET /api/control-tower/crm/proposals`** -> `Result<PagedList<CrmProposalDto>>`
- **`POST /api/control-tower/crm/proposals`** -> body: `{ CrmAccountId, Title, ExpiryDate, Items: [{ Description, Quantity, UnitPrice }] }`

---

## 🎨 3. Frontend Arayüz Gerekleri (Next.js 16)

Arayüz modülleri modern responsive tasarım, tablar ve filtreleme kriterleri ile zenginleştirilmelidir:

- **Müşteriler (Cariler):** `web/src/app/control-tower/sales/customers/page.tsx`
  - Müşteri listesi, yeni müşteri tanımlama, limit ve borç takibi.
- **Fırsatlar (Opportunities):** `web/src/app/control-tower/sales/opportunities/page.tsx`
  - Kazanma ihtimali (Probability) barı, satış hacmi grafiksel kanban görünümü (Shadcn UI Drag and Drop).
- **Teklifler (Proposals):** `web/src/app/control-tower/sales/proposals/page.tsx`
  - Teklif formu, kalem bazlı dinamik ekleme/çıkarma, ara toplam, vergi ve indirimlerin otomatik hesaplanması.

---

## 🧪 Sıfır Hata (Zero-Defect) Kontrol Listesi
1. [ ] **Veritabanı Migration:** `dotnet ef database update` sorunsuz çalıştı mı?
2. [ ] **Backend Testleri:** `tests/EmareTicket.Tests` altında en az 8 adet xUnit test senaryosu yazıldı ve `dotnet test` sıfır hata ile tamamlandı mı?
3. [ ] **Frontend Derleme:** `npm run build` ve `npm run lint` komutları sıfır hata ile çalıştı mı?
