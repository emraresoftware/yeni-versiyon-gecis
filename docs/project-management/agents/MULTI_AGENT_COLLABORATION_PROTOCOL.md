# Multi-Agent Collaboration Protocol v1.0

**Status:** Approved  
**Owner:** Agent 0 (Coordinator)  
**Last Updated:** 2026-06-28  
**Related:** `DEVELOPMENT_PROTOCOL.md`, `AGENTS.md`, `ANAYASA.md`

---

## Amaç

Bu protokol, Emare Ai Dashboard kod tabanında paralel çalışan AI ajanlarının çakışmadan, izlenebilir ve güvenli şekilde işbirliği yapmasını tanımlar.

Kod üreten veya dokümantasyon güncelleyen **tüm ajanlar** oturum başında bu dosyayı okumalıdır.

---

## Ajan Rolleri ve Sahiplik

| Agent | Rol | Birincil yazma alanı |
| ----- | ---- | -------------------- |
| Agent 0 | Coordinator | `emare-dashboard/docs/project-management/agents/` |
| Agent 1 | Developer | `src/`, `tests/` |
| Agent 2 | QA | `docs/project-management/qa/` |
| Agent 3 | Product | `docs/product/` |
| Agent 4 | Security | `docs/project-management/security/` |
| Agent 5 | Control Tower | `docs/control-tower/` |
| Agent 6 | Legacy | `docs/legacy/` (kanonik mirror: `yeni-versiyon-gecis`) |

**Kural:** Bir ajan, sahip olmadığı dizinde kod veya kalıcı doküman değişikliği yapmaz. İstisna: Coordinator onaylı handoff veya acil hotfix (Agent 0 kaydı zorunlu).

---

## Zorunlu Koordinasyon Dosyaları

Tüm ajanlar aşağıdaki dosyaları kullanır (`emare-dashboard/docs/project-management/agents/`):

| Dosya | Amaç |
| ----- | ---- |
| `AGENT_STATUS.md` | Kim aktif, hangi görevde |
| `TASK_QUEUE.md` | Öncelikli backlog |
| `WORK_IN_PROGRESS.md` | Dosya kilidi — eşzamanlı düzenleme yasağı |
| `HANDOFF.md` | Görev devir mesajları |
| `BLOCKERS.md` | İlerlemeyi durduran engeller |
| `DECISIONS.md` | Mimari / süreç kararları |

---

## Oturum Başlangıcı (Startup)

Her ajan açıldığında sırasıyla:

1. `git pull` (yalnızca kullanıcı onayı veya protokol gerektiriyorsa)
2. `AGENTS.md` oku
3. `Yeni versiyon geçiş/ANAYASA.md` oku
4. **Bu dosya** — `MULTI_AGENT_COLLABORATION_PROTOCOL.md`
5. `WORK_IN_PROGRESS.md` oku — kilitli dosyalara dokunma
6. `TASK_QUEUE.md` oku — atanmış görevi doğrula
7. Agent workspace `CURRENT_TASK.md` güncelle
8. Çalışmaya başla

---

## WIP (Work In Progress) Kilidi

> **CONCURRENCY RULE:** İki ajan aynı anda aynı dosyada çalışamaz.

### Başlamadan önce

1. `WORK_IN_PROGRESS.md` içinde hedef dosyaların kilitli olmadığını doğrula.
2. Görevi WIP'e kaydet: Agent adı, dosya listesi, başlangıç zamanı, tahmini bitiş.
3. `AGENT_STATUS.md` → durumu `ACTIVE` yap.

### Bitirirken

1. WIP kaydını kaldır veya `COMPLETED` olarak işaretle.
2. Gerekirse `HANDOFF.md`'ye devir yaz.
3. `AGENT_STATUS.md` → `IDLE` veya sıradaki duruma güncelle.

---

## Handoff Protokolü

Görev başka ajana geçtiğinde `HANDOFF.md`'ye yeni kayıt ekle:

```markdown
### [ISO-8601 timestamp] Kaynak (Agent X) ➔ Hedef (Agent Y)
- **Status:** ...
- **Context:** ...
- **Action Required:** ...
```

Alıcı ajan handoff'u okumadan dosyaya müdahale etmez.

---

## Blocker Protokolü

İlerleme durduğunda:

1. `BLOCKERS.md`'ye engeli yaz (neden, etki, ihtiyaç duyulan karar).
2. `AGENT_STATUS.md`'de ilgili görevi `BLOCKED` işaretle.
3. Mimari belirsizlikte Chief Architect kararı bekle — **sessiz varsayım yasak** (`ANAYASA.md` Article 3).

---

## Kod ve Deploy Kuralları

- **Commit / push:** Yalnızca kullanıcı açıkça istediğinde.
- **Deploy (prod, staging, SSH, rsync):** Yalnızca kullanıcı açıkça onayladığında.
- **Mimari değişiklik:** ADR + Chief Architect onayı olmadan yapılmaz.
- **Pre-flight (kod üretimi):** `AGENTS.md` + `ANAYASA.md` + ilgili domain/güvenlik dokümanları.

---

## Çakışma Çözümü

| Durum | Aksiyon |
| ----- | ------- |
| İki ajan aynı dosyayı WIP'e yazdı | Agent 0 karar verir; düşük öncelikli ajan durur |
| WIP güncel değil | Agent 0 WIP'i düzeltir; ajanlar stale kayda güvenmez |
| Handoff eksik | Alıcı ajan çalışmaya başlamaz; Coordinator'dan net devir ister |

---

## Yasaklar

- Başka ajanın WIP kayıtlı dosyasını düzenlemek
- `HANDOFF.md` / `TASK_QUEUE.md` güncellemeden görev devretmek
- Onaysız deploy veya force push
- Agent sahipliği dışında kalıcı kod değişikliği (Agent 1 dışında `src/` vb.)

---

## Ana İlke

Paralel hız önemlidir; **dosya çakışması ve izlenemeyen değişiklik** kabul edilemez. Şüphede WIP'e bak, handoff yaz, Coordinator'a sor.
