# Technical Debt Register

**Owner:** Agent 2  
**Son güncelleme:** 2026-06-27  
**Format (v1.0):** Id · Debt · Reason · Planned Sprint

| Id | Debt | Reason | Planned Sprint |
| -- | ---- | ------ | -------------- |
| TD-001 | EF tenant filter auth bypass + Permission istisnası | 004A kısmen; login/register kırık | Sprint 1 |
| TD-002 | AggregateRoot vs BaseAuditableEntity hizalama | Erken repository arayüzü | Sprint 0 |
| TD-003 | Application CQRS + Infrastructure impl. | Sprint sırası | Sprint 1 |
| TD-004 | ApiResponse Shared Kernel'de | Hızlı bootstrap | Sprint 1 |
| TD-005 | MediatR referansı BuildingBlocks.Common'da | Scaffold kolaylığı | Sprint 1 |
| TD-006 | ENTITY_STANDARDLARI audit alan adları | Kod önce üretildi | Sprint 0 |
| TD-007 | PostgreSQL persistence integration test | Yalnızca SQLite test | Sprint 1 |
| TD-008 | WeatherForecast API şablonu | dotnet new varsayılanı | Resolved |
| TD-009 | UserRole / RolePermission domain event | Minimal entity seti | Sprint 1 |
| TD-010 | EmareTicket birleşik migration | Hızlı prod unblock | Sprint 1 |
| TD-011 | Prod gereksiz standalone kopyalar | Canlı trafik önceliği | Ops |
| TD-012 | CDR sidebar menü linki | MVP dropdown yeterli | Sprint 1 |

---

## Ekleme kuralı

Agent 1 veya QA borcu tespit eder → Agent 2 ekler. Kapatıldığında daily log'a not. R-xxx ile çapraz referans.
