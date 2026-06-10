# Codebase Structure

## Core Sections (Required)

### 1) Top-Level Map

| Path | Purpose | Evidence |
|------|---------|----------|
| `ddownloader/` | Main Python application package (web app, downloader, DAO, metrics, hooks) | `ddownloader/main.py`, `ddownloader/web/app.py` |
| `tests/` | Python tests (legacy downloader/repository/validators) | `tests/test_downloader.py`, `tests/test_dtask_repository.py` |
| `db/` | SQL migration/seed scripts and DB reset helper | `db/up/1.schema.sql`, `db/up/2.jobs_monitoring.sql`, `db/reset.sh` |
| `config/` | gallery-dl base config and runtime-generated configs/logs | `config/gdl-base.template.json`, `ddownloader/download/gdl.py` |
| `docker/` | Docker image build/release scripts | `docker/ddownloader.dockerfile`, `docker/release.sh` |
| `ui/` | Separate Preact frontend app | `ui/package.json`, `ui/src/components/app.js` |
| `scripts/` | Utility scripts (API key generation) | `scripts/gen_api_key.py` |
| `docs/` | Project documentation | `docs/development.md` |
| `data/` | Downloaded/local media content used by the app | `template.env` (`GALLERIES_PATH`), `ddownloader/download/gdl.py` |

### 2) Entry Points

- Main runtime entry: `ddownloader/main.py`
- Secondary entry points (worker/cli/jobs): `otelw.sh`, `ddownloader/hooks/file_downloaded.py`, `ddownloader/hooks/file_skipped.py`, `docker/ddownloader.dockerfile` (ENTRYPOINT wrapper)
- How entry is selected (script/config): direct Python run (`python ddownloader/main.py`) or wrapper (`./otelw.sh`) based on `OTEL_ENABLED`.

### 3) Module Boundaries

| Boundary | What belongs here | What must not be here |
|----------|-------------------|------------------------|
| `ddownloader/web/` | Quart routes, blueprints, request auth/validation, Jinja templates | Download scheduling and DB model definitions |
| `ddownloader/download/` | Scheduling, downloader orchestration, gallery-dl subprocess integration | HTTP route handling |
| `ddownloader/dao/` | Persistence access/mapping between ORM rows and domain models | Route rendering/business orchestration |
| `ddownloader/metrics/` | Event hub + trackers for OTEL/Central/job metrics | Direct HTTP route logic |
| `ddownloader/hooks/` | External hook entry scripts posting back into API | Core DB logic |
| `ddownloader/downloader.py` + `ddownloader/dtask_repository.py` | Legacy sync downloader/task storage path | [ASK USER] Whether this legacy path should remain active |

### 4) Naming and Organization Rules

- File naming pattern: Python uses `snake_case.py` (`download_svc.py`, `http_gallery_source_dao.py`); UI files mostly lower/snake style (`validator.service.js`, `header.test.js`).
- Directory organization pattern: Backend is layer/domain-oriented (`web`, `download`, `dao`, `metrics`, `services`), UI is feature/components (`routes`, `components`, `services`).
- Import aliasing or path conventions: backend uses absolute package imports (`from ddownloader...`), UI uses relative imports.

### 5) Evidence

- `ddownloader/main.py`
- `ddownloader/web/app.py`
- `ddownloader/download/download_svc.py`
- `ddownloader/dao/database.py`
- `ddownloader/metrics/tracker.py`
- `ddownloader/hooks/file_downloaded.py`
- `ui/src/components/app.js`
- `db/up/1.schema.sql`
