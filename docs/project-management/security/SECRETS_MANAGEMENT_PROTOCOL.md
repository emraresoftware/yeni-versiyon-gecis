# Secrets Management Protocol (SECRETS_MANAGEMENT_PROTOCOL.md)

**Title:** Secrets and API Key Management Protocol
**Version:** 1.0.0
**Status:** Approved
**Owner:** Chief Technology Officer (CTO)
**Last Updated:** 2026-07-13

---

## 🔒 1. Secrets Security Classification

To prevent key leaks, all keys are classified into three tiers:

### Tier 1: System Master Keys (Highly Confidential)
* **Description:** Master keys that protect database access, encrypt data, or generate authentication tokens.
* **Keys:**
  * `JWT_SECRET_KEY`: Used to sign and verify JSON Web Tokens (JWT).
  * `ENCRYPTION_KEY`: 32-character AES key for encrypting sensitive fields (e.g., SMTP passwords).
* **Storage:** strictly in server environment variables or Docker Secrets. Never committed to git.

### Tier 2: Third-Party Provider Keys (Confidential)
* **Description:** API keys for external service providers (AI models, telephony, voice synthesis).
* **Keys:**
  * `GROK_API_KEY`: Grok/xAI model integration.
  * `GEMINI_API_KEY`: Google Gemini LLM & VAD integrations.
  * `Cartesia__ApiKey`: Cartesia TTS voice API integration.
  * `ElevenLabs__ApiKey`: ElevenLabs TTS/STT fallback voice integration.
* **Storage:** Configured in `.env` locally for developers, and in central environment configs on production nodes.

### Tier 3: Internal Integration Keys (Restricted)
* **Description:** Local API keys used to authenticate services running within the docker network or local microservices.
* **Keys:**
  * `Telephony__ApiKey` / `Telephony__WebhookSecret`: Telephony system connection security.
  * `VOICE_BRIDGE_SERVICE_KEY`: Key shared between voice bridge and CRM API.
  * `WhatsAppQrBridge__WebhookSecret` / `WhatsAppQrBridge__ApiKey`: Evolution/Baileys bridge integration.
* **Storage:** Stored in configuration files or docker-compose environment vars.

---

## 📂 2. Keys and Environment Mapping Schema

| Config Key | Naming Convention (Environment) | Provider | Tier | Usage Scope |
|---|---|---|---|---|
| JWT Key | `JWT_SECRET_KEY` | JWT Auth | Tier 1 | Sign/verify auth tokens |
| DB Conn | `DB_CONNECTION_STRING` | PostgreSQL | Tier 1 | DbContext database connections |
| Encrypt | `ENCRYPTION_KEY` | AES-256 | Tier 1 | Encrypt SMTP passwords / secrets |
| Grok API | `GROK_API_KEY` | xAI / Grok | Tier 2 | LLM integrations & fallback |
| Gemini API | `GEMINI_API_KEY` | Google Gemini | Tier 2 | Primary STT/LLM/TTS processing |
| Cartesia API | `Cartesia__ApiKey` | Cartesia | Tier 2 | High-fidelity voice synthesis |
| ElevenLabs | `ElevenLabs__ApiKey` | ElevenLabs | Tier 2 | Voice synthesis (fallback) |
| Telephony API | `Telephony__ApiKey` | Asterisk Bridge | Tier 3 | Telephony API authentication |
| Voice Bridge Key | `VOICE_BRIDGE_SERVICE_KEY` | Bridge API | Tier 3 | Auth between bridge & API |

---

## ⚡ 3. Key Rotation & Backup Strategy

1. **Automation:** Key rotations are triggered via CI/CD deployment or manually by the CTO using environment manager scripts.
2. **Production Rotation:** Tier 1 keys MUST be rotated every 90 days or immediately upon team membership changes.
3. **Mock Defaults:** The codebase uses fallback placeholder values for development environments (`compose-placeholder`, `Development`), ensuring the application can run out-of-the-box in local development mode without exposing production keys.
