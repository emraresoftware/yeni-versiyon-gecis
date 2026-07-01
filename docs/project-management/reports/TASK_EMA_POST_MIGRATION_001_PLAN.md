# Implementation Plan - TASK-EMA-POST-MIGRATION-001 Post-Migration Verification

Ayrıştırılan Voice Core (`emare-voice-runtime`) ve Ema Companion (`ema-companion`) repository'lerinin günlük geliştirme ve kullanım akışlarına uygunluğunun doğrulanması ve post-migration audit işlemlerinin tamamlanması.

## Proposed Verification Actions

### 1. Ema Companion Derleme & Test
- macOS companion app release paketi oluşturma testi (`./scripts/build_app.sh`).
- EmaBrain entegrasyon testi (`test_ema_brain.py`).
- Unity metadata/assets klasör yapısının doğrulanması.

### 2. Voice Runtime Doğrulama
- Docker Compose entegrasyon kontrolü (`docker compose config`).
- Python kod sözdizimi doğrulamaları (`py_compile`).

### 3. Monolit Yönlendirme Kontrolü
- Monolit içindeki eski `gemini-live-standalone/` README dosyasının yönlendirmeyi doğru yansıtıp yansıtmadığının kontrolü.
