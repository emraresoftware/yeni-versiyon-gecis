# Implementation Plan - TASK-EMA-CONTROLLED-MIGRATION-001 Controlled Migration

Ema Desktop Assistant ve Voice Core altyapısının yeni bağımsız repository iskeletlerine kopyalanması, derleme ve entegrasyon testlerinin yapılması ve monolit üzerinde yönlendirmenin sürdürülmesi.

## Proposed Changes

### [Copy] Voice Core Files to `emare-voice-runtime/`
- `standalone_bridge.py`
- `voice_provider.py`
- `gemini_live_adapter.py`
- `compose.yml`
- `requirements.txt`
- `asterisk_config/` (dizin)
- Tüm yardımcı Python bridge dosyaları.

### [Copy] Ema Companion Files to `ema-companion/`
- `macos-assistant/` (dizin)
- `ema_brain.py`
- `test_ema_brain.py`
- `EAOS_Unity_Client/` (Assets, Packages, ProjectSettings)
- `docs/eaos/` (Ema & Unity dokümantasyonu)

---

## Verification Plan

### Automated Tests
1. **Voice Runtime:**
   - `docker compose config` kontrolünün yapılması.
   - `python3 -m py_compile standalone_bridge.py` ile import ve sözdizimi kontrolü.
2. **Ema Companion:**
   - Swift derleme kontrolü: `swift build -Xswiftc -module-cache-path -Xswiftc .build/ModuleCache`
   - EmaBrain entegrasyon testi: `python3 test_ema_brain.py`
