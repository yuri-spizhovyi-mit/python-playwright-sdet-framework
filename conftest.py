"""
Root-level pytest configuration with failure artifacts.

This file is auto-discovered by pytest (no imports needed).
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

try:
    import allure  # optional dependency
except ImportError:
    allure = None  # type: ignore[assignment]

from playwright.sync_api import Error

from core.config import Config

# Reports path (Config override if present)
REPORTS_DIR = Path(getattr(Config, "REPORTS_DIR", "reports"))
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
TRACES_DIR = REPORTS_DIR / "traces"
LOGS_DIR = REPORTS_DIR / "logs"


def _safe_filename(nodeid: str) -> str:
    """Convert pytest node ID to a safe filename."""
    name = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    return name.strip("_")


def _now_stamp() -> str:
    """Timestamp safe for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom CLI options."""
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

def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Register custom CLI options for test execution modes.
    """
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

def pytest_configure(config: pytest.Config) -> None:
    """
    Apply marker expressions based on custom CLI execution flags.
    """
    selected = [
        config.getoption("--smoke"),
        config.getoption("--full"),
        config.getoption("--flaky"),
    ]

    if sum(bool(x) for x in selected) > 1:
        raise pytest.UsageError(
            "Only one execution mode can be selected: --smoke, --full, or --flaky"
        )

    if config.getoption("--smoke"):
        config.option.markexpr = "smoke"

    elif config.getoption("--full"):
        config.option.markexpr = "not flaky"

    elif config.getoption("--flaky"):
        config.option.markexpr = "flaky"


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Capture test outcome and write artifacts on failure.

    Important:
    - Collection errors (ERROR collecting ...) will not produce artifacts
      because the test body never ran and Playwright fixtures were not created.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    # Only act after the actual test body
    if rep.when != "call" or not rep.failed:
        return

    artifacts_enabled = item.config.getoption("--artifacts").lower() == "true"
    if not artifacts_enabled:
        return

    # Only UI tests have these fixtures
    page = item.funcargs.get("page")
    context = item.funcargs.get("context")

    test_id = _safe_filename(item.nodeid)
    stamp = _now_stamp()

    # ---- Console log (if captured) ----
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
            print(f"[DEBUG] Screenshot taken: {shot_path}")
        except Error as e:
            print(f"⚠️ Screenshot failed: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected exception type during screenshot: {e}")
        else:
            if allure is not None:
                allure.attach.file(
                    str(shot_path),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )

    # ---- Trace zip ----
    trace_enabled = item.config.getoption("--trace-on-failure").lower() == "true"
    print(
        f"[DEBUG] trace_enabled={trace_enabled}, context_present={context is not None}"
    )
    if trace_enabled and context is not None:
        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        trace_path = TRACES_DIR / f"{test_id}_{stamp}.zip"
        try:
            # Works only if tracing was started in the autouse fixture below.
            context.tracing.stop(path=str(trace_path))
            print(f"[DEBUG] tracing stopped and saved to: {trace_path}")
        except Error as e:
            print(f"⚠️ Trace save failed (trace may not have started): {e}")
        except Exception as e:
            print(f"⚠️ Unexpected exception type during trace save: {e}")
        else:
            if allure is not None:
                allure.attach.file(
                    str(trace_path),
                    name="playwright_trace.zip",
                    attachment_type=allure.attachment_type.TEXT,
                    extension="zip",
                )


@pytest.fixture(autouse=True)
def ui_runtime_capture(request: pytest.FixtureRequest):
    """
    Autouse fixture that activates only for UI tests (Playwright page/context).

    Responsibilities:
    - Capture browser console + page errors into item._console_lines
    - Start Playwright tracing at test start (if enabled)
    - Stop tracing without saving on success
      (On failure, saving happens in pytest_runtest_makereport)
    """
    is_ui_test = "page" in request.fixturenames or "context" in request.fixturenames
    if not is_ui_test:
        yield
        return

    artifacts_enabled = request.config.getoption("--artifacts").lower() == "true"
    trace_enabled = request.config.getoption("--trace-on-failure").lower() == "true"

    # Lazily resolve fixtures
    page = request.getfixturevalue("page") if "page" in request.fixturenames else None
    context = (
        request.getfixturevalue("context")
        if "context" in request.fixturenames
        else None
    )

    # Ensure dirs exist (harmless even if test passes)
    if artifacts_enabled:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # --- Console / page error capture ---
    console_lines: list[str] = []
    request.node._console_lines = console_lines  # type: ignore[attr-defined]

    if page is not None:

        def on_console(msg):
            try:
                console_lines.append(f"[console.{msg.type}] {msg.text}")
            except AttributeError as ae:
                print(f"[DEBUG] AttributeError in console handler: {ae}")
                console_lines.append("[console] <unreadable message>")
            except Exception as e:
                print(f"[DEBUG] Unexpected exception in console handler: {e}")
                console_lines.append("[console] <unreadable message>")

        def on_page_error(err):
            console_lines.append(f"[pageerror] {err}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)

    # --- Start tracing (save only on failure) ---
    tracing_started = False
    print(
        f"[DEBUG] artifacts_enabled={artifacts_enabled}, trace_enabled={trace_enabled}, context_present={context is not None}"
    )
    if artifacts_enabled and trace_enabled and context is not None:
        try:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            print(f"[DEBUG] tracing started on context: {context}")
            tracing_started = True
        except Error as e:
            print(f"⚠️ Trace start failed: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected exception type during trace start: {e}")

    yield  # run the test

    # On success, stop trace without saving (failure saving happens in makereport)
    if tracing_started and context is not None:
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and not rep.failed:
            try:
                context.tracing.stop()
                print(f"[DEBUG] tracing stopped successfully on success.")
            except Error as e:
                print(f"⚠️ Trace stop failed on success: {e}")
            except Exception as e:
                print(f"⚠️ Unexpected exception type during trace stop on success: {e}")
