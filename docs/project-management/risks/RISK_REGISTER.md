# Risk Register

**Owner:** Agent 2  
**Son güncelleme:** 2026-06-27  
**Format (v1.0):** Id · Risk · Severity · Status · Owner

| Id | Risk | Severity | Status | Owner |
| -- | ---- | -------- | ------ | ----- |
| R-001 | Emare BOS tenant filter — auth regresyon, Permission istisnası eksik | High | Open | Agent 1 |
| R-002 | IRepository AggregateRoot vs entity hizalama | High | Open | Agent 1 |
| R-003 | Application / Infrastructure tamamlanmamış alanlar | Medium | Open | Agent 1 |
| R-004 | Persistence PostgreSQL integration test yok | Medium | Open | Agent 2 |
| R-005 | EF config eksikleri (UserRole, RolePermission, AuditLog) | Medium | Resolved | Agent 1 |
| R-006 | DateTime.Now kullanımı (Platform API) | Low | Resolved | Agent 1 |
| R-007 | Prod migration PlatformFeedbacks çakışması | Medium | Open | Ops |
| R-008 | CDR sidebar menü linki eksik | Low | Open | Agent 1 |
| R-009 | Reseller müşteri CRUD 403 | Medium | Resolved | Agent 1 |
| R-010 | Global permission Guid.Empty tenant filter sonrası kaybolma | Medium | Open | Architect |
| R-011 | Corvis NS Cloudflare taşınması bekliyor | Low | Open | Ops |

**Severity:** Critical · High · Medium · Low  
**Status:** Open · Mitigated · Resolved

---

## Ekleme kuralı

Yeni risk Agent 2 tarafından eklenir; daily log'a kısa not. QA Critical Issues ile hizalanır.
