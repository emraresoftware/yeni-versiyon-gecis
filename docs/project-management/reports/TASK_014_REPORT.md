# Task 014 Report

PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

## Objective
The objective of Task 014 is to build the Clean Architecture Application layer (CQRS Commands, Queries, Handlers, DTOs, Validators, and integration tests) for the CRM Core Module of the platform.

## Scope
* **DTOs:** Create all CRM record DTOs and entity extension mapper methods in `DTOs/Crm/CrmDtos.cs`.
* **Commands & Handlers:** Implement CQRS Commands (Create, Update, Delete, Change Stage, Add Child Item, Send, Approve) and their MediatR Handlers.
* **Queries & Handlers:** Implement CQRS Queries (GetById, List) and their specifications, along with the CRM Dashboard Summary metrics query.
* **Validators:** Add FluentValidation validators for all CQRS commands enforcing validation business logic (NPS, Health, Risk ranges, UTC Date kind checks, positive numbers).
* **Integration Tests:** Implement real SQLite in-memory integration tests verifying all CQRS commands, validators, and queries.

## Files Created
* [CrmDtos.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/DTOs/Crm/CrmDtos.cs)
* [CrmAccountCommands.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/Commands/Crm/CrmAccountCommands.cs)
* [CrmContactCommands.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/Commands/Crm/CrmContactCommands.cs)
* [CrmOpportunityCommands.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/Commands/Crm/CrmOpportunityCommands.cs)
* [CrmProposalCommands.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/Commands/Crm/CrmProposalCommands.cs)
* [CrmActivityCommands.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/Commands/Crm/CrmActivityCommands.cs)
* [CrmQueries.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/Queries/Crm/CrmQueries.cs)
* [CrmValidators.cs](file:///Users/emre/Elyafgroup/src/Platform/Application/Validators/Crm/CrmValidators.cs)
* [CrmApplicationTests.cs](file:///Users/emre/Elyafgroup/tests/Emare.Platform.Persistence.Tests/Crm/CrmApplicationTests.cs)

## Files Modified
* [CrmProposalItem.cs](file:///Users/emre/Elyafgroup/src/Platform/Domain/Entities/Crm/CrmProposalItem.cs): Updated Id assignment in `Create` method to `Guid.Empty` to allow EF Core's change tracker to mark it as `Added` (inserted) instead of `Modified` (updated).
* [AuditableEntitySaveChangesInterceptor.cs](file:///Users/emre/Elyafgroup/src/Platform/Persistence/Interceptors/AuditableEntitySaveChangesInterceptor.cs): Modified `UpdateAuditProperties` to manually generate and rotate GUID byte arrays for `IConcurrencyTracked` entities under SQLite.

## Architecture Decisions
* **Child Entity Modeling:** `CrmProposalItem` is correctly treated as a child entity under the `CrmProposal` aggregate root. It has no independent repository, and operations are managed through `CrmProposal`.
* **Clean Change Tracking:** By initializing `Id` of `CrmProposalItem` to `Guid.Empty` inside the domain factory method, we leverage EF Core's built-in key generation. This enables the change tracker to correctly mark it as `Added` (triggering an `INSERT` statement) when added to the parent collection, avoiding the concurrency exception caused by pre-populating non-empty Guid keys.
* **SQLite Concurrency Simulation:** Implemented Guid byte array rotation for `IConcurrencyTracked` entities in the SQLite `SaveChangesInterceptor` to mimic SQL Server/Postgres rowversion behavior in test environments.

## Dependencies Added
* None.

## Build Result
* **Status:** Success. Compiled with 0 errors and 1 warning (unrelated async warning in `CrmPersistenceTests`).

## Test Result
* **Status:** Success. All **117** unit and integration tests across the solution passed successfully.

## Performance Notes
* Used EF Core `Specification` pattern with `.AsNoTracking()` implicitly on queries via `ListAsync` and `FirstOrDefaultAsync` where updates are not performed, optimizing read performance.
* Replaced redundant `.Update()` calls on repository updates to avoid unnecessary graph traversals.

## Security Notes
* Applied global query filters for multi-tenancy (`TenantId`) and soft delete (`IsDeleted`) to isolate tenant data.
* Handlers retrieve `TenantId` securely from `ITenantProvider` instead of client requests.

## Technical Debt
* SQLite `RowVersion` rotation is simulated via interceptor. This works perfectly for in-memory testing but depends on the DbContext interceptor. It does not affect production environments since Postgres uses native column tracking.

## Risks
* None identified.

## Known Limitations
* Database-generated default constraints on SQLite rowversions are not native, which is why they are handled via the interceptor.

## Breaking Changes
* None.

## Next Recommended Task
* Implement the Controller/API layer endpoints for CRM operations, exposing the CQRS commands and queries.
