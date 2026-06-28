# Task 027 Report - Manual IMAP Sync History Trigger & Date Sync

## Objective
Support triggering a synchronization of past emails for a mail account from a selected start date, and fix database constraint crashes for very long emails.

## Scope
- Add a nullable `ImapSyncStartDate` property to `MailAccount` entity.
- Map the new property in EF Core configuration and generate migration.
- Update `ImapPollerBackgroundService` to use `ImapSyncStartDate` as query start point when `LastImapUid` is 0.
- Truncate `SupportTicket.Description` to 5000 characters in `ImapPollerBackgroundService` to prevent database varchar(5000) constraint crash.
- Create `TriggerMailAccountSyncCommand` MediatR endpoint to reset `LastImapUid` and set `ImapSyncStartDate`.
- Expose `POST /api/v1/mail-accounts/{id}/sync-history` endpoint.

## Files Created
- [TriggerMailAccountSyncCommand.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Features/Mail/MailAccounts/Commands/TriggerMailAccountSync/TriggerMailAccountSyncCommand.cs)
- EF Core Migration files (`*_AddMailAccountSyncStartDate.cs` and Designer.cs)

## Files Modified
- [MailEntities.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Domain/Entities/MailEntities.cs)
- [MailEntityConfigurations.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Persistence/Configurations/MailEntityConfigurations.cs)
- [ImapPollerBackgroundService.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.BackgroundJobs/ImapPollerBackgroundService.cs)
- [MailAccountsController.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.API/Controllers/MailAccountsController.cs)

## Architecture Decisions
- **Background Worker Model:** The API endpoint updates database properties (`LastImapUid = 0` and `ImapSyncStartDate = requestedDate`) and lets the background service process emails. This avoids API request timeout or memory overload, leveraging the existing background poller sequential batch processing (50 emails per run).
- **String Truncation:** Truncated email body to 5000 characters before setting it on `SupportTicket.Description` to guarantee compliance with the database varchar constraint, while saving the full body in `InboundEmails` (using unlimited `text` type).

## Dependencies Added
None.

## Build Result
- Local build succeeded with 0 errors.
- Staging container build succeeded with 0 errors.

## Test Result
- Manual verification: Successfully reset UID and sync-date for a test account. Background poller resolved the tenant ID successfully and started importing 200+ historical emails into the database without any exceptions.

## Performance Notes
- Pre-existing mapping checks prevent duplicate email imports when resetting `LastImapUid`.
- Sequential batching (50 emails per run) protects database connections and memory consumption.

## Security Notes
- Row-level tenant validation prevents non-SuperAdmin users from triggering sync actions on mail accounts belonging to other tenants.

## Technical Debt
- Mail accounts created in early development phase were missing `TenantId`. Fixed existing records manually on the database. Added a task to ensure `AddMailAccountCommand` saves `TenantId` automatically.

## Risks
None.

## Known Limitations
- The first batch only pulls 50 emails, subsequent polls (every 2 minutes) pull the next 50 until completed.

## Breaking Changes
None.

## Next Recommended Task
- Update `AddMailAccountCommandHandler` to automatically set the `TenantId` of the account to `_currentUser.TenantId` during account creation to prevent null tenant IDs for future accounts.
