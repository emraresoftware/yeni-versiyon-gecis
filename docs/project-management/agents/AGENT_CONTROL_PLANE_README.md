# Agent Control Plane - AI Company OS v1

Bu doküman, Emare BOS AI İşletim Sistemi (AI Company OS v1) üzerindeki tüm AI ajanlarının koordinasyonunu, misyon odaklı çalışma prensiplerini ve uyacakları zorunlu algoritmaları açıklar.

---

## 1. Repo-Based Coordination ve Misyon Odaklı Yapı (v1)

AI Company OS v1, ajanları sadece ufak biletler/görevler koşturan birimler olarak değil, yüksek seviyeli **Misyonların (Missions)** sahipleri (Mission Owners) olarak konumlandırır:
- **Misyonlar (`MISSION_BOARD.md`):** Projenin ana hedeflerini, kabul kriterlerini ve başarı metriklerini içerir.
- **Görevler (`TASK_QUEUE.md`):** Her görev mutlaka üst seviye bir misyona bağlıdır ve misyonun hedeflerine hizmet etmek için açılır.
- **Koordinasyon Dosyaları:** Ajanlar, git deposundaki durum dosyalarını (`MISSION_BOARD.md`, `TASK_QUEUE.md`, `WORK_IN_PROGRESS.md`, `AGENT_STATUS.md`, `HANDOFF.md`, `BLOCKERS.md`) okuyup yazarak otonom olarak koordine olur.

---

## 2. Ajan Nasıl Başlar? (Startup Algoritması)

Yeni bir ajan açıldığında veya mevcut ajan yeni bir göreve başlayacağında sırasıyla şu adımları izler:

```text
1. git pull
2. AGENTS.md oku
3. ANAYASA.md oku
4. MULTI_AGENT_COLLABORATION_PROTOCOL.md oku
5. MISSION_BOARD.md oku (Atandığı misyonun hedeflerini anla)
6. AGENT_STATE_MACHINE.md oku
7. TASK_QUEUE.md oku (Kendi misyonuna veya adına atanmış READY görev var mı doğrula)
8. WORK_IN_PROGRESS.md oku (Hedef dosyaların kilitli olmadığını gör)
9. Atanmış READY task yoksa IDLE kal
10. Varsa WORK_IN_PROGRESS.md içine lock yaz (Misyon ve görev bilgisini ekle)
11. AGENT_STATUS.md üzerinde statusü IN_PROGRESS yap
12. Göreve başla
```

---

## 3. Ajan Nasıl Görev Alır?

1. Ajan, startup aşamasında `MISSION_BOARD.md` üzerindeki aktif misyonlarını inceler.
2. `TASK_QUEUE.md` üzerinde bu misyona bağlı ve `Status` değeri `READY` olan kendi görevini belirler.
3. Kilit yazarak çalışmayı başlatır.

---

## 4. Ajan Nasıl Dosya Kilitler?

- **Eşzamanlı Çalışma Yasağı:** Aynı dosya veya klasör üzerinde aynı anda iki ajan çalışamaz.
- Ajan, üzerinde değişiklik yapacağı tüm dosya veya yolları `WORK_IN_PROGRESS.md` altındaki **Active Locks** tablosuna kaydeder.
- Kilit tablosuna `Agent`, `Mission`, `Task`, `Files / Paths`, `Started At`, `Lock Type` ve `Notes` kaydedilmelidir.
- Diğer ajanlar bu kilitleri kontrol eder ve kilitli olan dosyalara kesinlikle müdahale etmez.

---

## 5. Ajan Nasıl Handoff Yapar?

Ajan bir görevi veya misyon çıktısını başka bir ajana devredeceğinde:
1. `HANDOFF.md` dosyasına yeni bir satır ekleyerek teslim edilen çıktıyı (`Deliverable`) ve gerekli aksiyonu belirtir.
2. `TASK_QUEUE.md` dosyasındaki görevin durumunu `WAITING_QA` veya bir sonraki durum olarak günceller.

---

## 6. QA ve Mimar Onay Süreçleri

1. **QA Tetikleme:** Geliştirme tamamlandığında görev `WAITING_QA` durumuna alınır. QA ajanı (Agent 2) görevi devralarak durumu `QA_IN_PROGRESS` yapar. Testler bittiğinde `QA_TASK_XXX.md` raporunu yazar ve görevi `DONE` (veya hata varsa `FAILED` / `READY`) durumuna çeker.
2. **Architect Review Tetikleme:** Mimari kararlar veya dokümantasyon güncellemeleri tamamlandığında durum `WAITING_ARCHITECT` yapılır ve Chief Architect'in onayı beklenir.

---

## 7. Commit / Push Kuralı

- **Sadece Kullanıcı Talebiyle Push:** Ajanlar hiçbir zaman otomatik push yapamaz. Yalnızca commit oluşturabilir ve push için Owner (Kullanıcı) onayını bekler.

---

## 8. Zorunlu Completion Algoritması

Görev tamamlandığında ajan sırasıyla aşağıdaki adımları gerçekleştirir:

```text
1. Build/test çalıştır
2. Rapor oluştur (TASK_XXX_REPORT.md veya QA_TASK_XXX.md)
3. TASK_QUEUE.md güncelle (Misyon durumunu kontrol et, hedefler bittiyse MISSION_BOARD.md güncelle)
4. HANDOFF.md güncelle
5. WORK_IN_PROGRESS.md lock kaldır
6. AGENT_STATUS.md güncelle
7. Commit oluştur (Mesaj: feat/fix/docs(scope): aciklama)
8. Push yapma; push için owner onayı bekle
9. Final teslim formatı ver
```

### Final Teslim Formatı

Ajan, görev bittiğinde kullanıcıya **yalnızca ve kesinlikle** aşağıdaki şablonda çıktı sunar:

```text
TASK: [GÖREV_ID]
STATUS: [DURUM]
COMMIT: [COMMİT_MESAJI]
FILES CREATED:
- [YENİ_OLUŞTURULAN_DOSYA_1]
FILES MODIFIED:
- [DEĞİŞTİRİLEN_DOSYA_1]
BLOCKERS:
- [ENGEL_1_VEYA_NONE]
NEXT RECOMMENDATION: [SONRAKİ_ADIM_ÖNERİSİ]
```

---

## 10. Otonom Tetikleme Motoru (Trigger Engine)

Sistem, Cursor (Agent 1) ve Antigravity (Agent 0, Agent 2) arasındaki geçişleri otomatikleştirmek için bir tetikleme motoru barındırır:
- **Git Post-Commit Hook (`.git/hooks/post-commit`):** Herhangi bir ajan (Cursor veya Antigravity) commit attığı anda arka planda [agent_trigger_engine.py](file:///Users/emre/Elyafgroup/scripts/agent_trigger_engine.py) betiğini tetikler.
- **Durum Analizi ve Güncelleme:** Betik, son commit mesajındaki Task ID'yi (Örn: `TASK_018_CLEAN`) tespit eder.
  - İlgili görevin durumunu `TASK_QUEUE.md` üzerinde `WAITING_QA` veya `DONE` yapar.
  - Bir sonraki aşamadaki ajanın durumunu `AGENT_STATUS.md` üzerinde `READY` veya `QA_ASSIGNED` konumuna getirir.
  - Bağımlılıkları kontrol ederek, tamamlanan işlerin unblok ettiği görevleri otomatik olarak `READY` durumuna geçirir.
- **Kullanıcı Bildirimleri:** Durum geçişleri sırasında macOS bildirim sistemi (`osascript`) üzerinden kullanıcıya masaüstü bildirimleri gönderir.
- **Otomatik Commit:** Durum güncellemelerini (`TASK_QUEUE.md`, `AGENT_STATUS.md`) otomatik olarak sahneye alır (stage) ve `docs(agents): auto-update status...` mesajıyla commit eder (sonsuz döngüyü önlemek için bu commit'ler tetikleyiciyi pas geçer).
- **Ev Dizinleri ve GOREV/UYANDIR Dosyaları:** Tetikleyici motor, durum geçişi yapıldığında `/Users/emre/Ai Agent/` altındaki ilgili ajanın ev dizinindeki `GOREV.md` dosyasını otomatik olarak `BEKLIYOR` veya `TAMAM` durumuna getirir. Ajanlar bu ev dizinlerinde çalışmaya başlar ve `@UYANDIR.md` ile uyandırılır.
- **Arka Plan İzleyici (Watcher):** Terminalde `./scripts/agent-control-plane-watch.sh` komutu koşturularak, ev dizinlerindeki `GOREV.md` dosyalarındaki `durum: BEKLIYOR` geçişleri anlık olarak izlenir ve macOS bildirim penceresiyle kullanıcı uyarılır.


