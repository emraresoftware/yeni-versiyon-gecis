# Test Report — TASK_MSG_003

## Pre-flight Check
PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

---

## Test Executed
Ran the full test suite and targeted normalizer tests via `dotnet test`.

## Test Scenarios Covered in `MessageNormalizerTests.cs`

### 1. Meta Messenger Normalization
* `Messenger_Normalize_Text_ShouldExtractCorrectFields`: Validates mapping of text payloads, Unix epoch timestamps (ms), sender/recipient identities, and page accounts.
* `Messenger_Normalize_Attachment_ShouldExtractAttachmentUrls`: Validates parsing of multiple media attachments (images, video) and mime-type mappings.
* `Messenger_Normalize_Reaction_ShouldExtractReactionMetadata`: Validates parsing of emojis, target message IDs, and actions (e.g. `react`).

### 2. WhatsApp Cloud API Normalization
* `WhatsApp_Normalize_Text_ShouldExtractCorrectFields`: Validates WA text body parsing, WA Unix epoch (seconds) timestamp, and WaId.
* `WhatsApp_Normalize_Image_ShouldExtractMediaAttachments`: Validates parsing of WA media IDs and captions.
* `WhatsApp_Normalize_Document_ShouldExtractDocumentAttachments`: Validates document mime types.
* `WhatsApp_Normalize_DeliveryStatus_ShouldCreateStatusUpdateEnvelope`: Verifies delivered status mapping.
* `WhatsApp_Normalize_ReadStatus_ShouldCreateStatusUpdateEnvelope`: Verifies read status mapping.

### 3. Web Widget Normalization
* `WebWidget_Normalize_Text_ShouldExtractFieldsCorrectly`: Validates widget message fields, tenant UUID, and files.
* `WebWidget_Normalize_Reconnect_ShouldRecognizeReconnectMetadata`: Validates reconnect payload mapping.

### 4. Negative Test Scenarios
* `Messenger_Normalize_InvalidPayload_ShouldThrow`: Validates behavior on empty payload structures.
* `WhatsApp_Normalize_MalformedJson_ShouldThrow`: Verifies exception propagation on malformed JSON payload strings.
* `WebWidget_Validate_MalformedJson_ShouldReturnFalse`: Verifies validation failure on malformed input streams.

---

## Output Metrics
* **Total Executed Tests:** 718
* **Passed Tests:** 718
* **Failed Tests:** 0
* **OMC Specific Tests:** 24
* **Average Execution Duration:** ~2s
