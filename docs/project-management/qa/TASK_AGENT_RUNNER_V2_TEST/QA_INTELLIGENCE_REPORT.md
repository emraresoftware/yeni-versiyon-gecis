# QA Intelligence Report — TASK_AGENT_RUNNER_V2_TEST

**Engine:** QA Intelligence V2 (2.0.0)
**Mission:** `MISSION_PLATFORM_RUNTIME_V2`
**Verdict:** `QA_PASS`
**Risk:** `CRITICAL` (1282)
**Mode:** `smoke`
**Duration:** 541 ms

## Change Analysis

- Git base: `HEAD`
- Changed files: 167
- Modules: api, docs, domain, platform_runtime, tests, web

### Changed Files

- `scripts/qa-intelligence-engine-v2.py`
- `.github/workflows/sealed-voice-settings.yml`
- `EAOS_Unity_Client/Assets/EAOS/Avatars/ema/Meshy_AI_Auric_Embrace_Rigged_biped_Animation_Walking_withSkin_Material.mat`
- `EAOS_Unity_Client/Assets/EAOS/Scripts/EMAController.cs`
- `EAOS_Unity_Client/Packages/manifest.json`
- `EAOS_Unity_Client/Packages/packages-lock.json`
- `EAOS_Unity_Client/ProjectSettings/ProjectSettings.asset`
- `Mobile App/app/build.gradle`
- `Mobile App/app/src/main/java/com/emare/asistan/api/ApiClient.kt`
- `Mobile App/app/src/main/java/com/emare/asistan/api/ApiService.kt`
- `Mobile App/app/src/main/java/com/emare/asistan/data/AuthRepository.kt`
- `Mobile App/app/src/main/java/com/emare/asistan/ui/demo/DemoAgentFragment.kt`
- `Mobile App/app/src/main/java/com/emare/asistan/ui/settings/SettingsFragment.kt`
- `Mobile App/app/src/main/res/layout/fragment_settings.xml`
- `Mobile App/app/src/main/res/values/strings.xml`
- `compose.prod.yml`
- `deploy/nginx/nginx.prod.conf`
- `dev-agent-worker/package-lock.json`
- `dev-agent-worker/package.json`
- `ema-companion/macos-assistant/Sources/AppState.swift`
- `ema-companion/macos-assistant/Sources/AssistantAudioEngine.swift`
- `ema-companion/macos-assistant/Sources/ContentView.swift`
- `ema-companion/macos-assistant/Sources/VoiceProfileMatcher.swift`
- `emare-dashboard/docs/kalan-eksikler/09-mobil-superapp.md`
- `emare-dashboard/docs/product/FEATURE_TRACEABILITY_MATRIX.md`
- `emare-dashboard/docs/project-management/agents/AGENT_STATUS.md`
- `emare-dashboard/docs/project-management/agents/EVENT_DISPATCHER_LOG.md`
- `emare-dashboard/docs/project-management/agents/HANDOFF.md`
- `emare-dashboard/docs/project-management/agents/MISSION_BOARD.md`
- `emare-dashboard/docs/project-management/agents/TASK_QUEUE.md`
- `emare-dashboard/docs/project-management/agents/WORKFLOW_RUNNER_LOG.md`
- `emare-dashboard/docs/project-management/agents/event_dispatcher.py`
- `emare-dashboard/docs/project-management/agents/events.jsonl`
- `emare-dashboard/docs/project-management/agents/workflow-state.json`
- `emare-dashboard/docs/project-management/agents/workflow_runner.py`
- `emare-voice-runtime/ENV.example`
- `emare-voice-runtime/asterisk_config/generate_webrtc.sh`
- `emare-voice-runtime/asterisk_config/manager.conf`
- `emare-voice-runtime/compose.yml`
- `gemini-live-standalone/.env.example`
- … +127 more

## Test Plan

- **py_compile:event_dispatcher.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:workflow_runner.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:call_room.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:room_brain.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:originate_call.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:standalone_bridge.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:test_ami.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:test_gemini_live_direct.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:test_originate.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:agent_trigger_engine.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:create_customer_playwright.py** [PASS] — Smoke/test task — script syntax only
- **py_compile:qa-intelligence-engine-v2.py** [PASS] — Smoke/test task — script syntax only
- **bash_n:generate_webrtc.sh** [PASS] — Smoke/test task — shell syntax only
- **bash_n:generate_webrtc.sh** [PASS] — Smoke/test task — shell syntax only
- **bash_n:deploy_voice_bridge.sh** [PASS] — Smoke/test task — shell syntax only
- **bash_n:agent-control-plane-watch.sh** [PASS] — Smoke/test task — shell syntax only
- **bash_n:elyaf-staging-smoke.sh** [PASS] — Smoke/test task — shell syntax only

## Risk Hits

- `CRITICAL` — `gemini-live-standalone/.env.example`
- `CRITICAL` — `deploy/nginx/nginx.prod.conf`
- `HIGH` — `src/EmareTicket.API/Controllers/AuthController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/CallsController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/ControlTower/CrmController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/SuperAdminTenantsController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/TelephonyEventsController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/TenantAdminController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/TextToSpeechController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/VoiceBridgeController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/WhatsAppAgentController.cs`
- `HIGH` — `Mobile App/app/src/main/java/com/emare/asistan/data/AuthRepository.kt`
- `HIGH` — `scripts/tenants/open-corvis-customer.sql`
- `HIGH` — `scripts/tenants/open-emare-asistan-tenant.sql`
- `HIGH` — `scripts/tenants/seed-elyaf-department-users.sql`
- `HIGH` — `src/EmareTicket.API/Controllers/AuthController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/SuperAdminTenantsController.cs`
- `HIGH` — `src/EmareTicket.API/Controllers/TenantAdminController.cs`
- `HIGH` — `tenant-sites/corvis/corvis.tech.conf`
- `HIGH` — `tenant-sites/corvis/index.html`
- `HIGH` — `web/src/app/(auth)/login/login.css`
- `HIGH` — `web/src/app/(auth)/login/page.tsx`
- `HIGH` — `web/src/app/workspace/navigation/mock-permissions.ts`
- `HIGH` — `web/src/lib/api/whatsapp.ts`
- `MEDIUM` — `web/src/app/(auth)/login/login.css`
- `MEDIUM` — `web/src/app/(auth)/login/page.tsx`
- `MEDIUM` — `web/src/app/(dashboard)/call-center/page.tsx`
- `MEDIUM` — `web/src/app/(dashboard)/customers/import/page.tsx`
- `MEDIUM` — `web/src/app/(dashboard)/products/import/page.tsx`
- `MEDIUM` — `web/src/app/(dashboard)/whatsapp/settings/page.tsx`
- `MEDIUM` — `web/src/app/api/project-control-tower/route.ts`
- `MEDIUM` — `web/src/app/api/site/v1/route.ts`
- `MEDIUM` — `web/src/app/layout.tsx`
- `MEDIUM` — `web/src/app/workspace-control-tower/page.tsx`
- `MEDIUM` — `web/src/app/workspace/components/shell/HomeDashboard.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/activities/CrmActivities.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/activities/data/mockCrmActivities.ts`
- `MEDIUM` — `web/src/app/workspace/crm/activities/hooks/useCrmActivitiesFilters.ts`
- `MEDIUM` — `web/src/app/workspace/crm/companies/CrmCompanies.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/companies/data/mockCrmCompanies.ts`
- `MEDIUM` — `web/src/app/workspace/crm/companies/hooks/useCrmCompaniesFilters.ts`
- `MEDIUM` — `web/src/app/workspace/crm/contacts/CrmContacts.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/contacts/data/mockCrmContacts.ts`
- `MEDIUM` — `web/src/app/workspace/crm/contacts/hooks/useCrmContactsFilters.ts`
- `MEDIUM` — `web/src/app/workspace/crm/dashboard/components/CrmOverviewHeader.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/dashboard/hooks/useCrmDashboardAccess.ts`
- `MEDIUM` — `web/src/app/workspace/crm/notes-documents/CrmNotesDocuments.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/notes-documents/data/mockCrmNotesDocuments.ts`
- `MEDIUM` — `web/src/app/workspace/crm/notes-documents/hooks/useCrmNotesDocumentsFilters.ts`
- `MEDIUM` — `web/src/app/workspace/crm/opportunities/CrmOpportunities.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/opportunities/data/mockCrmOpportunities.ts`
- `MEDIUM` — `web/src/app/workspace/crm/opportunities/hooks/useCrmOpportunitiesFilters.ts`
- `MEDIUM` — `web/src/app/workspace/crm/timeline/CrmTimeline.tsx`
- `MEDIUM` — `web/src/app/workspace/crm/timeline/data/mockCrmTimeline.ts`
- `MEDIUM` — `web/src/app/workspace/crm/timeline/types.ts`
- `MEDIUM` — `web/src/app/workspace/erp/ErpAppView.tsx`
- `MEDIUM` — `web/src/app/workspace/erp/components/InventoryView.tsx`
- `MEDIUM` — `web/src/app/workspace/erp/components/ShippingView.tsx`
- `MEDIUM` — `web/src/app/workspace/navigation/NavigationRegistry.ts`
- `MEDIUM` — `web/src/app/workspace/navigation/mock-permissions.ts`
- `MEDIUM` — `web/src/app/workspace/navigation/types.ts`
- `MEDIUM` — `web/src/app/workspace/utils/animations.ts`
- `MEDIUM` — `scripts/qa-intelligence-engine-v2.py`
- `MEDIUM` — `scripts/agent-control-plane-watch.sh`
- `MEDIUM` — `scripts/agent_trigger_engine.py`
- `MEDIUM` — `scripts/create_customer_playwright.py`
- `MEDIUM` — `scripts/elyaf-staging-smoke.sh`
- `MEDIUM` — `scripts/tenants/open-corvis-customer.sql`
- `MEDIUM` — `scripts/tenants/open-emare-asistan-tenant.sql`
- `MEDIUM` — `scripts/tenants/seed-elyaf-department-users.sql`
- `LOW` — `emare-dashboard/docs/project-management/agents/AGENT_STATUS.md`
- `LOW` — `emare-dashboard/docs/project-management/agents/EVENT_DISPATCHER_LOG.md`
- `LOW` — `emare-dashboard/docs/project-management/agents/HANDOFF.md`
- `LOW` — `emare-dashboard/docs/project-management/agents/MISSION_BOARD.md`
- `LOW` — `emare-dashboard/docs/project-management/agents/TASK_QUEUE.md`
- `LOW` — `emare-dashboard/docs/project-management/agents/WORKFLOW_RUNNER_LOG.md`
- `LOW` — `emare-dashboard/docs/project-management/agents/event_dispatcher.py`
- `LOW` — `emare-dashboard/docs/project-management/agents/events.jsonl`
- `LOW` — `emare-dashboard/docs/project-management/agents/workflow-state.json`
- `LOW` — `emare-dashboard/docs/project-management/agents/workflow_runner.py`

## Warnings

- none
