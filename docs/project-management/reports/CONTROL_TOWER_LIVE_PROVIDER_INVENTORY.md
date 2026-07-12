# Control Tower Live Provider Inventory

This document defines the live provider inventory feeding the Control Tower aggregation core.

## 1. Engineering Memory Provider
- **Class**: `EngineeringMemoryProvider`
- **Abstractions**: `IEngineeringMemoryProvider`
- **Goal**: Scans Markdown ADRs, current status docs, tasks, risks, and technical debt registers.
- **Classification Types**: ADR, Architecture, CurrentStatus, Task, Sprint, Report, Risk, TechnicalDebt, Runbook, DomainDocumentation, Unknown.

## 2. Local Git State Provider
- **Class**: `LocalGitStateProvider`
- **Abstractions**: `ILocalGitStateProvider`
- **Goal**: Discovers HEAD SHA, current branch, dirty workspace state, and uncommitted/untracked files.
- **Access Level**: Read-only process commands (`git status`, `git rev-parse`).

## 3. Runtime Health Provider
- **Class**: `RuntimeHealthProvider`
- **Abstractions**: `IRuntimeHealthProvider`
- **Goal**: Probes API availability and database/cache connections.
- **Types**: HTTP, DB, Cache, queue.

## 4. Canonical Registry Persistence Provider
- **Class**: `CanonicalRegistryPersistenceProvider`
- **Abstractions**: `ICanonicalRegistryPersistenceProvider`
- **Goal**: Queries organizations, workspaces, domains, modules, and workflows.
- **Isolation Scope**: Standard multi-tenant isolation applied.
