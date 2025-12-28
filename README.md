# python-playwright-sdet-framework

[![CI](https://github.com/yuri-spizhovyi-mit/python-playwright-sdet-framework/actions/workflows/test_suite.yml/badge.svg)](https://github.com/yuri-spizhovyi-mit/python-playwright-sdet-framework/actions)
[![Allure Report](https://img.shields.io/badge/Allure-Live_Report-blue)](https://yuri-spizhovyi-mit.github.io/python-playwright-sdet-framework/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Python-green)](https://playwright.dev/python/)

Portfolio-grade **Python + Playwright** SDET framework demonstrating scalable UI and API testing with clean architecture, deterministic execution, and production-style CI reporting.

This repository is designed to reflect **real-world SDET practices** rather than toy examples.

---

## Key characteristics

- Deterministic UI automation using **Playwright (sync API)**
- Page Object Model with clear responsibility boundaries
- Centralized **pytest fixtures** and reusable test data
- Stable execution in both **headed and headless CI**
- **Allure reporting**, published automatically via GitHub Pages
- CI-first design with reproducible and observable test runs

---

## Live test report (CI)

The latest CI execution report is publicly available:

https://yuri-spizhovyi-mit.github.io/python-playwright-sdet-framework/

The report is generated automatically by GitHub Actions and includes:

- test results and durations
- suite and feature breakdowns
- browser and execution metadata
- historical execution data (when applicable)

No local setup is required to view results.

---

## Project structure

```text
python-playwright-sdet-framework/
  core/                      # framework core (base page, config, api client)
  apps/
    saucedemo/
      pages/                 # page objects
      tests/                 # UI tests
    demoqa/
      pages/
      tests/
  api/
    reqres/
      schemas/               # JSON schemas for contract validation
      tests/                 # API tests
  reports/
    screenshots/             # failure screenshots
    traces/                  # optional Playwright traces
    allure-results/          # raw Allure results
  .github/workflows/         # GitHub Actions CI
  conftest.py                # global pytest fixtures
  pytest.ini                 # pytest configuration
  requirements.txt
  .env.example
  README.md
```

---

## Test execution

### Local run (headed)

```bash
pytest -m smoke -v
```

### Local run (headless)

```bash
HEADLESS=true pytest -m smoke -v
```

### CI run

Tests are executed automatically by GitHub Actions:

- on every push to `main`
- on pull requests
- on a scheduled nightly run

---

## CI scheduling (nightly execution)

In addition to push and pull request triggers, the framework is configured to run **automatically every night** via GitHub Actions.

This ensures:

- early detection of flaky behavior
- continuous validation against third-party demo applications
- historical stability tracking in Allure

Example schedule configuration:

```yaml
schedule:
  - cron: "0 2 * * *" # nightly run at 02:00 UTC
```

---

## Debugging failed tests

### Automatic artifacts

On test failure, the framework automatically captures:

- Screenshot (visual state at failure moment)
- Allure attachments (failure context in the report)
- Optional Playwright trace (disabled by default)

These artifacts are available:

- in GitHub Actions run artifacts
- inside the Allure report for failed tests

---

## Playwright traces (optional)

Tracing is disabled by default to keep CI fast and lightweight.

When enabled, traces provide:

- DOM snapshots
- network activity
- step-by-step replay in Playwright Inspector

Example usage:

```bash
playwright show-trace reports/traces/<trace-file>.zip
```
