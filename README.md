# python-playwright-sdet-framework

Portfolio-grade **Python + Playwright** SDET framework demonstrating scalable UI + API testing with clean architecture (Page Object Model, fixtures, reporting, CI).

---

## What’s inside

- **UI automation (Playwright)** with Page Object Model
- **API automation (Requests)** with schema validation
- **Pytest** fixtures, markers, parallel runs
- **Reporting-ready** structure (Allure folder included)
- **CI-ready** GitHub Actions workflow included

---

## Project structure

```text
python-playwright-sdet-framework/
  core/                      # framework core (browser, config, base page, logger, api client)
  apps/
    saucedemo/
      pages/                 # page objects
      tests/                 # UI tests
    demoqa/
      pages/
      tests/
  api/
    reqres/
      schemas/               # JSON schemas
      tests/                 # API tests
  utils/                     # helpers (data generators, etc.)
  reports/
    screenshots/             # failure screenshots
    videos/                  # optional recordings
    allure-results/          # allure results output
  .github/workflows/         # GitHub Actions CI
  conftest.py                # global pytest fixtures
  pytest.ini                 # pytest configuration
  requirements.txt
  .env.example
  .gitignore
  README.md
```

## 🐛 Debugging Failed Tests

### Automatic Artifacts

On test failure, the framework automatically captures:

- **Screenshot**: `reports/screenshots/<test>_<timestamp>.png`
- **Console logs**: `reports/logs/<test>_<timestamp>.txt`
- **Playwright trace** (optional): `reports/traces/<test>_<timestamp>.zip`

### Viewing Traces

```bash
# Enable tracing for debugging
pytest --trace-on-failure=true

# View trace in Playwright's inspector
playwright show-trace reports/traces/<trace-file>.zip
```

**Why traces are disabled by default:** Tracing adds ~10-15% overhead and 5-10MB per test. For portfolio demos and CI speed, screenshots + console logs are sufficient. Enable traces when debugging complex flaky tests.
