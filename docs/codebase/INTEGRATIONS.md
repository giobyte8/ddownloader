# External Integrations

## Core Sections (Required)

### 1) Integration Inventory

| System | Type (API/DB/Queue/etc) | Purpose | Auth model | Criticality | Evidence |
|--------|---------------------------|---------|------------|-------------|----------|
| PostgreSQL | DB | Source catalog, items, jobs, scheduler job store | DB credentials from env | high | `template.env`, `ddownloader/dao/database.py`, `db/up/*.sql`, `ddownloader/download/schedulers/aio_gl_scheduler.py` |
| gallery-dl | CLI tool | Pull remote gallery content into local folders | Depends on site credentials in runtime `gdl-base.json` | high | `requirements.txt`, `ddownloader/download/gdl.py`, `config/gdl-base.template.json` |
| Central API | External HTTP API | Send download completion notifications | Bearer token (`CT_API_KEY`) | medium | `template.env`, `ddownloader/metrics/central/notifications.py` |
| OpenTelemetry collector | Telemetry backend | Export traces/metrics | Endpoint config via `OTEL_*` | medium | `template.env`, `otelw.sh`, `ddownloader/metrics/trackers/otel_tracker.py` |
| Hook callback API (self) | Internal HTTP API | Receive downloaded/skipped file callbacks from subprocess hooks | Bearer token (`API_KEY_HOOKS`) | high | `ddownloader/hooks/file_downloaded.py`, `ddownloader/web/security.py`, `ddownloader/web/api_hooks.py` |
| Preact UI -> backend API | HTTP API | Read/create/update tasks metadata in frontend | [TODO] No auth in `ui/src/services/ddownloader_service.js` | medium | `ui/src/services/ddownloader_service.js` |

### 2) Data Stores

| Store | Role | Access layer | Key risk | Evidence |
|-------|------|--------------|----------|----------|
| Postgres | Primary backend data + APScheduler jobs | Tortoise ORM + SQLAlchemy job store | Runtime/scheduler both fail if DB unavailable | `ddownloader/dao/database.py`, `ddownloader/download/schedulers/aio_gl_scheduler.py` |
| SQLite (legacy) | Legacy download-task storage / Huey queue metadata | `ddownloader/dtask_repository.py`, `ddownloader/async_tasks.py` | Legacy path drift from primary async stack | `ddownloader/dtask_repository.py`, `ddownloader/async_tasks.py` |

### 3) Secrets and Credentials Handling

- Credential sources: env vars via `.env` (`python-dotenv`) and `template.env`; gallery-dl auth material is expected in copied `config/gdl-base.json`.
- Hardcoding checks: backend uses env for DB/API keys; UI service hardcodes backend base URL (`http://192.168.1.110:5000`).
- Rotation or lifecycle notes: [TODO] No key rotation/lifecycle process documented in repo.

### 4) Reliability and Failure Behavior

- Retry/backoff behavior: no explicit retry/backoff for central notifications or hook POSTs.
- Timeout policy: `requests.head(..., timeout=5)` and `requests.get(..., timeout=60)` in legacy downloader; [TODO] no explicit timeout configured in central aiohttp notifications.
- Circuit-breaker or fallback behavior: none found.

### 5) Observability for Integrations

- Logging around external calls: yes (gallery-dl return code, central notification failures, scheduler/source logs).
- Metrics/tracing coverage: yes (OpenTelemetry spans/counters in download, DAO, and tracker paths).
- Missing visibility gaps: hook scripts print failures and exit, but no explicit retry queue or persisted dead-letter handling.

### 6) Evidence

- `template.env`
- `ddownloader/config.py`
- `ddownloader/download/gdl.py`
- `ddownloader/metrics/central/notifications.py`
- `ddownloader/web/security.py`
- `ddownloader/web/api_hooks.py`
- `ddownloader/dao/database.py`
- `db/up/1.schema.sql`
- `ddownloader/download/schedulers/aio_gl_scheduler.py`
- `ui/src/services/ddownloader_service.js`
