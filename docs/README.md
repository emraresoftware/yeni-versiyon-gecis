# yeni-versiyon-gecis/docs — Arşiv / Mirror

**Durum:** STALE — kanonik kaynak değil  
**Tarih:** 2026-07-06

---

## Tek kanonik kaynak

Tüm güncel proje dokümantasyonu:

```text
/Users/emre/Elyafgroup/emare-dashboard/docs/
```

Repo kökünden erişim:

```text
Elyafgroup/docs/   (symlink → emare-dashboard/docs)
```

Harita: [`emare-dashboard/docs/DOCS_INDEX.md`](../emare-dashboard/docs/DOCS_INDEX.md)

---

## Bu klasör neden var?

Geçmiş **dual-repository** modelinde public repo (`emraresoftware/yeni-versiyon-gecis`) için rapor mirror’ı olarak kullanılıyordu.  
AI OS V2, audit raporları ve 2026-07 sonrası task çıktıları **burada güncellenmiyor**.

---

## Ne yapmalı?

| Rol | Aksiyon |
|-----|---------|
| Agent / geliştirici | Buraya **yazma** — `docs/` kullan |
| Public repo sync | Gerekirse `docs/project-management/{reports,qa,architect}/` seçici export |
| Temizlik | Onay sonrası `project-management/` altı silinebilir veya tek sefer rsync |

---

## Public repo hâlâ kullanılıyorsa

```bash
# Örnek: yalnızca rapor katmanını sync (dry-run önce)
rsync -avn --delete \
  /Users/emre/Elyafgroup/emare-dashboard/docs/project-management/reports/ \
  /Users/emre/Elyafgroup/yeni-versiyon-gecis/docs/project-management/reports/
```

**Not:** `--delete` kullanmadan önce diff inceleyin.

---

_Legacy mirror — kanonik içerik için DOCS_INDEX.md_
