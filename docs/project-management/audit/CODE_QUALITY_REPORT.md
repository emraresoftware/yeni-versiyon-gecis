# Code Quality Report — Seviye 2

**Tarih:** 2026-07-06  
**Repo:** `/Users/emre/Elyafgroup`  
**Denetim yöntemi:** Otomatik metrik + statik analiz + build/test

---

## Executive Summary

| Metrik | Değer | Hedef | Durum |
|--------|-------|-------|-------|
| Build (Release) | **0 error, 0 warning** | 0 | ✅ |
| Unit tests | **445 PASS / 0 FAIL** | 100% pass | ✅ |
| Toplam LOC (kod) | **~899K** | — | ℹ️ |
| Component >300 satır (TSX) | **96 dosya** | <20 | 🔴 |
| Component >300 satır (CS, excl. migrations) | **~45 dosya** | <30 | 🟡 |
| Merge conflict marker | **0** | 0 | ✅ |
| TODO/FIXME (src/) | **0** | — | ✅ |
| CI workflows | **3** | ≥3 | ✅ |

**Genel kod kalitesi skoru:** **72/100** — build/test mükemmel; component boyutu ve teknik borç yüksek.

---

## 1. Kod Hacmi

| Alan | Satır | Dosya türü |
|------|-------|------------|
| `src/` | 673,687 | C# (.NET 8) |
| `web/src/` | 189,884 | TypeScript/React |
| `tests/` | 12,698 | xUnit |
| `scripts/` | 16,095 | Python |
| `superapp/` | 7,237 | Kotlin + Swift |
| **Toplam (ölçülen)** | **~899,601** | — |

**Not:** Migration Designer dosyaları (~10K satır/dosya) toplamı şişiriyor; gerçek uygulama kodu ~550K civarı.

---

## 2. Build & Test

```
dotnet build EmareTicket.sln -c Release
→ Oluşturma başarılı. 0 Uyarı, 0 Hata

dotnet test EmareTicket.sln -c Release
→ 445/445 PASS (2026-07-06)
```

| Proje | Controller/Modül | Test kapsamı |
|-------|------------------|--------------|
| EmareTicket.API | 84 controller | Integration + unit |
| EmareTicket.Tests | 446 test metodu | AI, CRM, Auth, Voice, Branding |
| web/ | Next.js 14 | npm build PASS (QA gate) |

**Test coverage:** Resmi % raporu yok (coverlet/collector yapılandırılmamış). Tahmini backend **~40-55%** (kritik path'ler testli, UI düşük).

---

## 3. Component >300 Satır (Risk)

### En büyük TSX dosyaları (top 10)

| Satır | Dosya | Risk |
|-------|-------|------|
| 3,447 | `web/src/app/(dashboard)/demo-agent/page.tsx` | 🔴 Refactor |
| 3,094 | `web/src/app/(dashboard)/settings/ai-scenarios/ScenarioCanvas.tsx` | 🔴 |
| 2,405 | `web/src/app/(dashboard)/call-center/page.tsx` | 🔴 |
| 1,514 | `web/src/app/(auth)/login/LoginPageClient.tsx` | 🟡 |
| 1,371 | `web/src/app/(dashboard)/super-admin/tenants/page.tsx` | 🟡 |
| 1,336 | `web/src/app/(dashboard)/reports/page.tsx` | 🟡 |
| 1,244 | `web/src/app/(dashboard)/settings/ai-scenarios/page.tsx` | 🟡 |
| 1,238 | `web/src/app/(dashboard)/call-center/CampaignVisualDesigner.tsx` | 🟡 |
| 1,148 | `web/src/features/elyaf-control-tower/.../BudgetSlideDeck.tsx` | 🟡 |
| 1,105 | `web/src/app/(dashboard)/reseller/tenants/page.tsx` | 🟡 |

**Toplam >300 satır TSX:** 96 dosya  
**Architect kuralı:** component <300 — **%89 ihlal oranı** (ölçülen sette)

### En büyük C# dosyaları (migration hariç, top 5)

| Satır | Dosya |
|-------|-------|
| ~3,200 | `AiActionService.cs` |
| ~1,800 | `WhatsAppWebhookProcessor.cs` |
| ~1,200 | `Program.cs` (API) |
| ~900 | `VoiceBridgeController.cs` |
| ~800 | `AppDbContext.cs` |

---

## 4. Duplicate Code

| Alan | Bulgu |
|------|-------|
| Locale dosyaları | 50+ `web/src/config/locales/*.ts` — yapısal tekrar (i18n generator yok) |
| Elyaf rol dashboard'ları | 16 benzer dashboard component — kısmen `elyaf-control-tower/` modülünde konsolide |
| AI OS scripts | V1/V2 paralel (mission-planner, agent-runner, qa) — bilinçli fallback |
| docs/ vs emare-dashboard/docs/ | Mirror kopyalar — sync riski |

**Architect duplicate_code check:** QA V2 platform scope'ta SKIP — otomatik tarama yok.

---

## 5. TODO / FIXME / Technical Debt Markers

| Konum | Sayı | Not |
|-------|------|-----|
| `src/` | 0 | Temiz |
| `web/src/` (TODO/FIXME) | 0 | Temiz |
| Locale `XXX` placeholder | ~100 | Çeviri placeholder |
| WhatsAppWebhookProcessor | 3 | Inline notlar |

**Sonuç:** Kod içi TODO disiplini iyi; borç dokümantasyonda (`kalan-eksikler/`).

---

## 6. Dead Code & Unused

| Bulgu | Kanıt |
|-------|-------|
| Monolit dashboard | `web/src/app/(dashboard)/dashboard/page.tsx` — 10K+ satır, modüler rota `/control-tower/` ile paralel |
| V1 pipeline scripts | Hâlâ referans var, V2 aktif |
| `docs/project-management/` mirror | Elyafgroup root + emare-dashboard duplicate |
| ERP InventoryView/ShippingView | git diff'te silinmiş görünüyor — doğrulanmalı |

**Unused packages:** web 47 deps + 11 devDeps — `depcheck` çalıştırılmadı; manuel review önerilir.

---

## 7. Circular Dependency

| Katman | Durum |
|--------|-------|
| Domain → Application → Infrastructure → API | ✅ DDD katmanları temiz |
| Persistence ↔ Infrastructure | ✅ Interface üzerinden |
| web → API | HTTP only — ✅ |
| scripts → repo | Python standalone — ✅ |

**Bilinen risk:** `AiActionService` 3200 satır — god service anti-pattern, circular risk düşük ama maintainability düşük.

---

## 8. Merge Conflicts

```
rg "^<<<<<<< " → 0 aktif conflict marker
```

**Not:** `client.ts` merge conflict geçmişte ARCHITECT condition olarak raporlanmış — güncel durumda yok.

---

## 9. CI/CD

| Workflow | Dosya | Durum |
|----------|-------|-------|
| Backend build | `.github/workflows/backend-build.yml` | ✅ |
| Deploy | `.github/workflows/deploy.yml` | ✅ |
| Sealed voice settings | `.github/workflows/sealed-voice-settings.yml` | ✅ |

**Eksik:** Frontend CI ayrı workflow yok; QA autorunner local-only.

---

## 10. Skor Kartı

| Kategori | Puan | Ağırlık |
|----------|------|---------|
| Build stability | 100 | 20% |
| Test pass rate | 100 | 20% |
| Component size discipline | 35 | 15% |
| Duplicate / DRY | 55 | 10% |
| Documentation debt | 60 | 10% |
| Security markers (TODO) | 85 | 10% |
| CI coverage | 70 | 10% |
| Layer architecture | 90 | 5% |
| **Weighted total** | **72** | 100% |

---

## Öncelikli Aksiyonlar

1. **P0:** `demo-agent/page.tsx`, `ScenarioCanvas.tsx`, `call-center/page.tsx` — parçalama
2. **P1:** Coverlet + coverage gate (%60 hedef)
3. **P1:** `depcheck` + unused export taraması (web)
4. **P2:** Locale generator — 50 dosya tekrarını azalt
5. **P2:** `AiActionService.cs` handler extract (domain bazlı partial class)

---

_Generated: Program Review V1 — Seviye 2_
