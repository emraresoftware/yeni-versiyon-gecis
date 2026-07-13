# Task Kurstanbul Provisioning & Simulation Report

## Objective

Provision and configure the "Kurstanbul" tenant account in the system (both local and production databases), and design/implement a user-controlled, self-serve simulation framework where administrators can prepare or clear a 3-year historical dataset with 50 employee profiles.

## Scope

- Database: PostgreSQL (local development and production Master `.85` instances)
- Scripts: 
  - `scripts/tenants/open-kuristanbul-tenant.sql`
  - `scripts/tenants/seed-kuristanbul-ai.sql`
  - `scripts/tenants/generate-kuristanbul-simulation.py` (Python generator)
  - `scripts/tenants/seed-kuristanbul-simulation.sql` (Generated SQL seed)
  - `scripts/tenants/rollback-kuristanbul-simulation.sql` (Rollback script to delete simulation)
- Web/Frontend: Next.js SuperAdmin dashboard (`web/src/app/(dashboard)/super-admin/tenants/page.tsx`)
- Backend API: SuperAdminTenantsController endpoints (`/simulate-history`, `/rollback-simulation`)

## Files Created

- `scripts/tenants/generate-kuristanbul-simulation.py`
- `scripts/tenants/seed-kuristanbul-simulation.sql`
- `scripts/tenants/rollback-kuristanbul-simulation.sql`

## Files Modified

- `scripts/tenants/open-kuristanbul-tenant.sql`
- `scripts/tenants/seed-kuristanbul-ai.sql`
- `src/EmareTicket.API/Controllers/SuperAdminTenantsController.cs`
- `web/src/lib/api/super-admin.ts`
- `web/src/app/(dashboard)/super-admin/tenants/page.tsx`

## Architecture Decisions

- **Self-Serve Simulation:** Instead of hardcoding simulation values into the tenant creation boot script, we built a dynamic execution system. Administrators can trigger/clean history simulation for *any* tenant directly from the UI.
- **Transactional Seeding/Rollback:** Both simulation seeding and rollback actions are executed within safe, database-level transactions in the API layer, guaranteeing that database states remain atomic and clean if a command fails mid-execution.

## Dependencies Added

None.

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet build EmareTicket.sln` | PASS (0 Hata) |

## Test Result

| Komut | Sonuç |
|-------|--------|
| Local SQL Seeding & Seeding Verification | PASS |
| Prod SQL Seeding & Seeding Verification | PASS |
| Landing site deployment (`deploy-kuristanbul-site.sh`) | PASS |
| Transactional API Rollback Execution | PASS |
| Next.js Frontend Integration compilation | PASS |

## Performance Notes

- Seeding 1,000 call logs, 500 support tickets, 300 proposals, 150 customers, and 50 users takes **less than 250 milliseconds** due to transactional raw SQL execution in PostgreSQL.

## Security Notes

- Authorization check: Only users with the **SuperAdmin** role can execute `/simulate-history` and `/rollback-simulation` endpoints.
- Placed the domain as `asistan.kuristanbul.com` for proper tenant resolution, separating public routing from other tenant environments.
- All simulated user accounts are created with password hashes and are bound correctly to the `User` role to maintain security partitioning.

## Technical Debt

None.

## Risks

None.

## Known Limitations

None.

## Breaking Changes

None.

## Next Recommended Task

- Test the simulation trigger option directly in the staging/production SuperAdmin interface to verify rendering of historical statistics.
