# Implementation Plan - TASK_MSG_003: Message Normalizer

## Objective
Implement and decouple the inbound normalization logic (`InboundMessageEnvelope` parsing) across core communication adapters (WhatsApp, Meta Messenger, LiveChat/Web Widget, Email). The aim is to convert raw provider webhook payloads into unified structures warning-free.

## Scope of TASK_MSG_003
1. **Refining the Adapter Interfaces:** Establish concrete normalization contract details on `IChannelAdapter` for parsing payloads.
2. **Payload Normalizers:** Create normalizer implementations or parser helpers for:
   * **Meta Messenger Webhook:** Parse entry objects, messaging events, text, quick replies, media attachments, and sender IDs.
   * **WhatsApp Cloud API Webhook:** Parse messages, text body, media ids, locations, interactive button selections, and client phone numbers.
   * **LiveChat / Web Widget:** Parse widget chat message events and uploaded file attachment arrays.
3. **Mime Type and Media Mapping:** Standardize mapping of attachments from provider media links to `MessageAttachment` contracts.
4. **Integration Tests:** Write a suite verifying correct parsing of raw webhook JSON payloads against actual Meta and WhatsApp payloads.

---

## Proposed Changes

### Application Layer (`EmareTicket.Application`)

#### [MODIFY] [IChannelAdapter.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Application/Abstractions/Messaging/IChannelAdapter.cs)
* Extend normalizer abstractions to support explicit payload signature parsing and attachment file parsing.

### Infrastructure Layer (`EmareTicket.Infrastructure`)

#### [NEW] [MessengerPayloadNormalizer.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Normalizers/MessengerPayloadNormalizer.cs)
* Implements parsing logic for Meta Messenger JSON payloads. Extends extraction of message body, attachments (images, video, audio), external conversation IDs, and user profile metadata.

#### [NEW] [WhatsAppPayloadNormalizer.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Normalizers/WhatsAppPayloadNormalizer.cs)
* Implements parsing logic for WhatsApp Business Cloud API JSON payloads. Extracts text, button selections, interactive messages, geographic locations, and media tokens.

#### [NEW] [WebWidgetPayloadNormalizer.cs](file:///Users/emre/Elyafgroup/src/EmareTicket.Infrastructure/Services/Messaging/Normalizers/WebWidgetPayloadNormalizer.cs)
* Normalizes incoming Web Widget/LiveChat SignalR or HTTP message events.

### Test Layer (`EmareTicket.Tests`)

#### [NEW] [MessageNormalizerTests.cs](file:///Users/emre/Elyafgroup/tests/EmareTicket.Tests/Messaging/MessageNormalizerTests.cs)
* Contains unit tests validating normalization pipelines with raw Meta Messenger and WhatsApp webhook JSON mock files.

---

## Verification Plan

### Automated Verification
* Execute test suite on sample mock payloads:
  `dotnet test --filter "FullyQualifiedName~MessageNormalizerTests"`
* Verify zero compile errors on build:
  `dotnet build EmareTicket.sln -c Release`
