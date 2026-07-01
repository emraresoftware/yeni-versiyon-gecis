# Implementation Plan - TASK-EMA-ACTION-001 Action Engine

Ema Companion beynine (`ema_brain.py`) kullanıcının açık onayı doğrultusunda küçük geliştirme ve dosya düzenleme adımlarını (Dry Run, Whitelist kontrolü, Verify ve Rollback desteği ile) güvenli bir şekilde kendi kendine yapabilmesi için Action Engine katmanının entegre edilmesi.

## Proposed Changes

### [Modify] [ema_brain.py](file:///Users/emre/Elyafgroup/ema-companion/ema_brain.py)
- `build_command_sequence(task)` metodu eklenerek checkout, edit, diff, test ve build adımları sıraya alınacak.
- `get_dry_run_summary(sequence)` metodu eklenerek yapılacak işler listelenecek ve onay istenecek.
- `execute_action_sequence(sequence)` metodu eklenerek sadece whitelist'e uygun kabuk komutları koşturulacak ve verify adımları işletilecek.
- `rollback_actions(history)` metodu eklenerek hata anında yapılan değişiklikler geri alınacak.

### [Modify] [test_ema_brain.py](file:///Users/emre/Elyafgroup/ema-companion/test_ema_brain.py)
- Test 10 eklenerek Dry Run çıktısının formatı ve onay sonrasında güvenli yürütüm/özet akışı doğrulanacak.

---

## Verification Plan

### Automated Tests
- `python3 test_ema_brain.py` komutu çalıştırılarak Test 10 doğrulaması yapılacak.
