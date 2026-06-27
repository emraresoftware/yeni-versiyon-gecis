# A3: Finans ve Muhasebe Görev Kutusu

Bu dosya, **A3 (Finans ve Muhasebe)** modüllerini geliştirecek olan ajanın rehberidir.

---

## 🎯 Modül Kapsamı: Hesap Planı, Yevmiye Fişleri, Kasa/Banka & e-Fatura Yönetimi

Şirketin tek düzen hesap planını, çift taraflı kayıt (double-entry) muhasebe sistemini, yevmiye fişlerini ve banka/kasa işlemlerini kapsar.

---

## 💾 1. Veritabanı Şeması (Database Schema Specs)

Aşağıdaki entity sınıfları **`src/EmareTicket.Domain/Entities/Elyaf/`** altında oluşturulmalıdır:

### FinanceAccountPlan.cs (Hesap Planı - Tek Düzen)
```csharp
using System;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class FinanceAccountPlan : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string Code { get; set; } = null!; // Örn: 100, 100.01, 102
    public string Name { get; set; } = null!;
    public string Type { get; set; } = null!; // Asset, Liability, Equity, Revenue, Cost, Expense
    public string NormalBalance { get; set; } = null!; // Debit, Credit
    public int Level { get; set; } // Hiyerarşi Seviyesi (1, 2, 3...)
    public string? ParentCode { get; set; }
    public bool IsActive { get; set; } = true;
    public bool IsSystem { get; set; } = false;
}
```

### FinanceJournalEntry.cs (Yevmiye Fişi Başlığı)
```csharp
using System;
using System.Collections.Generic;
using EmareTicket.Domain.Common;

namespace EmareTicket.Domain.Entities.Elyaf;

public class FinanceJournalEntry : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid TenantId { get; set; }
    public string EntryNo { get; set; } = null!; // YV-YYYY-00001
    public DateTime Date { get; set; }
    public string? Description { get; set; }
    public string Type { get; set; } = "Manual"; // Opening, Sale, Purchase, Expense, Manual, Closing
    public bool IsPosted { get; set; } = false; // Deftere nakledildi mi?

    public ICollection<FinanceJournalEntryLine> Lines { get; set; } = new List<FinanceJournalEntryLine>();
}
```

### FinanceJournalEntryLine.cs (Yevmiye Fişi Satırları)
```csharp
using System;

namespace EmareTicket.Domain.Entities.Elyaf;

public class FinanceJournalEntryLine
{
    public Guid Id { get; set; }
    public Guid FinanceJournalEntryId { get; set; }
    public FinanceJournalEntry FinanceJournalEntry { get; set; } = null!;
    public string AccountCode { get; set; } = null!;
    public string? Description { get; set; }
    public decimal Debit { get; set; } // Borç Tutarı
    public decimal Credit { get; set; } // Alacak Tutarı
    public int LineOrder { get; set; }
}
```

---

## 🔑 2. Çift Taraflı Kayıt (Double-Entry) Kontrolü (Business Rules)

- **Bakiye Eşitliği Zorunluluğu:** Fiş kaydedilirken/onaylanırken **Toplam Borç (Debit) = Toplam Alacak (Credit)** olmak zorundadır. Fark sıfır olmalıdır, aksi halde `Result.Failure("Journal entry is not balanced")` dönmelidir.
- **Tutar Pozitifliği:** `Debit` ve `Credit` değerleri negatif olamaz, en az biri sıfırdan büyük olmalıdır.
- **Tarih Geçerliliği:** Geçmiş döneme fiş girilemez (Postgres DateTime UTC kontrolü).

---

## 🔌 3. REST API Sözleşmesi (Endpoints)

Tüm endpoints **`src/EmareTicket.API/Controllers/ControlTower/FinanceController.cs`** altında bulunmalıdır:

- **`GET /api/control-tower/finance/accounts`** -> `Result<List<FinanceAccountPlanDto>>`
- **`POST /api/control-tower/finance/accounts`** -> body: `{ Code, Name, Type, NormalBalance, ParentCode }`
- **`GET /api/control-tower/finance/entries`** -> `Result<PagedList<FinanceJournalEntryDto>>`
- **`POST /api/control-tower/finance/entries`** -> body: `{ Date, Description, Type, Lines: [{ AccountCode, Description, Debit, Credit }] }`
- **`POST /api/control-tower/finance/entries/{id}/post`** -> Fişi deftere nakleder (onaylar).

---

## 🎨 4. Frontend Arayüz Gerekleri (Next.js 16)

- **Hesap Planı Ağacı (Chart of Accounts):** `web/src/app/control-tower/finance/accounts/page.tsx`
  - Hiyerarşik ağaç görünümlü (Collapsible tree list), arama filtreli, doğrudan alt hesap eklemeyi sağlayan butonlar.
- **Yeni Fiş Girişi (Journal Entry Form):** `web/src/app/control-tower/finance/entries/new/page.tsx`
  - Grid satırlardan oluşan dinamik form. Alt tarafta anlık `Toplam Borç`, `Toplam Alacak` ve `Bakiye Farkı` hesaplayıcıları. Fark sıfır olmadığında Kaydet butonu pasif olmalıdır.

---

## 🧪 Sıfır Hata (Zero-Defect) Kontrol Listesi
1. [ ] **Veritabanı Migration:** `dotnet ef database update` sorunsuz çalıştı mı?
2. [ ] **Validation Unit Testleri:** Yevmiye fişlerinin denge (balancing) doğrulama logic'ini test eden en az 6 adet xUnit testi yazıldı mı?
3. [ ] **Frontend Derleme:** `npm run build` sıfır hata ile tamamlandı mı?
