# Architecture

## Core Sections (Required)

### 1) Architectural Style

- Primary style: layered async service with event-driven tracking.
- Why this classification: request handlers (`web/`) call DAOs/services; download execution is scheduled asynchronously and emits events to tracker subscribers.
- Primary constraints:
  1. Scheduler and ORM both depend on reachable Postgres.
  2. gallery-dl execution relies on local filesystem and subprocess execution.
  3. Hook callbacks depend on in-process HTTP endpoints and API key config.

### 2) System Flow

```text
main.py -> Quart startup -> DB init + scheduler init -> gallery-dl subprocess -> hook callbacks -> EventHub trackers -> DB/UI updates
```

Flow details:
1. `ddownloader/main.py` starts Quart and runs `before_serving`.
2. `before_serving` initializes Tortoise DB (`dao/database.py`) and launches `download_svc.start()`.
3. `download_svc.start()` loads enabled sources and schedules jobs via `AIOGalleryDlScheduler`.
4. `GalleryDownloader.download()` marks source state, invokes `gdl.download()`, and emits start/end events.
5. `gdl.download()` runs `gallery-dl` with hook commands (`hooks/file_downloaded.py`, `hooks/file_skipped.py`).
6. Hook scripts POST into `/api/hooks/...`; `web/api_hooks.py` upserts items and emits `FILE_DOWNLOADED`/`FILE_SKIPPED`.
7. `metrics/tracker.py` dispatches events to trackers: OTEL counters, Central notifications, and download-job persistence.

### 3) Layer/Module Responsibilities

| Layer or module | Owns | Must not own | Evidence |
|-----------------|------|--------------|----------|
| `web` | Routing, HTTP auth, rendering templates | Scheduling and downloader subprocess control | `ddownloader/web/app.py`, `ddownloader/web/api_hooks.py`, `ddownloader/web/app_sources.py` |
| `download` | Source scheduling and download orchestration | Request validation and HTML rendering | `ddownloader/download/download_svc.py`, `ddownloader/download/schedulers/aio_gl_scheduler.py`, `ddownloader/download/downloaders/gallery_downloader.py` |
| `dao` | Data retrieval/persistence and model mapping | UI presentation logic | `ddownloader/dao/http_gallery_source_dao.py`, `ddownloader/dao/gallery_src_download_job_dao.py` |
| `metrics` | Event fan-out and observability side effects | Core source business rules | `ddownloader/metrics/tracker.py`, `ddownloader/metrics/trackers/*.py` |
| `hooks` | Event callback bridge from gallery-dl to API | DB schema ownership | `ddownloader/hooks/file_downloaded.py`, `ddownloader/hooks/file_skipped.py` |

### 4) Reused Patterns

| Pattern | Where found | Why it exists |
|---------|-------------|---------------|
| Event hub / observer | `ddownloader/metrics/tracker.py` + trackers | One download event updates multiple systems (metrics, notifications, DB). |
| DAO/repository mapping | `ddownloader/dao/*_dao.py` + `dao/tortoise/models.py` | Isolates ORM row shape from domain models (`ddownloader/models.py`). |
| Builder | `ddownloader/download/gdl.py` (`GDLCfgFileBuilder`) | Creates runtime gallery-dl config with dynamic hook commands. |
| Shared singleton-like client session | `ddownloader/metrics/central/notifications.py` | Reuses aiohttp session for central API calls. |

### 5) Known Architectural Risks

- Two backend paths coexist (Quart async/Postgres and legacy Flask/Huey/SQLite modules), increasing ambiguity about supported runtime surface.
- Hook scripts call `localhost:{APP_PORT}` and assume service availability during subprocess callbacks; failures can silently desync file/job tracking.

### 6) Evidence

- `ddownloader/main.py`
- `ddownloader/dao/database.py`
- `ddownloader/download/download_svc.py`
- `ddownloader/download/schedulers/aio_gl_scheduler.py`
- `ddownloader/download/gdl.py`
- `ddownloader/web/api_hooks.py`
- `ddownloader/metrics/tracker.py`
- `ddownloader/downloader.py`
- `ddownloader/async_tasks.py`
