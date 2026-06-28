# TASK 018 — Proposal Module Expansion (Acar Telekom Pilot)

**Title:** Teklif modülü genişletme — Acar Telekom pilot, tüm tenant’lar için multi-tenant  
**Version:** 1.0.0  
**Status:** Approved (planning)  
**Owner:** Product / Agent 1  
**Last Updated:** 2026-06-28  
**Pilot Tenant:** Acar Telekom / Acarcell — `95f4fbc7-db68-4063-9be7-c0a8ce93afb9`  
**Related:** `LEGACY_BUSINESS_RULES.md`, `FEATURE_TRACEABILITY_MATRIX.md`, Platform `CrmProposal` (Task 013/015 — ayrı hat)

---

## 1. Karar özeti

| Soru | Karar |
|------|--------|
| Yeni Platform CRM mi? | **Hayır** (kısa vade) |
| Mevcut EmareTicket Proposal modülü mü? | **Evet** — genişlet |
| Sadece Acar mı? | **Hayır** — kod tüm tenant’lara geçer; Acar **pilot** |
| Public link + tracking? | Mevcut `ProposalView` + `/p/{id}` korunur ve güçlendirilir |

---

## 2. Mevcut modül envanteri (Elyafgroup / EmareTicket)

| Bileşen | Konum |
|---------|--------|
| CRM teklif API | `src/EmareTicket.API/Controllers/ProposalsController.cs` |
| Public teklif + tracking | `src/EmareTicket.API/Controllers/PublicProposalsController.cs` |
| Tracking entity | `src/EmareTicket.Domain/Entities/ProposalView.cs` |
| Geo / cihaz helper | `src/EmareTicket.API/Services/VisitorTrackingHelper.cs` |
| Dashboard UI | `web/src/app/(dashboard)/deals/` |
| Public sayfa | `web/src/app/p/[id]/page.tsx` |
| Analytics UI | `web/src/components/proposals/ProposalAnalytics.tsx` |
| Workspace | `proposals` — `emare-dashboard/docs/workspaces/modules.json` |

### Tracking özellikleri (zaten var)

- Sayfa açılışı, bölüm süresi (`SectionName`, `DurationSeconds`)
- Konum: `Country`, `City`, `Region`, `Latitude`, `Longitude`
- Cihaz: `DeviceType`, `Browser`, `Os`
- Paylaşım: `IsForwarded`, `ReferrerUrl`, UTM
- CRM aktivite: `CustomerActivity` — “Teklif görüntülendi… Konum: …”
- Durum: Sent → Görüşülüyor (3) otomatik

---

## 3. Tenant matrisi

### Feature key

`FeatureKeys.Proposals` = `"proposals"` — tenant ve kullanıcı seviyesinde açılır/kapanır.

### Sektör varsayılanları (`sector-features.yaml`)

| Sektör | `proposals` varsayılan |
|--------|-------------------------|
| retail | ✅ |
| manufacturing | ❌ |
| services | ❌ |
| logistics | ❌ |
| saas | ❌ |
| other | ❌ |

### Bilinen tenant seed’leri (`proposals` açık)

| Tenant | Script |
|--------|--------|
| Elyaf Group | `scripts/tenants/open-elyaf-group-tenant.sql` |
| Emare Asistan | `scripts/tenants/open-emare-asistan-tenant.sql` |
| Corvis | `scripts/tenants/open-corvis-customer.sql` |

### Acar Telekom — **GAP**

| Alan | Durum |
|------|--------|
| Tenant UUID | `95f4fbc7-db68-4063-9be7-c0a8ce93afb9` |
| AI / ses seed | ✅ `scripts/tenants/seed-acar-telekom-ai.sql` |
| `TenantFeatures.proposals` | ❌ **Seed’de yok** — Phase 0’da eklenmeli |
| Tenant branding (logo, renk) | ⚠️ Doğrulanmalı (`Tenants.BrandName`, `LogoUrl`, `PrimaryColor`) |

---

## 4. Faz planı

### Phase 0 — Acar pilot hazırlık (1–2 gün)

- [ ] `TenantFeatures` → `proposals`, `whatsapp`, `email`, `reports` (satış akışı için)
- [ ] Acarcell branding: logo, `#` renkler, public `/p/{id}` önizleme
- [ ] Demo teklif + public link smoke test
- [ ] Script: `scripts/tenants/seed-acar-telekom-proposals.sql` (yeni)

### Phase 1 — Modül sağlamlaştırma (tüm tenant’lar)

- [ ] `ProposalView` + analytics endpoint regression test
- [ ] Public page section tracking (`trackPublicProposal`) doğrulama
- [ ] PDF + e-posta gönderim (`SendEmailDialog`) + link kopyala akışı
- [ ] NotFound / iptal teklif edge case’leri
- [ ] `DateTime.UtcNow` audit (ANAYASA)

### Phase 2 — Acar satış entegrasyonu

- [ ] WhatsApp: teklif linki paylaşımı (`/p/{id}`) — AI “teklif oluşturdum” guard’ları ile uyum
- [ ] Sesli/outbound: keşif sonrası teklif oluşturma → link SMS/WhatsApp (opsiyonel)
- [ ] Acar ürün kataloğu → `ProposalItem` şablonları (santral, fiber, kamera paketleri)
- [ ] CRM aktivite timeline’da proposal view görünürlüğü

### Phase 3 — Diğer tenant rollout

- [ ] Paket matrisi: hangi tenant’ta `proposals` açılacak
- [ ] Onboarding: `retail` sektörüne otomatik `proposals` (mevcut yaml)
- [ ] Dokümantasyon: tenant admin “Teklif paylaşım linki” rehberi

### Out of scope (ayrı task)

- Platform `CrmProposal` + `ProposalView` port (Task 019+)
- Control Tower Sales widget’larının EmareTicket Proposal’a bağlanması

---

## 5. Kabul kriterleri (Acar pilot)

1. Acar tenant’ta `/deals` menüsü görünür (`proposals` feature açık).
2. Teklif oluştur → public link `/p/{id}` → Acarcell branding.
3. Link açılınca `ProposalView` + `CustomerActivity` konum/cihaz ile kayıt.
4. Dashboard analytics: görüntülenme, lokasyon, forward tespiti.
5. E-posta veya WhatsApp ile link paylaşımı (en az biri).
6. Multi-tenant: başka tenant verisi Acar panelinde görünmez.

---

## 6. Dosya hedefleri (Agent 1)

| Aksiyon | Dosya |
|---------|--------|
| Yeni seed | `scripts/tenants/seed-acar-telekom-proposals.sql` |
| Opsiyonel | `PublicProposalsController.cs` — Acar şablon alanları |
| Opsiyonel | `web/src/app/p/[id]/page.tsx` — branding iyileştirme |
| Test | `tests/EmareTicket.Tests/Proposals/` veya API integration |
| Rapor | `docs/project-management/reports/TASK_018_REPORT.md` |

---

## 7. Agent ataması

| Rol | Görev |
|-----|--------|
| **Agent 1** | Phase 0–2 implementasyon |
| **Agent 2** | QA — build/test, tenant isolation, tracking doğrulama |
| **Agent 3** | Mimari — Platform port roadmap (opsiyonel ADR) |
| **Kullanıcı** | Task 016 Voice Bridge refactor kararı |

---

## 8. Sonraki adım

**Agent 1:** Phase 0 — `seed-acar-telekom-proposals.sql` + Acar branding doğrulama + smoke test.
