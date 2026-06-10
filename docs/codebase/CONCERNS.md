# Codebase Concerns

## Core Sections (Required)

### 1) Top Risks (Prioritized)

| Severity | Concern | Evidence | Impact | Suggested action |
|----------|---------|----------|--------|------------------|
| high | Runtime architecture split between active async Quart/Postgres path and legacy Flask/Huey/SQLite modules | `ddownloader/main.py`, `ddownloader/web/app.py`, `ddownloader/web/api.py`, `ddownloader/async_tasks.py`, `ddownloader/dtask_repository.py` | Ambiguous ownership and maintenance risk; regressions can hide in dormant/partially wired paths | [ASK USER] decide canonical backend path and deprecate/archive the other |
| high | DB reset script references `schema.sql` that is not present in `db/` | `db/reset.sh`, `db/up/1.schema.sql`, `db/up/2.jobs_monitoring.sql`, `db/` | New environment setup can fail or apply wrong migration flow | Align `reset.sh` with `db/up/*.sql` migration strategy |
| medium | Frontend hardcodes backend host/IP | `ui/src/services/ddownloader_service.js` | Breaks portability across environments and deployments | Move UI API base URL to environment/config |
| medium | Hook/API key model is single shared secret string comparison | `template.env` (`API_KEY_HOOKS`), `ddownloader/web/security.py` | Weak key management and no per-client revocation/audit | Introduce key store/rotation policy and stronger auth model |
| low | Central notification integration catches broad exceptions and logs only | `ddownloader/metrics/central/notifications.py` | Notification failures can be noisy or silent without retries | Add explicit timeout/retry strategy and structured failure metrics |

### 2) Technical Debt

| Debt item | Why it exists | Where | Risk if ignored | Suggested fix |
|-----------|---------------|-------|-----------------|---------------|
| Logging setup TODO | Incomplete historical logging refactor | `ddownloader/__init__.py` | Inconsistent logging outputs and maintenance overhead | Consolidate logging setup and remove dead commented code |
| File service cache TODOs | Performance optimization deferred | `ddownloader/services/file_svc.py` | Repeated DB lookups per file operation | Add measured cache with invalidation strategy |
| Mixed old/new API models | Migration appears incomplete | `ddownloader/web/api.py` vs `ddownloader/web/app.py`/`api_hooks.py` | Team confusion over supported endpoints/contracts | Mark deprecated modules and enforce one API surface |

### 3) Security Concerns

| Risk | OWASP category (if applicable) | Evidence | Current mitigation | Gap |
|------|--------------------------------|----------|--------------------|-----|
| Single static bearer token for hooks | A07: Identification and Authentication Failures | `ddownloader/web/security.py`, `template.env` | Requires `Authorization: Bearer ...` header | No rotation/audit/per-client scoping |
| Potential sensitive config in local files | N/A | `template.env`, `config/gdl-base.template.json`, `README.md` instructions to add cookies | Template separates placeholders from runtime values | [TODO] No explicit secret-scanning or policy config in repo |
| Legacy API modules may expose routes without current auth model | A01: Broken Access Control [TODO verify runtime wiring] | `ddownloader/web/api.py`, `ddownloader/web/dtask_service.py` | Hook routes are protected | [ASK USER] confirm whether legacy routes are still served |

### 4) Performance and Scaling Concerns

| Concern | Evidence | Current symptom | Scaling risk | Suggested improvement |
|---------|----------|-----------------|-------------|-----------------------|
| File cleanup loops delete files sequentially | `ddownloader/hooks/source_downloaded.py` | Slower cleanup for large source sets | Long post-download processing windows | Batch/parallelize safely with bounded concurrency |
| Hook callback per file via subprocess HTTP | `ddownloader/download/gdl.py`, `ddownloader/hooks/file_downloaded.py` | High overhead when many files are downloaded/skipped | Increased local HTTP load and event lag | Consider buffered/batch event reporting mode |
| UI API host fixed to LAN address | `ui/src/services/ddownloader_service.js` | UI fails outside one network | Blocks scale to multiple envs | Configure via env at build/runtime |

### 5) Fragile/High-Churn Areas

| Area | Why fragile | Churn signal | Safe change strategy |
|------|-------------|-------------|----------------------|
| Download pipeline (`download/`, `hooks/`, `metrics/`) | Cross-module coupling across scheduler, subprocess, HTTP callbacks, and trackers | [TODO] recent-commit churn hotspot not determinable from repository files alone | Change with integration-style tests around full event flow |
| DB bootstrap/migrations (`db/`, `dao/database.py`) | Runtime startup depends on DB schema compatibility and env correctness | [TODO] commit churn mapping needed from git history analytics | Validate migration path in disposable DB before release |

### 6) `[ASK USER]` Questions

1. [ASK USER] Is the canonical backend stack now Quart + async download scheduler + Postgres, and can `web/api.py`, `dtask_service.py`, `async_tasks.py`, and `dtask_repository.py` be treated as deprecated?
2. [ASK USER] Should the UI under `ui/` still be maintained as an active product surface, or is the Jinja UI under `ddownloader/web/templates/` the intended primary interface?
3. [ASK USER] Do you want hook/API authentication to remain a single shared API key, or should this move to multi-key/identity-backed auth?
4. [ASK USER] What is the intended migration workflow (`db/up/*.sql` vs `db/reset.sh`), and should reset script behavior be corrected to match current schema layout?

### 7) Evidence

- `ddownloader/main.py`
- `ddownloader/web/app.py`
- `ddownloader/web/api.py`
- `ddownloader/async_tasks.py`
- `ddownloader/dtask_repository.py`
- `ddownloader/services/file_svc.py`
- `ddownloader/hooks/source_downloaded.py`
- `ddownloader/download/gdl.py`
- `ddownloader/metrics/central/notifications.py`
- `db/reset.sh`
- `db/up/1.schema.sql`
- `db/up/2.jobs_monitoring.sql`
- `ui/src/services/ddownloader_service.js`
- `template.env`
