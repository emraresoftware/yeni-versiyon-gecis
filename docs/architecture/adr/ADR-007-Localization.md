# ADR-007 — Localization (i18n)

**Date:** 2026-06-27  
**Decision Makers:** Architecture Board

---

## Status

**Accepted**

---

## Context

Emare BOS küresel ölçeklenebilirlik hedefler; Control Tower ekranları, backend hata mesajları, bildirimler ve AI Copilot yanıtları çoklu dil desteği gerektirir. Hardcoded arayüz metinleri i18n borcu, RTL layout kırıkları ve AI dil tutarsızlığı üretir. `LOCALIZATION_I18N_STANDARDS.md` ve `CONTROL_TOWER_FINAL_SCOPE.md` § Multi-language bu gereksinimi kilitler.

---

## Decision

Platform **dört kilitli dil** ile tam i18n desteği sağlar:

| Locale | Dil | Not |
|---|---|---|
| `tr-TR` | Türkçe | **defaultLocale** — kanonik şema |
| `en-US` | İngilizce | |
| `de-DE` | Almanca | |
| `ar-SA` | Arapça | **RTL** layout desteği |

**Frontend:**

- Tip güvenli `emare-i18n` paketi; derleme zamanı anahtar doğrulaması.
- Dil dosyaları: `src/config/locales/{tr,en,de,ar}.ts`; kanonik şema `tr.ts`.
- Kategori ayrımı: `common`, `navigation`, `validation`, `pages`.
- Pluralization: `_zero`, `_one`, `_other` sonek standardı.
- SSR hydration: `deferClientDetection` + `applyClientLocale()` ile mismatch önleme.
- **Control Tower:** Hiçbir etiket, KPI, alert, tablo kolonu hardcoded olamaz.
- **RTL:** `dir="rtl"` dinamik; mantıksal CSS (`margin-inline-start` vb.) zorunlu.

**Backend:**

- `Accept-Language` header → `RequestLocalizationMiddleware` → `CultureInfo.CurrentUICulture`.
- Dinamik içerik: PostgreSQL `jsonb` translation kolonları (`NameTranslations`).

**AI Copilot dil hiyerarşisi:**

1. Aktif kullanıcı dili (UI/profil)
2. Tenant varsayılan dili
3. `Accept-Language` HTTP header

---

## Consequences

**Pozitif:**

- Tek codebase ile 4 pazar; RTL dahil.
- Compile-time i18n hataları erken yakalanır.
- Backend/AI/UI dil tutarlılığı tanımlı hiyerarşi ile sağlanır.

**Negatif:**

- Her yeni UI metni 4 dil dosyasına eklenmeli (veya fallback chain).
- RTL test matrisi QA yükünü artırır.
- JSONB translation kolonları sorgu karmaşıklığı getirir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **TR-only MVP** | Scope dokümanı i18n'i zorunlu kılar; geri dönüş maliyeti yüksek. |
| **Runtime-only i18n (no type safety)** | Yanlış anahtarlar production'a sızar. |
| **Separate locale builds** | Deploy çoğaltma; bakım maliyeti. |
| **Third-party i18n (i18next) only** | `emare-i18n` zero-dependency ve type-safe hedefi için özel paket seçildi. |

---

## References

- [LOCALIZATION_I18N_STANDARDS.md](../../product/LOCALIZATION_I18N_STANDARDS.md)
- [CONTROL_TOWER_FINAL_SCOPE.md](../../product/CONTROL_TOWER_FINAL_SCOPE.md)
- [FRONTEND_STANDARDLARI.md](../../../FRONTEND_STANDARDLARI.md)
- [AI_ENGINE.md](../../../AI_ENGINE.md)
- [FULL_REPO_REVIEW_CHECKLIST.md](../../project-management/reviews/FULL_REPO_REVIEW_CHECKLIST.md)
