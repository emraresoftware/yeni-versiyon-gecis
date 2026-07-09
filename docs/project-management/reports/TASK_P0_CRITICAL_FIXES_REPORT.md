# Task P0_CRITICAL_FIXES Report

## Objective

Resolve critical P0 errors listed in `Emare-Keşif.docx` including file upload authentication redirects, sales lead postgres kind exceptions, automatic product SKU generation, and invoice layout theme alignments.

## Scope

- **API Modules:** `FilesController`, `SalesLeadsController`, `ProductsController`.
- **Frontend Pages/Components:** `FileUploadDialog`, `customers/[id]/page.tsx`, `files/page.tsx`, `products/page.tsx`, `invoices/page.tsx`, `invoices/[id]/page.tsx`, `invoices/settings/page.tsx`.
- **API Client / State Hooks:** `client.ts`, `files.ts`, `customers.ts`, `use-files.ts`, `use-tasks.ts`, `use-customers.ts`.

## Files Created

None.

## Files Modified

- `src/EmareTicket.API/Controllers/ProductsController.cs`
- `src/EmareTicket.API/Controllers/SalesLeadsController.cs`
- `web/src/app/(dashboard)/customers/[id]/page.tsx`
- `web/src/app/(dashboard)/files/page.tsx`
- `web/src/app/(dashboard)/invoices/[id]/page.tsx`
- `web/src/app/(dashboard)/invoices/page.tsx`
- `web/src/app/(dashboard)/invoices/settings/page.tsx`
- `web/src/app/(dashboard)/products/page.tsx`
- `web/src/components/files/FileUploadDialog.tsx`
- `web/src/hooks/use-customers.ts`
- `web/src/hooks/use-files.ts`
- `web/src/hooks/use-tasks.ts`
- `web/src/lib/api/client.ts`
- `web/src/lib/api/customers.ts`
- `web/src/lib/api/files.ts`
- `web/src/lib/api/index.ts`

## Architecture Decisions

None.

## Dependencies Added

None.

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet build EmareTicket.sln` | PASS |
| `dotnet build Emare.sln` | PASS |
| `npm run build` | PASS |

## Test Result

| Komut | Sonuç |
|-------|--------|
| `dotnet test EmareTicket.sln` | PASS — 681/681 geçti |
| `dotnet test Emare.sln` | PASS — 52/52 geçti |

## Performance Notes

None.

## Security Notes

- Secured file upload routes and download streams by routing raw custom fetch implementations to the centralized `apiClient.postForm` and `apiClient.getBlob`. This ensures that httpOnly cookie/JWT token validation and refreshing are handled automatically and securely.
- Prevented potential data injection on SKU codes by validating and generating unique values under tenant-isolated checks.

## Technical Debt

None.

## Risks

None.

## Known Limitations

None.

## Breaking Changes

None.

## Next Recommended Task

Review and update project-scoped documentation on client-api request patterns to prevent raw `fetch()` overrides.
