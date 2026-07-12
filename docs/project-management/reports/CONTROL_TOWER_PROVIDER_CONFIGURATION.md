# Control Tower Provider Configuration Guide

This document lists sample provider configurations mapped to C# options templates.

## AppSettings configuration example

```json
{
  "ControlTower": {
    "Providers": {
      "EngineeringMemory": {
        "Enabled": true,
        "IsRequired": true,
        "TimeoutMilliseconds": 5000,
        "FreshnessWindowMinutes": 60,
        "Roots": [
          {
            "Path": "D:\\Workspace\\EmareTicket\\docs",
            "RepositoryId": "REPO-EMARE-DOCS",
            "IsAuthoritative": true
          }
        ]
      },
      "LocalGit": {
        "Enabled": true,
        "IsRequired": false,
        "TimeoutMilliseconds": 3000,
        "Repositories": [
          {
            "CanonicalId": "REPO-EMARE-API",
            "Path": "D:\\Workspace\\EmareTicket"
          }
        ]
      },
      "RuntimeHealth": {
        "Enabled": true,
        "IsRequired": true,
        "TimeoutMilliseconds": 3000,
        "EnvironmentScope": "Development",
        "Probes": [
          {
            "CanonicalServiceId": "API-EMARE",
            "Name": "Emare Ticket API",
            "Type": "HTTP",
            "Endpoint": "http://127.0.0.1:5002/health"
          }
        ]
      },
      "RegistryPersistence": {
        "Enabled": true,
        "IsRequired": true,
        "TimeoutMilliseconds": 5000,
        "FreshnessWindowMinutes": 30
      }
    }
  }
}
```

## Options Mapping Classes
* `ControlTowerProviderOptions`
* `EngineeringMemoryProviderOptions`
* `LocalGitProviderOptions`
* `RuntimeHealthProviderOptions`
* `RegistryPersistenceProviderOptions`
