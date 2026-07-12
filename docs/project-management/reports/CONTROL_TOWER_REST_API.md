# Control Tower REST API Documentation

This document describes the REST API endpoints exposed by the Control Tower Snapshot Delivery layer.

## Base URL
`/api/v1/control-tower`

## Endpoints

### 1. Retrieve Platform Snapshot
- **URL**: `GET /snapshot`
- **Authorization**: `Admin` or `SuperAdmin` roles required
- **Response**: `ControlTowerApiResponse<ControlTowerSnapshot>`

### 2. Retrieve Snapshot Metadata
- **URL**: `GET /snapshot/metadata`
- **Response**: `ControlTowerApiResponse<SnapshotFingerprint>`

### 3. Request Snapshot Refresh
- **URL**: `POST /snapshot/refresh`
- **Query Parameter**: `scope` (defaults to `platform`)
- **Response**: `ControlTowerApiResponse<ControlTowerSnapshot>`

### 4. Retrieve Organization Snapshot
- **URL**: `GET /organizations/{organizationId}/snapshot`
- **Response**: `ControlTowerApiResponse<ControlTowerSnapshot>` (filtered)

### 5. Retrieve Workspace Snapshot
- **URL**: `GET /workspaces/{workspaceId}/snapshot`
- **Response**: `ControlTowerSnapshot`

### 6. Retrieve Domain Snapshot
- **URL**: `GET /domains/{domainId}/snapshot`
- **Response**: `ControlTowerSnapshot`

### 7. Retrieve Module Snapshot
- **URL**: `GET /modules/{moduleId}/snapshot`
- **Response**: `ControlTowerSnapshot`

### 8. Retrieve Data Quality Metrics
- **URL**: `GET /data-quality`
- **Response**: `ControlTowerDataQualitySnapshot`
