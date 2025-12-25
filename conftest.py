"""
Root-level pytest configuration with failure artifacts.

This file is auto-discovered by pytest.
It applies to all tests in the repo, but only activates for UI tests that
use Playwright fixtures ('page' and/or 'context').

On UI test failure (rep.when == "call"):
- saves screenshot to: reports/screenshots/
- saves Playwright trace zip to: reports/traces/ (if enabled)
- saves browser console log to: reports/logs/
- attaches artifacts to Allure (if allure-pytest is installed)
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
import pytest
from apps.saucedemo.pages.login_page import LoginPage
from apps.saucedemo.pages.inventory_page import InventoryPage

try:
    import allure  # optional dependency
except ImportError:
    allure = None  # type: ignore[assignment]

from playwright.sync_api import Error
from core.config import Config

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------

REPORTS_DIR = Path(Config.REPORTS_DIR)
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
TRACES_DIR = REPORTS_DIR / "traces"
LOGS_DIR = REPORTS_DIR / "logs"


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------


def _safe_filename(nodeid: str) -> str:
    """Convert pytest node ID to a filesystem-safe filename."""
    name = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    return name.strip("_")


def _now_stamp() -> str:
    """Timestamp safe for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]


# ------------------------------------------------------------------------------
# CLI options
# ------------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Register custom CLI options.
    """

    # Artifact / tracing flags
    parser.addoption(
        "--artifacts",
        action="store",
        default="true",
        help="Enable/disable failure artifacts (true/false). Default: true",
    )
    parser.addoption(
        "--trace-on-failure",
        action="store",
        default="true",
        help="Save Playwright trace zip on failure (true/false). Default: true",
    )

    # Execution modes
    group = parser.getgroup("execution modes")

    group.addoption(
        "--smoke",
        action="store_true",
        help="Run smoke tests only",
    )
    group.addoption(
        "--full",
        action="store_true",
        help="Run full regression suite (exclude flaky tests)",
    )
    group.addoption(
        "--flaky",
        action="store_true",
        help="Run flaky tests only",
    )


# ------------------------------------------------------------------------------
# Execution mode handling
# ------------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """
    Apply marker expressions based on custom CLI execution flags.
    """

    selected = [
        config.getoption("smoke"),
        config.getoption("full"),
        config.getoption("flaky"),
    ]

    if sum(bool(x) for x in selected) > 1:
        raise pytest.UsageError(
            "Only one execution mode can be selected: --smoke, --full, or --flaky"
        )

    if config.getoption("smoke"):
        config.option.markexpr = "smoke"

    elif config.getoption("full"):
        config.option.markexpr = "not flaky"

    elif config.getoption("flaky"):
        config.option.markexpr = "flaky"


# ------------------------------------------------------------------------------
# Failure artifact handling
# ------------------------------------------------------------------------------


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Capture test outcome and write artifacts on failure.

    Collection/setup errors do not produce artifacts because Playwright
    fixtures are not created.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when != "call" or not rep.failed:
        return

    artifacts_enabled = item.config.getoption("artifacts").lower() == "true"
    if not artifacts_enabled:
        return

    page = item.funcargs.get("page")
    context = item.funcargs.get("context")

    test_id = _safe_filename(item.nodeid)
    stamp = _now_stamp()

    # ---- Console log ----
    console_lines = getattr(item, "_console_lines", None)
    if console_lines:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_path = LOGS_DIR / f"{test_id}_{stamp}.txt"
        log_path.write_text("\n".join(console_lines), encoding="utf-8")

        if allure is not None:
            allure.attach(
                "\n".join(console_lines),
                name="browser_console_log",
                attachment_type=allure.attachment_type.TEXT,
            )

    # ---- Screenshot ----
    if page is not None:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        shot_path = SCREENSHOTS_DIR / f"{test_id}_{stamp}.png"
        try:
            page.screenshot(path=str(shot_path), full_page=True)
        except Error:
            pass
        else:
            if allure is not None:
                allure.attach.file(
                    str(shot_path),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )

    # ---- Trace ----
    trace_enabled = item.config.getoption("trace_on_failure").lower() == "true"
    if trace_enabled and context is not None:
        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        trace_path = TRACES_DIR / f"{test_id}_{stamp}.zip"
        try:
            context.tracing.stop(path=str(trace_path))
        except Error:
            pass
        else:
            if allure is not None:
                allure.attach.file(
                    str(trace_path),
                    name="playwright_trace.zip",
                    attachment_type=allure.attachment_type.TEXT,
                    extension="zip",
                )


# ------------------------------------------------------------------------------
# UI runtime capture (console + tracing)
# ------------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def ui_runtime_capture(request: pytest.FixtureRequest):
    """
    Autouse fixture activated only for UI tests (Playwright page/context).

    Responsibilities:
    - Capture browser console + page errors
    - Start tracing at test start (if enabled)
    - Stop tracing on success (failure saving handled elsewhere)
    """

    is_ui_test = "page" in request.fixturenames or "context" in request.fixturenames
    if not is_ui_test:
        yield
        return

    artifacts_enabled = request.config.getoption("artifacts").lower() == "true"
    trace_enabled = request.config.getoption("trace_on_failure").lower() == "true"

    page = request.getfixturevalue("page") if "page" in request.fixturenames else None
    context = (
        request.getfixturevalue("context")
        if "context" in request.fixturenames
        else None
    )

    if artifacts_enabled:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Console capture ----
    console_lines: list[str] = []
    request.node._console_lines = console_lines  # type: ignore[attr-defined]

    if page is not None:

        def on_console(msg):
            console_lines.append(f"[console.{msg.type}] {msg.text}")

        def on_page_error(err):
            console_lines.append(f"[pageerror] {err}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)

    # ---- Tracing ----
    tracing_started = False
    if artifacts_enabled and trace_enabled and context is not None:
        try:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            tracing_started = True
        except Error:
            pass

    yield

    # Stop trace on success (do not save)
    if tracing_started and context is not None:
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and not rep.failed:
            try:
                context.tracing.stop()
            except Error:
                pass


@pytest.fixture
def authenticated_page(page):
    """
    Returns a Playwright page with an authenticated SauceDemo session.

    Fails fast if login does not succeed.
    """
    login_page = LoginPage(page)
    login_page.open()

    login_page.login(
        username=Config.SAUCE_STANDARD_USER,
        password=Config.SAUCE_PASSWORD,
    )

    inventory_page = InventoryPage(page)

    # Fail fast if login did not succeed
    assert inventory_page.is_loaded(), "Login failed: inventory page not loaded"

    return page
