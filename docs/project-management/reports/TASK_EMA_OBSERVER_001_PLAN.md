# Implementation Plan - TASK-EMA-OBSERVER-001 Workspace Observer

Ema Companion beynine (`ema_brain.py`) kullanıcının aktif çalışma alanı durumlarını (aktif uygulama, aktif pencere, açık proje dizini, git branch/status, VS Code açık dosyaları ve terminal son hata logu) izleme yeteneğinin eklenmesi.

## Proposed Changes

### [Modify] [ema_brain.py](file:///Users/emre/Elyafgroup/ema-companion/ema_brain.py)
- `get_observer_data()` metodu eklenerek AppleScript, git ve dosya sistemi üzerinden aktif ortam bilgileri okunacak.
- `build_context()` metodu güncellenerek okunan tüm gözlemler Gemini prompt context'ine beslenecek.

### [Modify] [test_ema_brain.py](file:///Users/emre/Elyafgroup/ema-companion/test_ema_brain.py)
- Test 8 eklenerek izleyici (Observer) katmanının bütün çıktılarının doğruluğu test edilecek.

### [Modify] [README.md](file:///Users/emre/Elyafgroup/ema-companion/README.md)
- VS Code / Cursor dosya algılama ve terminal son hata kancası (shell hook) kurulum yönergeleri eklenecek.

---

## Verification Plan

### Automated Tests
- `python3 test_ema_brain.py` komutu koşturularak Test 8 (Workspace Observer) çıktısının doğrulanması.
