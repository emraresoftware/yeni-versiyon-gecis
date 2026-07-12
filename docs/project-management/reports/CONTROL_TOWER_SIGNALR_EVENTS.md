# Control Tower SignalR Events Reference

This document lists the SignalR hub subscriptions and real-time events.

## Hub Path
`/hubs/control-tower`

## Client Connection and Subscriptions
Clients must authenticate and can call:
- `SubscribeToScope(scope)`
- `UnsubscribeFromScope(scope)`

Allowed scopes are:
- `platform` (Admin only)
- `org_{organizationId}`
- `workspace_{workspaceId}`
- `domain_{domainId}`
- `module_{moduleId}`

## Hub Events Broadcasted to Groups
- **`SnapshotUpdated`**: Broadcasted when a new snapshot aggregation completes.
- **`SnapshotSectionChanged`**: Emitted when a specific section changes.
- **`RuntimeHealthChanged`**: Emitted when health check warnings change.
- **`ProviderStateChanged`**: Emitted when git state or documentation state changes.
- **`AlertRaised`**: Emitted when an operational alert is created.
- **`IncidentCreated`**: Emitted when a performance incident is created.
