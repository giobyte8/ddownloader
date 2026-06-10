# Coding Conventions

## Core Sections (Required)

### 1) Naming Rules

| Item | Rule | Example | Evidence |
|------|------|---------|----------|
| Files | Python modules use `snake_case.py` | `download_svc.py`, `http_gallery_source_dao.py` | `ddownloader/download/download_svc.py`, `ddownloader/dao/http_gallery_source_dao.py` |
| Functions/methods | Python functions/methods use `snake_case` | `find_by_download_enabled`, `human_readable_schedule` | `ddownloader/dao/http_gallery_source_dao.py`, `ddownloader/models.py` |
| Types/interfaces | Python classes use `PascalCase` | `HttpGallerySource`, `AIOGalleryDlScheduler` | `ddownloader/models.py`, `ddownloader/download/schedulers/aio_gl_scheduler.py` |
| Constants/env vars | Constants/env names are `UPPER_CASE` | `APP_PORT`, `CT_API_URL`, `CREATE_TABLE_IF_NOT_EXISTS` | `template.env`, `ddownloader/dtask_repository.py` |

### 2) Formatting and Linting

- Formatter: [TODO] No explicit formatter config found for backend (`black`, `ruff format`, `isort`, `prettier` config not present at root).
- Linter: `pylint` with repo config; UI lint via `eslint` (`preact` preset).
- Most relevant enforced rules: Python `snake_case` naming, max line length `100`, module/function/class docstring checks relaxed.
- Run commands: `pylint ...` [TODO exact canonical command not documented], `cd ui && npm run lint`.

### 3) Import and Module Conventions

- Import grouping/order: no strict import-order tool config found; modules typically place stdlib first, then third-party, then local imports.
- Alias vs relative import policy: backend strongly favors absolute package imports (`from ddownloader...`); UI uses relative imports (`../`, `./`).
- Public exports/barrel policy: minimal `__init__.py` usage, no barrel-export pattern beyond package markers.

### 4) Error and Logging Conventions

- Error strategy by layer: web/API layers raise typed exceptions for validation/transition failures; DAOs return `None` for not-found in many methods.
- Logging style and required context fields: Python `logging` with custom formatter (`asctime`, shortened logger, level, message); many logs include IDs (`job_id`, `src.id`).
- Sensitive-data redaction rules: [TODO] No centralized redaction policy found; tokens/keys are loaded from env but not explicitly scrubbed in logging helpers.

### 5) Testing Conventions

- Test file naming/location rule: backend tests under `tests/` and nested `tests/web/`, names start with `test_*.py`; UI tests use `*.test.js` under `ui/tests/`.
- Mocking strategy norm: Python uses `unittest.mock.patch` and fixtures; UI uses Enzyme shallow rendering + Jest.
- Coverage expectation: [TODO] No coverage threshold/config found.

### 6) Evidence

- `.pylintrc`
- `requirements-dev.txt`
- `ddownloader/models.py`
- `ddownloader/dao/http_gallery_source_dao.py`
- `ddownloader/__init__.py`
- `tests/test_downloader.py`
- `tests/web/test_validators.py`
- `ui/package.json`
- `ui/tests/header.test.js`
