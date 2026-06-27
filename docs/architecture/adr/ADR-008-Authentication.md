# ADR-008 — Authentication & Identity

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS kurumsal müşterilere SaaS olarak sunulur; kimlik doğrulama hem local kullanıcılar hem kurumsal IdP (LDAP, Azure AD, OIDC) entegrasyonlarını desteklemelidir. Zero Trust prensibi (`SECURITY_ARCHITECTURE.md`) hiçbir isteğin varsayılan güvenilmemesini gerektirir. Authorization (RBAC/ABAC) ayrı ADR kapsamında `SECURITY_AUTHORIZATION.md`'de tanımlıdır; bu ADR kimlik doğrulama katmanına odaklanır.

---

## Decision

**Kimlik yönetimi** BOS Kernel'de merkezi olarak yönetilir.

**Desteklenen kimlik kaynakları:**

- Local User (username/password)
- LDAP / Active Directory
- Azure AD
- OpenID Connect / OAuth2
- SAML

**Desteklenen authentication yöntemleri:**

| Yöntem | Kullanım |
|---|---|
| **JWT (Bearer)** | Web/API oturum token'ı |
| **Username / Password + BCrypt** | Local auth |
| **MFA / FIDO2 / Passkey** | Yüksek güvenlik (yol haritası) |
| **API Key** | Servis entegrasyonları |
| **Service Account** | Background worker / sistem |

**JWT claim standardı (minimum):**

- `sub` (UserId)
- `tenant_id` (TenantId)
- `roles`
- `permissions` (veya permission endpoint ile lazy load)

**Güvenlik kuralları:**

1. Token'lar **httpOnly, Secure, SameSite=Strict** cookie'de saklanmalıdır (localStorage yasak — SECURITY_REVIEW bulgusu).
2. Her API isteği JWT doğrulamasından geçer; `[AllowAnonymous]` yalnızca public endpoint'lerde.
3. 401 (kimlik yok/geçersiz) vs 403 (yetki yetersiz) ayrımı zorunlu.
4. Secret/key rotation ve environment-based configuration; hardcoded secret yasak.
5. Rate limiting: login ve token endpoint'lerinde agresif limit.

---

## Consequences

**Pozitif:**

- Kurumsal IdP entegrasyonu ile SSO.
- JWT claims üzerinden tenant + permission context taşınır.
- Zero Trust ile defense-in-depth.

**Negatif:**

- Cookie-based auth SPA/CORS yapılandırması dikkat gerektirir.
- MFA/Passkey implementasyonu ek geliştirme.
- IdP çeşitliliği test matrisini genişletir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Session-only (no JWT)** | API/mobile/AI agent entegrasyonunda stateless avantaj kaybı. |
| **localStorage JWT** | XSS ile token çalınması riski (SECURITY_REVIEW CRITICAL). |
| **API Key only** | İnsan kullanıcı oturumu için uygun değil. |
| **Custom auth protocol** | Standart OIDC/OAuth2 ekosistem uyumu tercih edildi. |

---

## References

- [SECURITY_ARCHITECTURE.md](../../../SECURITY_ARCHITECTURE.md)
- [SECURITY_AUTHORIZATION.md](../../../SECURITY_AUTHORIZATION.md)
- [SECURITY_REVIEW.md](../../project-management/security/SECURITY_REVIEW.md)
- [DOMAIN_MODEL.md](../../../DOMAIN_MODEL.md)
- [API_STANDARDLARI.md](../../../API_STANDARDLARI.md)
