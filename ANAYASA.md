# 📜 Emare Kod Kalitesi Anayasası

**Title:** Emare Kod Kalitesi Anayasası
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** Yok
**Related Documents:** ORTAK_TEKNIK_PROTOKOL.md, ERD_MODEL.md, DOMAIN_MODEL.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Bu dosya, projede kod geliştiren tüm yapay zeka ajanlarının uymakla yükümlü olduğu **değişmez kurallar bütünüdür**. Herhangi bir ajan tarafından bu kuralların çiğnenmesi kabul edilemez ve doğrudan derleme/çalışma hatası olarak kabul edilir.

---

## Kapsam

C# Backend, React Frontend, veritabanı sorguları ve white-labeling yapılandırması.

---

## Hedef Kitle

Geliştiriciler, AI Ajanları.

---

## ARTICLE 1

No AI agent is allowed to generate code before reading AGENTS.md.

Violation of this rule invalidates the task.

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
Bağımlılık yönü her zaman içe (Domain katmanına) doğrudur. 

Referans Akışı:
`Web / UI` ➡️ `API` ➡️ `Infrastructure` & `Persistence` ➡️ `Application` ➡️ `Domain` (Bağımsız Çekirdek).

**5 Kritik Katman Yasağı:**
1. **Controller ➡️ DbContext Yasaktır:** Veritabanı DbContext'i API Controller'lar içinde doğrudan kullanılamaz.
2. **UI ➡️ Entity Yasaktır:** Arayüz katmanı Domain Entity sınıflarını doğrudan referans alamaz.
3. **Domain ➡️ Infrastructure Yasaktır:** Domain katmanı altyapı sınıflarına bağımlı olamaz.
4. **Application ➡️ Infrastructure Implementation Yasaktır:** Uygulama somut altyapı uygulamalarına bağımlı olamaz.
5. **Domain ➡️ Hiçbir Katmana Bağımlı Olamaz:** Domain en iç katmandır, dışındaki hiçbir katmanı bilemez.

Detaylar için bkz. [ADR-0002 — Clean Architecture](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/docs/adr/0002-clean-architecture.md).
