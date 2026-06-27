# Task 004 Report

## Objective

Bu taskın amacı, Emare BOS platform domain entity'leri (`Tenant`, `ApplicationUser`, `Role`, `Permission`, `UserRole`, `RolePermission`, `AuditLog`) için EF Core Persistence (veritabanı erişim) altyapısının kurulmasıdır.

---

## Files Created

- [EmareDbContext.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/DbContext/EmareDbContext.cs)
- [AuditableEntitySaveChangesInterceptor.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/Interceptors/AuditableEntitySaveChangesInterceptor.cs)
- [SoftDeleteSaveChangesInterceptor.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/Interceptors/SoftDeleteSaveChangesInterceptor.cs)
- [PersistenceDependencyInjection.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/PersistenceDependencyInjection.cs)
- [EfRepository.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/Repositories/EfRepository.cs)
- [UnitOfWork.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/Repositories/UnitOfWork.cs)
- [PersistenceTests.cs](file:///Users/emre/Elyafgroup/tests/Emare.Platform.Persistence.Tests/PersistenceTests.cs)
- Configurations:
  - `TenantConfiguration.cs`
  - `ApplicationUserConfiguration.cs`
  - `RoleConfiguration.cs`
  - `PermissionConfiguration.cs`
  - `UserRoleConfiguration.cs`
  - `RolePermissionConfiguration.cs`
  - `AuditLogConfiguration.cs`

---

## Files Modified

- [Emare.sln](file:///Users/emre/Elyafgroup/Emare.sln) (Test projesi dahil edildi)
- [BaseAuditableEntity.cs](file:///Users/emre/Elyafgroup/src/BuildingBlocks/Common/Entities/BaseAuditableEntity.cs) (Multiple inheritance engelini aşmak için `AggregateRoot`'tan türetildi)

---

## Architecture Decisions

- **Save Changes Interceptors:** Denetim izi (`IAuditable`) ve yumuşak silme (`ISoftDelete`) kuralları DB SaveChanges adımlarında interceptor'lar vasıtasıyla otomatik işletilir.
- **AuditLog Immutability:** `AuditLog` kayıtları değiştirilemez kılındı. Güncelleme veya silme işlemleri interceptor'da engellenip `InvalidOperationException` fırlatılır.
- **SQLite RowVersion Uyumlaştırması:** SQLite üzerinde `byte[]` row version kolonu veritabanı tarafından otomatik doldurulmadığından, C# default byte dizisi atanarak insert hataları çözüldü. Bu doğrultuda `RowVersion` özelliği nullable yapıldı.

---

## Dependencies

- `Npgsql.EntityFrameworkCore.PostgreSQL` v8.0.11
- `Microsoft.EntityFrameworkCore.Sqlite` v8.0.11 (Tests)

---

## Build Result

```text
Oluşturma başarılı oldu.
    0 Uyarı
    0 Hata
```

---

## Test Result

```text
Başarılı!  - Başarısız:     0, Başarılı:    11, Atlanan:     0, Toplam:    11, Süre: 946 ms - Emare.Platform.Persistence.Tests.dll (net8.0)
```

---

## Security Notes

- SQL Injection riskine karşı EF Core Parametrik LINQ / Raw SQL yapıları ve Fluent API sınırlandırmaları kullanıldı.

---

## Technical Debt

- PostgreSQL xmin ve SQLite RowVersion davranışı arasındaki farklılıkların Fluent API'de conditional (SQLite kontrolü) olarak ele alınması.

---

## Risks

- Concurrency kontrolleri SQLite in-memory testlerinde PostgreSQL kadar katı şekilde simüle edilememektedir.

---

## Next Recommended Task

- Task 004A: Persistence QA Findings (Multi-tenancy global query filters)
