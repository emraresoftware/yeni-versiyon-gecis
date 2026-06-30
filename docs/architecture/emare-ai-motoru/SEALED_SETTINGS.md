# 🔒 SEALED_SETTINGS.md
# Gemini Live Standalone Voice Bridge — Üretim Kritik Ayarları
# Tarih: 2026-06-30 | Sürüm: v1.0
# Bu dosya değiştirilmeden önce takım onayı gerektirir.

---

## 🤖 Gemini Live Model & Ses

| Parametre | Değer | Dosya |
|---|---|---|
| `GEMINI_LIVE_MODEL` | `gemini-2.5-flash-native-audio-latest` | compose.yml / .env |
| `GEMINI_VOICE_NAME` (varsayılan) | `Puck` | compose.yml |
| Acarcell tenant voice | `Kore` (DB: EdaVoice → resolve edilir) | standalone_bridge.py |
| `thinking_budget` | `0` (thinking kapalı) | standalone_bridge.py:3079 |
| `include_thoughts` | `False` | standalone_bridge.py:3077 |
| `response_modalities` | `["AUDIO"]` | standalone_bridge.py:3073 |

---

## 🎙️ Mikrofon & Barge-In Parametreleri

| Parametre | .env (prod) | Kod default | Açıklama |
|---|---|---|---|
| `MIC_BARGE_IN_RMS` | **3200** | 2500 | Araya girme tetik eşiği |
| `MIC_BARGE_IN_FRAMES` | **12** | 8 | Tetik için ardışık frame sayısı |
| `MIC_GATE_THRESHOLD` | **800** | 800 | Konuşma başlangıç eşiği |
| `MIC_RMS_LOG_INTERVAL_SEC` | 5.0 | 5.0 | Mikrofon log aralığı |

> ⚠️ env override ile 3200 aktif. Kod içindeki 2500 default'u üretimde GEÇERSİZDİR.

---

## 🛡️ Karşılama Koruma (Greeting Protection)

| Koruma | Değer | Satır |
|---|---|---|
| `safety_timeout` | **12.0 saniye** | standalone_bridge.py ~3466 |
| Supervisor engeli (ilk N sn) | **6.0 saniye** | standalone_bridge.py ~3167 |
| Barge-in greeting kilit | `greeting_finished=False` → yalnızca `turn_complete` ile açılır | ~3724 |

> Neden 12 sn? Uzun sistem promptu (Acarcell ~600 kelime) + Gemini işlem süresi = 6-8 sn. 12 sn güvenli tampon.

---

## ⚡ L1/L2 Hybrid Cache

| Katman | TTL | Teknoloji |
|---|---|---|
| L1 (bellek) | 15 saniye | Python dict |
| L2 (Redis) | 120 saniye | Redis conf:* key prefix |
| Redis bağlantı | redis://standalone-redis:6379/0 | Docker network |
| Redis image | redis:7-alpine | compose.yml |

---

## 🔌 Servis Portları

| Servis | Port |
|---|---|
| Voice Bridge (AudioSocket) | 8095 |
| Assistant WebSocket | 8096 |
| Asterisk SIP UDP | 5060 / 5090 |
| Asterisk AMI | 5038 |
| Redis | 6379 |
| EmareTicket API (prod) | 8080 |
| Asterisk RTP | 10051–10101 UDP |

---

## 🌐 Sunucu Topolojisi

| Rol | IP |
|---|---|
| Aktif Üretim (Master) | 185.189.54.107 |
| Staging / Orkestratör | 31.169.72.85 |
| Yedek Staging | 77.92.152.3 |
| Standby | 31.169.72.82 |

---

## 🔄 HTTP API Retry

| Parametre | Değer |
|---|---|
| `BRIDGE_API_TIMEOUT_SEC` | 5.0 sn |
| `BRIDGE_API_MAX_RETRIES` | 6 |
| Fallback dizin | /tmp/voice_bridge_fallback/ |

---

## 📊 Token Loglama

| Log Etiketi | Açıklama |
|---|---|
| `[TOKENS] Canlı Tüketim ->` | Her token güncellemesinde anlık log |
| `[TOKENS] Final ->` | Arama sonunda toplam özet |
| DB | CallLogs.PromptTokens + CompletionTokens |

---

## 📡 Redis Pub/Sub Transkript

Kanal: `call:transcript:{call_uuid}`
Format: JSON `{"role": "user"|"assistant", "text": "...", "ts": <timestamp>}`

---

> 🔒 Bu dosya mühürlenmiştir.
> Değer değişikliği için: test → log doğrulama → takım onayı → bu dosyayı güncelle.
