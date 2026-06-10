# Testing Patterns

## Core Sections (Required)

### 1) Test Stack and Commands

- Primary test framework: `pytest==6.2.5` (backend), `jest` (UI).
- Assertion/mocking tools: `pytest` assertions, `unittest.mock.patch`, Jest `expect`, Enzyme shallow renderer.
- Commands:

```bash
pytest
pytest tests/test_downloader.py
cd ui && npm run test
[TODO] coverage command not defined in repo configs
```

### 2) Test Layout

- Test file placement pattern: backend tests in `tests/` (plus `tests/web/`), UI tests in `ui/tests/`.
- Naming convention: backend `test_*.py`; UI `*.test.js`.
- Setup files and where they run: backend `ddownloader/conftest.py` + `pytest.ini` (`.env.test`); UI Jest setup files in `ui/tests/__mocks__/`.

### 3) Test Scope Matrix

| Scope | Covered? | Typical target | Notes |
|-------|----------|----------------|-------|
| Unit | yes | URL metadata logic, validators, SQLite task repository | `tests/test_downloader.py`, `tests/web/test_validators.py`, `tests/test_dtask_repository.py` |
| Integration | [TODO] | [TODO] | No explicit integration suite/config found |
| E2E | [TODO] | [TODO] | No end-to-end runner/config found |

### 4) Mocking and Isolation Strategy

- Main mocking approach: patch HTTP calls (`requests.head`) and isolate fields/inputs with mock objects.
- Isolation guarantees: backend uses fixture cleanup for test DB file and `.env.test`; UI tests use browser/setup mocks.
- Common failure mode in tests: backend tests mainly target legacy sync modules, leaving async Quart/download scheduler paths largely uncovered.

### 5) Coverage and Quality Signals

- Coverage tool + threshold: [TODO] not configured.
- Current reported coverage: [TODO] not found in repository files.
- Known gaps/flaky areas: no tests found for `ddownloader/download/*`, `ddownloader/metrics/*`, or async Quart blueprints under `web/app_sources.py` and `web/api_hooks.py`.

### 6) Evidence

- `requirements-dev.txt`
- `pytest.ini`
- `ddownloader/conftest.py`
- `tests/test_downloader.py`
- `tests/test_dtask_repository.py`
- `tests/web/test_validators.py`
- `ui/package.json`
- `ui/tests/header.test.js`
- `ui/tests/__mocks__/setupTests.js`
