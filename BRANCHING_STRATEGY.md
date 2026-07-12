# 🌿 Git Branching Strategy

**Title:** Git Branching Strategy
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-07-12
**Dependencies:** README.md, AGENTS.md
**Related Documents:** DEPLOYMENT_ARCHITECTURE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-07-12 | Agent 0 (Antigravity) | İlk sürüm — branch modeli, sunucu eşlemesi ve merge kuralları. |

---

## Branch Modeli

Proje **Modified Git Flow** stratejisi kullanır. İki ana branch ve opsiyonel feature branch'ler vardır:

```text
main ──────────────────────────────────────────► (kararlı / production)
  │
  └── gece-otonom ─────────────────────────────► (geliştirme / staging)
        │
        ├── feature/xxx  (opsiyonel kısa ömürlü)
        └── fix/xxx      (opsiyonel kısa ömürlü)
```

---

## Branch Tanımları

### `main` — Kararlı (Stable Production)
- **Amaç:** Production-ready, kararlı sürüm.
- **Sunucu:** `31.169.72.84` (Stable Test), `185.189.54.107` (Master Production)
- **Merge Kaynağı:** Yalnızca `gece-otonom` → `main` merge ile (no-ff).
- **Kural:** Doğrudan commit **yasaktır**. Her merge, staging'de test edildikten sonra yapılır.
- **Domain:** `test.emarecloud.tr`, `test.asistan.emarecloud.tr`

### `gece-otonom` — Geliştirme (Development / Staging)
- **Amaç:** AI ajanlarının gece boyunca otonom çalıştığı aktif geliştirme branch'i.
- **Sunucu:** `31.169.72.85` (Staging Orchestrator), `31.169.72.82` (Standby)
- **İsim Kökeni:** "Gece Otonom" = Gece saatlerinde AI ajanları otonom olarak görev alıp kod üretir, test eder ve commit'ler.
- **Kural:** Feature merge ve doğrudan commit kabul eder.

### `feature/*` ve `fix/*` — Kısa Ömürlü Branch'ler (Opsiyonel)
- **Amaç:** Büyük özellikler veya karmaşık bug fix'ler için izolasyon.
- **Ömür:** Mümkün olan en kısa sürede `gece-otonom`'a merge edilip silinir.
- **Kural:** Merge öncesi build ve test kontrolü gerekir.

---

## Sunucu ↔ Branch Eşlemesi

| Sunucu | IP | Branch | Rol |
|---|---|---|---|
| Master Production | `185.189.54.107` | `main` | Canlı müşteri trafiği |
| Stable Test | `31.169.72.84` | `main` | QA ve kabul testleri |
| Staging Orchestrator | `31.169.72.85` | `gece-otonom` | Geliştirme ve ajan testleri |
| Standby | `31.169.72.82` | `gece-otonom` | Yedek (uykudayken güncellenir) |

---

## Merge ve Deployment Akışı

### Geliştirme Süreci
```bash
# 1. Geliştirme branch'inde çalış
git checkout gece-otonom
# ... kod yaz, test et ...
git add . && git commit -m "feat: açıklama"
git push emaredestek gece-otonom

# 2. Staging'e deploy et
ssh ticket@31.169.72.85 "/home/ticket/sync_deploy.sh 31.169.72.85 gece-otonom"
```

### Kararlı Sürüm Yayınlama
```bash
# 1. gece-otonom → main merge
git checkout main
git merge gece-otonom --no-ff -m "merge: release açıklama"
git push emaredestek main
git checkout gece-otonom

# 2. Stable Test sunucusuna deploy et
ssh ticket@31.169.72.85 "/home/ticket/sync_deploy.sh 31.169.72.84 main"

# 3. Testler başarılı → Master Production'a deploy et
ssh ticket@31.169.72.85 "/home/ticket/sync_deploy.sh 185.189.54.107 main"
```

---

## Commit Mesajı Standartları (Conventional Commits)

```text
<tip>(<kapsam>): <açıklama>

Tipler:
  feat     — Yeni özellik
  fix      — Bug düzeltmesi
  refactor — Davranış değiştirmeyen kod düzenlemesi
  docs     — Belge değişikliği
  test     — Test ekleme/güncelleme
  chore    — Build, CI, bağımlılık güncellemesi
  perf     — Performans iyileştirmesi
  style    — Formatlama (boşluk, noktalı virgül vb.)

Örnekler:
  feat(crm): müşteri segmentasyon filtresi eklendi
  fix(telephony): Asterisk trunk yeniden kayıt hatası düzeltildi
  docs(readme): dual repository disclaimer eklendi
```

---

## Koruma Kuralları

| Kural | `main` | `gece-otonom` |
|---|---|---|
| Doğrudan push | ❌ Yasak | ✅ İzinli |
| Merge kaynağı | Yalnızca `gece-otonom` | Feature branch veya doğrudan |
| Force push | ❌ Yasak | ❌ Yasak |
| Build kontrolü (gelecek) | ✅ Zorunlu | ⚠️ Önerilir |
| Test kontrolü (gelecek) | ✅ Zorunlu | ⚠️ Önerilir |

---

## Temel İlkeler

1. **`main` her zaman deploy edilebilir durumda olmalıdır.**
2. **`gece-otonom` kırılabilir**, ama mümkün olan en kısa sürede düzeltilmelidir.
3. **Feature branch'ler kısa ömürlü olmalıdır** — günler değil, saatler.
4. **Sırlar (secret) hiçbir branch'te commit edilmez** — `.env`, API key, connection string vb.
5. **Her merge sonrası staging'de doğrulama yapılır** — build + smoke test.
