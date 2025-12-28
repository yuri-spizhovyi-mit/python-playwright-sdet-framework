# python-playwright-sdet-framework

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-python-green)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/pytest-framework-orange)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure-Live_Report-blue)](https://yuri-spizhovyi-mit.github.io/python-playwright-sdet-framework/)

---

## Live Test Report

**Allure Report (GitHub Pages):**  
[View live Allure report (GitHub Pages)](https://yuri-spizhovyi-mit.github.io/python-playwright-sdet-framework/)

The report is automatically generated and published by GitHub Actions after each CI run.  
It allows reviewers to inspect test results, execution history, and failures without running the project locally.

---

## Project Purpose

This repository demonstrates a **portfolio-grade SDET automation framework** built with Python and Playwright.

The goal of the project is to showcase:

- Clean and scalable test architecture
- Production-style UI automation practices
- CI/CD-ready reporting and artifacts
- Maintainability, observability, and debuggability of tests

This is not a demo or tutorial repository.  
The structure and decisions reflect how automation frameworks are typically designed and maintained in large engineering organizations.

---

## Technology Stack

- **Language:** Python 3.12
- **UI Automation:** Playwright (Python)
- **Test Runner:** Pytest
- **Reporting:** Allure
- **CI/CD:** GitHub Actions
- **Design Patterns:** Page Object Model (POM), Fixture-based setup
- **Target Applications:**
  - DemoQA (UI components & interactions)
  - SauceDemo (sample e-commerce UI)

---

## High-Level Architecture

Key architectural principles:

- Clear separation between **test logic** and **page behavior**
- Centralized **browser lifecycle management**
- Reusable **pytest fixtures** for environment setup
- Explicit waits and state-based assertions (no hard sleeps)
- CI-first mindset (headless by default, artifacts on failure)

---

## Project Structure

```text
python-playwright-sdet-framework/
│
├── core/
│   ├── browser.py              # Browser & context management
│   ├── config.py               # Runtime configuration
│   ├── base_page.py            # Base page abstraction
│   ├── api_client.py           # API client foundation
│   └── logger.py               # Logging utilities
│
├── apps/
│   ├── demoqa/
│   │   ├── pages/              # Page Objects
│   │   └── tests/              # UI tests
│   │
│   └── saucedemo/
│       ├── pages/
│       └── tests/
│
├── api/
│   └── reqres/
│       ├── schemas/            # JSON schemas
│       └── tests/              # API tests
│
├── utils/
│   ├── data_generators.py
│   └── helpers.py
│
├── reports/
│   ├── screenshots/            # Failure screenshots
│   ├── traces/                 # Playwright traces (optional)
│   └── allure-results/         # Raw Allure results
│
├── .github/
│   └── workflows/
│       └── test_suite.yml      # CI pipeline
│
├── conftest.py                 # Global pytest fixtures
├── pytest.ini                  # Pytest configuration
├── requirements.txt
├── .env.example
└── README.md
```

---

## Test Coverage Overview

### UI Tests (DemoQA)

- Elements
  - Text Box
  - Check Box
  - Radio Button
- Widgets
  - Date Picker
  - Slider
  - Tabs
  - Progress Bar
- Interactions
  - Drag & Drop
  - Droppable
  - Sortable
  - Selectable
  - Resizable

### UI Tests (SauceDemo)

- Login flow
- Inventory page smoke validation

---

## Pytest Configuration

Markers used in the project:

- `@pytest.mark.smoke` – fast, critical-path tests (CI default)
- `@pytest.mark.full` – extended UI coverage

Example:

```bash
pytest -m smoke
pytest -m full
```

---

## Fixtures Strategy

Fixtures are centralized in `conftest.py` and include:

- Browser and context lifecycle
- Page initialization
- Base URL validation
- Faker session data
- Headless / headed control via environment variables

This ensures:

- No duplicated setup code
- Predictable test execution
- Easy extension for parallelization or multiple environments

---

## Debugging & Failure Analysis

### Automatic Artifacts

On test failure, the framework captures:

- Screenshot of the failure state
- Console logs
- Allure step-level information

Artifacts are uploaded to GitHub Actions and attached to the Allure report.

### Playwright Traces (Optional)

Tracing can be enabled when deeper debugging is required.

```bash
pytest --trace-on-failure=true
playwright show-trace reports/traces/<trace>.zip
```

Tracing is disabled by default to keep CI fast and storage usage minimal.

---

## Continuous Integration

### GitHub Actions

The CI pipeline:

- Runs on every push and pull request
- Executes smoke tests in headless Chromium
- Generates Allure results
- Publishes Allure report to GitHub Pages
- Uploads artifacts on failure

### Optional Nightly Run

The workflow can be extended with a scheduled trigger:

```yaml
schedule:
  - cron: "0 2 * * *"
```

This enables unattended nightly validation.

---

## Allure Reporting

Allure provides:

- Suite-level and test-level visibility
- Execution history
- Duration analytics
- Attachments and logs
- Environment metadata

The live report is publicly accessible and requires no local setup.

---

## Environment Configuration

Runtime configuration is controlled via environment variables:

- `HEADLESS=true|false`
- `BROWSER=chromium|firefox|webkit`
- `BASE_URL=<target url>`

An example file is provided: `.env.example`

---

## How to Run Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

playwright install chromium
pytest -m smoke --headed
```

---

## What This Project Demonstrates

- Senior-level test architecture decisions
- Maintainable Page Object design
- CI-ready automation with reporting
- Clear separation of concerns
- Focus on stability, not flakiness
