# Implementation Plan - TASK-EMA-EVENTBUS-001 Event Bus Backbone

Ema OS bileşenlerinin (Observer, Brain, Memory, Action Engine vb.) birbirine sıkı sıkıya bağlı (tightly coupled) çalışmasını önlemek amacıyla merkezi, in-memory ve hafif bir Event Bus omurgasının tasarlanması ve entegre edilmesi.

## Proposed Changes

### [New] [ema_event_bus.py](file:///Users/emre/Elyafgroup/ema-companion/ema_event_bus.py)
- `EmaEvent` modelinin oluşturulması (`id`, `type`, `source`, `timestamp`, `payload`, `priority`, `requires_approval`).
- `EmaEventBus` sınıfının implemente edilmesi (`publish`, `subscribe`, `get_recent`, `clear` metotları).

### [Modify] [ema_brain.py](file:///Users/emre/Elyafgroup/ema-companion/ema_brain.py)
- Observer aktif gözlemlerinde (uygulama/git/hata değişiklikleri) Event Bus üzerinden `workspace.changed`, `git.status.changed`, `terminal.error` eventlerinin yayınlanması.
- Brain context oluşturulurken (`build_context`) son event geçmişinin context içine enjekte edilmesi.
- Action Engine onay ve tamamlanma durumlarında (`action.approval.required`, `action.completed`, `build.started`, `build.finished`, `test.finished`) event yayınlanması.

### [Modify] [test_ema_brain.py](file:///Users/emre/Elyafgroup/ema-companion/test_ema_brain.py)
- Test 11 eklenerek event pub/sub, observer event, brain context event ve approval event davranışlarının doğrulanması.

---

## Verification Plan

### Automated Tests
- `python3 test_ema_brain.py` test suite koşturularak tüm event bus entegrasyonlarının başarılı olduğu doğrulanacaktır.
