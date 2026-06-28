# Task 018 Report — Proposal Module (Acar Telekom Pilot, Phase 0)

## Objective

Acar Telekom / Acarcell tenant'ında mevcut EmareTicket **Proposal** modülünü pilot olarak açmak: `proposals` feature flag, tenant branding, demo teklif + kalemler ve public link (`/p/{id}`) için regression test kapsamı.

## Scope

- Phase 0 only (plan: `TASK_018_PROPOSAL_ACAR_PILOT_PLAN.md`)
- Pilot tenant: `95f4fbc7-db68-4063-9be7-c0a8ce93afb9`
- Platform `CrmProposal` (Task 013/015) kapsam dışı

## Files Created

| Dosya | Açıklama |
|-------|----------|
| `scripts/tenants/seed-acar-telekom-proposals.sql` | TenantFeatures, branding, demo müşteri/teklif/kalemler |

## Files Modified

| Dosya | Değişiklik |
|-------|-----------|
| `tests/EmareTicket.Tests/Application/ProposalTrackingTests.cs` | Acarcell branding assertion testi eklendi |

## Architecture Decisions

1. **Mevcut modül genişletme:** Yeni Platform CRM teklif entity'si yerine `Proposals` / `PublicProposalsController` kullanıldı.
2. **Multi-tenant:** Seed script yalnızca Acar UUID'sine yazar; kod değişikliği tüm tenant'lara geçerli.
3. **Demo veri sabit UUID:** Smoke test ve dokümantasyon için deterministik proposal ID (`95f4fbc7-c0a0-5000-8000-000000000010`).

## Dependencies Added

Yok.

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet build` (EmareTicket.Tests transitif) | PASS |

## Test Result

| Komut | Sonuç |
|-------|--------|
| `dotnet test tests/EmareTicket.Tests --filter FullyQualifiedName~ProposalTrackingTests` | PASS — **10/10** |

Yeni test: `GetPublicProposal_ShouldReturnAcarcellBranding_WhenTenantBranded`

## Performance Notes

Yok.

## Security Notes

- Seed script production DB'ye manuel `psql` ile uygulanır; repoda secret yok.
- Public endpoint tenant izolasyonu mevcut controller mantığı ile korunur.

## Technical Debt

- Phase 1–2 (PDF/e-posta/WhatsApp link paylaşımı, ürün şablonları) planlandı, henüz uygulanmadı.
- `LogoUrl` = `/branding/acarcell-logo.svg` — static asset henüz `web/public` altında yok; logo yüklenince güncellenmeli.
- `docs/project-management/reports/TASK_018_REPORT.md` Voice Bridge raporunu içeriyor; numara çakışması — Voice Bridge raporu `TASK_016` olarak yeniden adlandırılmalı.

## Breaking Changes

Yok.

## Deployment / Ops

Production/staging'de seed uygulama (önce `seed-acar-telekom-ai.sql`):

```bash
psql -U emareticket -d EmareTicketProd -f scripts/tenants/seed-acar-telekom-proposals.sql
```

Smoke test:

1. Acar tenant admin → `/deals` menüsü görünür.
2. Demo teklif: `ACR-2026-0001` — public link `/p/95f4fbc7-c0a0-5000-8000-000000000010`.
3. Link açılışı → `ProposalView` + `CustomerActivity` kaydı.
4. Analytics panelinde görüntülenme.

## Phase 0 Checklist

| Kriter | Durum |
|--------|--------|
| `TenantFeatures.proposals` (+ satış modülleri) | ✅ Seed |
| Acarcell branding (BrandName, renkler) | ✅ Seed + test |
| Demo teklif + kalemler | ✅ Seed |
| Tracking regression test | ✅ 10/10 |
| Canlı DB seed uygulaması | ⏳ Ops (manuel) |

## Next Recommended Task

- **Phase 1:** Analytics/PDF/e-posta regression + edge case'ler
- **Phase 2:** WhatsApp teklif linki + Acar ürün şablonları
- Ops: Production'da seed script çalıştır + smoke test
