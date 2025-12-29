# python-playwright-sdet-framework

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-python-green)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/pytest-framework-orange)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure-Live_Report-blue)](https://yuri-spizhovyi-mit.github.io/python-playwright-sdet-framework/)
![Test Suite](https://github.com/yuri-spizhovyi-mit/python-playwright-sdet-framework/actions/workflows/test-suite.yml/badge.svg)

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
│   ├── api_client.py
│   ├── base_page.py
│   ├── config.py
│   ├── logger.py
│   └── allure_helpers.py
│
├── apps/
│   ├── demoqa/
│   │   ├── pages/
│   │   └── tests/
│   │
│   └── saucedemo/
│       ├── pages/
│       └── tests/
│
├── api/
│   ├── postman_echo/
│   │   ├── client.py
│   │   ├── test_data.py
│   │   ├── schemas/
│   │   └── tests/
│   │
│   └── jsonplaceholder/
│       ├── client.py
│       ├── schemas/
│       └── tests/
│
├── utils/
│   ├── data_generator.py
│   ├── validators.py
│   └── retry.py
│
├── reports/
│   ├── screenshots/
│   └── traces/
│
├── .github/
│   └── workflows/
│       └── test-suite.yml
│
├── conftest.py
├── pytest.ini
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

## API Automation Architecture

This framework includes a dedicated API automation layer designed with
the same production-grade principles as the UI tests.

### Design Principles

- Clear separation between API client, test logic, schemas, and test data
- Deterministic and CI-safe external APIs
- No test assertions inside client code
- Contract validation using JSON Schema
- Session-scoped API clients for performance

### API Client Layer

Each external system is represented by a thin client wrapper.
For example, the Postman Echo API is implemented via `EchoClient`,
which encapsulates endpoint paths and HTTP mechanics while returning
raw responses to the tests.

### Schema Validation

JSON Schema is used as a first-class contract mechanism.
Both positive and negative schema validation tests are included to
demonstrate detection of breaking API changes.

### JSONPlaceholder

Used for REST-style resource validation.

Covers:

- Resource listing (e.g. posts)
- Schema validation
- Read-only operations (CI-safe)

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

- Scalable test architecture
- Maintainable Page Object design
- CI-ready automation with reporting
- Clear separation of concerns
- Focus on stability, not flakiness
