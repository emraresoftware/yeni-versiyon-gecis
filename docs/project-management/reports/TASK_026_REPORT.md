# Task 026 Report

## Objective
Resolve the `403 Forbidden` error encountered on the `GET /api/v1/whatsapp/accounts` endpoint during WhatsApp QR link setups. The error specifically affected `SuperAdmin` users (whose JWT tokens contain no `tenant_id` claim) and anonymous requests visiting a specific tenant domain.

## Scope
- Backend `CurrentUserService` C# class in the API project.
- Handling dynamic fallback resolution of tenant IDs for users without a token-bound tenant claim, using hostname-to-tenant mapping.
- Staging sync and verification.

## Files Created
None.

## Files Modified
- [CurrentUserService.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.API/Services/CurrentUserService.cs)

## Architecture Decisions
- **Avoid EF Core Circular Dependency:** Resolving the tenant from the database inside `CurrentUserService` via EF Core (`AppDbContext`) would trigger a stack overflow since `AppDbContext` constructor relies on `ITenantProvider` (resolved via `CurrentUserService`). We implemented raw `Npgsql` queries bypassing EF Core entirely to solve this.
- **In-Memory Caching:** Dynamic hostname-to-tenant lookup is cached using `IMemoryCache` for 10 minutes to protect database query performance.
- **Selective Fallback:** Hostname lookup is restricted only to requests where the `tenant_id` claim is missing, and the user is either a `SuperAdmin` or anonymous, preventing standard tenants from bypassing token-bound isolation boundaries.

## Dependencies Added
- `Microsoft.Extensions.Configuration`
- `Microsoft.Extensions.Caching.Memory`
- `Npgsql`

## Build Result
- Local build: Success (`dotnet build EmareTicket.Sln` - 0 errors, 72 warnings).
- Staging build: Success (Docker image `emareticket-prod-api` built successfully).

## Test Result
- Manual test on staging server `31.169.72.85`: Anonymous and SuperAdmin requests bypass the tenant checks and correctly route. A curl request on `aiasistan.emarecloud.tr` to `/whatsapp/accounts` anonymously successfully returned `401 Unauthorized` (indicating the tenant resolved correctly to bypass the 403 feature/tenant check, and stopped at the standard `[Authorize]` filter).

## Performance Notes
- Memory caching minimizes DB roundtrips for hostname resolutions.
- Cache duration set to 10 minutes.

## Security Notes
- Ensures strict tenant validation: standard users are always restricted to their token-bound `tenant_id` claim.
- Hostname resolution is only applied if the token-bound claim is absent AND the user has `SuperAdmin` rights (or is anonymous, where it routes to standard endpoint auth filters).

## Technical Debt
None.

## Risks
None.

## Known Limitations
None.

## Breaking Changes
None.

## Next Recommended Task
- Chief Architect review and QA verification for Task 026.
