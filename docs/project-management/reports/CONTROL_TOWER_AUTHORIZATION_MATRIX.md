# Control Tower Authorization Matrix

This document defines the access control roles and corresponding endpoint permissions.

| Endpoint / Action | Platform Admin (Admin) | Org Admin | Partner User | Domain Owner |
|---|---|---|---|---|
| **GET /snapshot** | Allowed (Platform) | Allowed (Filtered) | Allowed (Filtered) | Denied |
| **POST /snapshot/refresh** | Allowed | Denied | Denied | Denied |
| **GET /snapshot/metadata** | Allowed | Allowed | Allowed | Allowed |
| **SignalR platform scope** | Allowed | Denied | Denied | Denied |
| **SignalR org scope** | Allowed | Allowed (Own Org) | Allowed (Own Org) | Denied |
| **GET /data-quality** | Allowed | Allowed | Allowed | Allowed |
