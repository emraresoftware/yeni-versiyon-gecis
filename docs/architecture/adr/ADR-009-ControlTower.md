# ADR-009 — Control Tower Product Architecture

**Date:** 2026-06-27  
**Decision Makers:** Product Board / Architecture Board

---

## Status

**Accepted**

---

## Context

Elyaf Group 2.0 platformu 16 departman/modül için yönetici dashboard'ları (Control Tower) sunar. Her kule farklı KPI ve iş süreçlerine sahip olsa da görsel ve fonksiyonel tutarlılık müşteri kabul kriteridir. Dağınık dashboard implementasyonu eğitim maliyeti, UX tutarsızlığı ve backend API tekrarı üretir. `CONTROL_TOWER_FINAL_SCOPE.md` v1.1.0 final kapsamı kilitler.

---

## Decision

**16 Control Tower** standart **15 UI bloğu** ile implemente edilir:

1. Executive Snapshot  
2. KPI Kartları (≥4, trend + periyot karşılaştırması)  
3. Today's Priorities  
4. Critical Alerts  
5. Notifications  
6. Risk / Health Score  
7. Customer / Supplier / Department Panel  
8. Message Drafts  
9. Calendar & Key Events  
10. Next 7 Days Focus  
11. Reports & Analytics  
12. Sol dikey menü (modül alt menüleri)  
13. Rol bazlı profil alanı  
14. Export / Filter / Date controls  
15. Legend / status açıklamaları  

**MVP öncelik matrisi:**

| Öncelik | Control Tower'lar |
|---|---|
| 🔴 Kritik | CEO, Sales, Finance, HR, Production |
| 🟠 Yüksek | QC, Logistics, Fabric Procurement, Accessories Procurement |
| 🟡 Orta | Merchandising, Design, Sample, Licensing, Compliance, IT & AI, Performance Intelligence |

**Backend sözleşmesi:**

- API prefix: `/api/control-tower/{module}/...`
- Permission: `{Module}.ControlTower.View` (ör. `CEO.ControlTower.View`)
- Event/Entity isimlendirme: `CONTROL_TOWER_FINAL_SCOPE.md` § Standardization Notes
- Traceability: `FEATURE_TRACEABILITY_MATRIX.md` — widget → API → handler → entity → permission → test

**UX standartları:** `UX_REVIEW.md` — grid layout, KPI card, widget kabuğu, responsive, WCAG 2.2 AA.

**Sprint gate:** Scope dokümanı onaylanmadan CRM/Sales sprint başlatılmaz.

---

## Consequences

**Pozitif:**

- Müşteri screenshot'ları ile görsel kabul testi mümkün.
- 92+ widget traceability ile denetlenebilir geliştirme.
- Modüller arası tutarlı yönetici deneyimi.

**Negatif:**

- 16 kule × 15 blok = yüksek implementasyon hacmi.
- Backend aggregation servisleri KPI başına ayrı endpoint gerektirir.
- Scope değişikliği Architecture Board onayı gerektirir.

---

## Alternatives Considered

| Alternatif | Neden reddedildi |
|---|---|
| **Modül başına özel dashboard layout** | UX tutarsızlığı; eğitim maliyeti. |
| **Tek unified dashboard (filtre ile modül)** | Departman persona ihtiyaçları karşılanmaz. |
| **BI tool embed (Power BI only)** | İşlem/onay akışları ve AI entegrasyonu zayıf. |
| **Metadata-driven dashboard (MVP)** | Uzun vadede hedef; MVP'de scope-locked widget seti tercih edildi. |

---

## References

- [CONTROL_TOWER_FINAL_SCOPE.md](../../product/CONTROL_TOWER_FINAL_SCOPE.md)
- [FEATURE_TRACEABILITY_MATRIX.md](../../product/FEATURE_TRACEABILITY_MATRIX.md)
- [UX_REVIEW.md](../../product/UX_REVIEW.md)
- [LOCALIZATION_I18N_STANDARDS.md](../../product/LOCALIZATION_I18N_STANDARDS.md)
- [SECURITY_AUTHORIZATION.md](../../../SECURITY_AUTHORIZATION.md)
