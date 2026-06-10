# Technology Stack

## Core Sections (Required)

### 1) Runtime Summary

| Area | Value | Evidence |
|------|-------|----------|
| Primary language | Python | `requirements.txt`, `ddownloader/main.py` |
| Runtime + version | Python 3.12 (dev + container) | `mise.toml`, `docker/ddownloader.dockerfile` |
| Package manager | `pip` | `docs/development.md`, `requirements.txt`, `requirements-dev.txt` |
| Module/build system | Direct module execution (`python ddownloader/main.py`), no packaging metadata found | `docs/development.md`, `ddownloader/main.py`, `[TODO] pyproject/setup.cfg not found` |

### 2) Production Frameworks and Dependencies

| Dependency | Version | Role in system | Evidence |
|------------|---------|----------------|----------|
| Quart | `0.20.0` | Async web app runtime | `requirements.txt`, `ddownloader/web/app.py` |
| Hypercorn | `0.17.3` | ASGI serving in prod mode | `requirements.txt`, `ddownloader/main.py` |
| Flask | `3.1.0` | Legacy request/validation modules still present | `requirements.txt`, `ddownloader/web/api.py` |
| tortoise-orm | `0.25.0` | Async ORM for Postgres data access | `requirements.txt`, `ddownloader/dao/database.py`, `ddownloader/dao/tortoise/models.py` |
| psycopg | `3.2.6` | Postgres driver | `requirements.txt`, `ddownloader/dao/database.py` |
| APScheduler + SQLAlchemy | `3.11.0` + `2.0.41` | Scheduled download jobs with DB-backed job store | `requirements.txt`, `ddownloader/download/schedulers/aio_gl_scheduler.py` |
| gallery_dl | `1.29.5` | External downloader subprocess | `requirements.txt`, `ddownloader/download/gdl.py` |
| aiohttp | `3.11.18` | Async HTTP for hooks/notifications | `requirements.txt`, `ddownloader/metrics/central/notifications.py`, `ddownloader/hooks/file_downloaded.py` |
| opentelemetry-* | mixed (`1.32.1`, `0.53b1`) | Tracing/metrics instrumentation | `requirements.txt`, `otelw.sh`, `ddownloader/metrics/trackers/otel_tracker.py` |
| pydantic | `2.11.3` | Domain model validation/types | `requirements.txt`, `ddownloader/models.py` |
| preact | `^10.3.2` | Web UI framework (`ui/`) | `ui/package.json` |

### 3) Development Toolchain

| Tool | Purpose | Evidence |
|------|---------|----------|
| pylint | Linting (Python) | `.pylintrc`, `requirements-dev.txt` |
| pytest | Testing (Python) | `requirements-dev.txt`, `pytest.ini`, `tests/` |
| pytest-dotenv | Test env loading | `requirements-dev.txt`, `pytest.ini` |
| eslint | Linting (UI JS) | `ui/package.json` |
| jest + enzyme | UI unit tests | `ui/package.json`, `ui/tests/header.test.js` |
| preact-cli | UI dev/build | `ui/package.json` |

### 4) Key Commands

```bash
pip install -r requirements.txt && pip install -r requirements-dev.txt
python ddownloader/main.py
pytest
cd ui && npm install && npm run build && npm run test && npm run lint
```

### 5) Environment and Config

- Config sources: `.env` (loaded via `python-dotenv`), `template.env`, `config/gdl-base.json`, `config/runtime/*.json`.
- Required env vars (from template): `APP_ENV`, `APP_PORT`, `APP_BASE_URL`, `GALLERIES_PATH`, `CONFIG_PATH`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `API_KEY_HOOKS`, `CT_MONITORING_ENABLED`, `CT_API_URL`, `CT_API_KEY`, `OTEL_*`.
- Deployment/runtime constraints: service assumes Postgres connectivity and invokes `gallery-dl` binary at runtime.

### 6) Evidence

- `requirements.txt`
- `requirements-dev.txt`
- `mise.toml`
- `docker/ddownloader.dockerfile`
- `ddownloader/main.py`
- `docs/development.md`
- `template.env`
- `ui/package.json`
