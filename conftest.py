"""Root-level pytest configuration with failure artifacts."""

import os
import re
from datetime import datetime
from pathlib import Path
import pytest

try:
    import allure
except ImportError:
    allure = None

from core.config import Config

# Use config-managed paths
REPORTS_DIR = Path(Config.REPORTS_DIR if hasattr(Config, "REPORTS_DIR") else "reports")
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
TRACES_DIR = REPORTS_DIR / "traces"
LOGS_DIR = REPORTS_DIR / "logs"


def _safe_filename(nodeid: str) -> str:
    """Convert pytest node ID to safe filename."""
    name = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    return name.strip("_")


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom CLI options."""
    parser.addoption(
        "--artifacts",
        action="store",
        default="true",
        help="Enable/disable artifacts on failure (true/false). Default: true",
    )
    parser.addoption(
        "--trace-on-failure",
        action="store",
        default="false",  # Changed to false by default
        help="Record Playwright trace on failure (true/false). Default: false",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Store test result for fixture access."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def playwright_artifacts(request):
    """
    Auto-use fixture for Playwright test artifacts.

    Activates only for tests using 'page' or 'context' fixtures.
    On failure:
        - Saves screenshot
        - Saves trace (if enabled)
        - Saves console/error logs
        - Attaches to Allure (if available)
    """
    # Skip for non-UI tests
    if "page" not in request.fixturenames and "context" not in request.fixturenames:
        yield
        return

    # Check configuration
    artifacts_enabled = request.config.getoption("--artifacts").lower() == "true"
    trace_enabled = request.config.getoption("--trace-on-failure").lower() == "true"

    if not artifacts_enabled:
        yield
        return

    # Get Playwright fixtures
    page = request.getfixturevalue("page") if "page" in request.fixturenames else None
    context = (
        request.getfixturevalue("context")
        if "context" in request.fixturenames
        else None
    )

    # Ensure directories exist
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Console capture
    console_lines = []
    if page is not None:

        def on_console(msg):
            try:
                console_lines.append(f"[{msg.type}] {msg.text}")
            except Exception:
                console_lines.append("[console] <unreadable>")

        def on_page_error(err):
            console_lines.append(f"[ERROR] {err}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)

    # Start tracing if enabled
    if context is not None and trace_enabled:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield  # Run test

    # Check if test failed
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    # Generate unique identifier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
    test_id = _safe_filename(request.node.nodeid)

    # Save console log on failure
    if failed and console_lines:
        log_path = LOGS_DIR / f"{test_id}_{timestamp}.txt"
        log_path.write_text("\n".join(console_lines), encoding="utf-8")

        if allure is not None:
            allure.attach(
                "\n".join(console_lines),
                name="browser_console",
                attachment_type=allure.attachment_type.TEXT,
            )

    # Save trace on failure
    if context is not None and trace_enabled:
        if failed:
            trace_path = TRACES_DIR / f"{test_id}_{timestamp}.zip"
            context.tracing.stop(path=str(trace_path))

            if allure is not None:
                allure.attach.file(
                    str(trace_path),
                    name="playwright_trace",
                    attachment_type=allure.attachment_type.ZIP,
                )
        else:
            context.tracing.stop()

    # Screenshot on failure
    if failed and page is not None:
        shot_path = SCREENSHOTS_DIR / f"{test_id}_{timestamp}.png"
        try:
            page.screenshot(path=str(shot_path), full_page=True)

            if allure is not None:
                allure.attach.file(
                    str(shot_path),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception as e:
            # Log but don't fail test teardown
            print(f"⚠️  Screenshot capture failed: {e}")
