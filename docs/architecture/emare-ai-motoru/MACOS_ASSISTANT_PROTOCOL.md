# macOS Assistant WebSocket Protocol

The desktop assistant uses a dedicated WebSocket endpoint and does not connect
to the Asterisk AudioSocket port.

## Endpoint

```text
ws://<bridge-host>:8096
```

## Start Message

The first client message must be JSON:

```json
{
  "type": "start",
  "did": "90850...",
  "callerPhone": "905...",
  "assistantKey": "optional-shared-key"
}
```

`did` and `callerPhone` are resolved through the existing voice bridge API so
tenant isolation, Gemini key lookup, and CRM context stay server-side.

## Server Ready

```json
{
  "type": "ready",
  "callReference": "desktop-...",
  "inputAudio": "audio/pcm;rate=16000",
  "outputAudio": "audio/pcm;rate=24000"
}
```

## Audio

- Client sends binary PCM16 mono at 16 kHz.
- Server sends binary PCM16 mono at 24 kHz.

## Text Control

```json
{ "type": "text", "text": "Merhaba" }
{ "type": "ping" }
{ "type": "stop" }
```

## Server Events

```json
{ "type": "transcript", "speaker": "user", "text": "..." }
{ "type": "transcript", "speaker": "assistant", "text": "..." }
{ "type": "tool_result", "name": "create_support_ticket", "result": {} }
{ "type": "turn_complete" }
{ "type": "interrupted" }
{ "type": "error", "message": "..." }
```

## Security Boundary

The macOS client never receives the tenant Gemini API key. Business actions are
executed by the bridge using the existing API-backed tool handler.
