# 📜 Emare Kod Kalitesi Anayasası (ANAYASA.md)

Bu dosya, projede kod geliştiren tüm yapay zeka ajanlarının uymakla yükümlü olduğu **değişmez kurallar bütünüdür**. Herhangi bir ajan tarafından bu kuralların çiğnenmesi kabul edilemez ve doğrudan derleme/çalışma hatası olarak kabul edilir.

---

## 1. DateTime + PostgreSQL Kuralı (Kritik!)

PostgreSQL `timestamptz` veri tipiyle çalışırken .NET runtime tarafında kesinlikle **`DateTimeKind.Utc`** kullanılmalıdır. Aksi takdirde, veritabanına kayıt veya LINQ sorgularında **Npgsql runtime 500 hatası** alınır.

```csharp
// ❌ YANLIŞ (Npgsql hatası verir)
entity.CreatedAt = DateTime.Now;

// ✅ DOĞRU
entity.CreatedAt = DateTime.UtcNow;

// ✅ DOĞRU (Ham tarihlerde kind belirtme)
var d = DateTime.SpecifyKind(rawDate, DateTimeKind.Utc);
```

---

## 2. Hata Fırlatmama & Result Pattern
- Kod içinde doğrudan `throw new Exception()` yapısı **kullanılmamalıdır**.
- Backend katmanında fonksiyonlar `Result<T>` veya `Result` (başarı/başarısızlık durumunu dönen ortak tip) döndürmelidir.
- API Controller katmanı bunu yakalayarak `ApiResponse` sınıfı ile sarmalamalıdır.

---

## 3. Asenkron (Async/Await) ve İptal Mekanizmaları
- Tüm I/O ve veritabanı işlemleri asenkron (`async/await`) olarak kodlanmalıdır.
- Tüm asenkron metotlara mutlaka `CancellationToken ct` parametresi geçilmeli ve bu parametre EF Core sorgularına iletilmelidir (`ToListAsync(ct)` vb.).

---

## 4. White-Labeling (Marka Bağımsızlaştırma) Kuralları
- Kod tabanına hiçbir sabit marka adı (`elyaf-group`, `elyafgroup` vb.) **sert kodlanmamalıdır (hardcoded)**.
- **Backend Kiracı (Tenant) Doğrulaması:** Kiracı slug doğrulamalarında `Environment.GetEnvironmentVariable("CONTROL_TOWER_TENANT_SLUG") ?? "elyaf-group"` yapısı kullanılmalıdır.
- **Frontend Kiracı Doğrulaması:** `process.env.NEXT_PUBLIC_CONTROL_TOWER_TENANT_SLUG || "elyaf-group"` kullanılmalıdır.
- **Frontend Başlık ve Markalama:** Arayüzdeki marka ve başlık isimleri `process.env.NEXT_PUBLIC_BRAND_NAME` üzerinden okunmalıdır.
- **Ulaşım Yolları:** URL rotalarında `/elyaf/` gibi markaya özel isimler yerine marka bağımsız `/control-tower/` prefix'i kullanılmalıdır.

---

## 5. Clean Architecture Bağımlılık Yönü
Bağımlılık yönü her zaman içe doğrudur:
`Domain` (en iç - hiçbir bağımlılığı yok) ➡️ `Application` ➡️ `Infrastructure` & `Persistence` ➡️ `API` (en dış).
İç katmanlar dış katmanlardaki hiçbir sınıfa doğrudan bağımlı olamaz (örneğin Domain, Application veya Persistence katmanına referans veremez).
