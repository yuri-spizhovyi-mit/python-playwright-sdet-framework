"""Configuration management for test automation framework.

Loads settings from environment variables with sensible defaults.
Supports local development (.env) and CI/CD environments.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration options loaded from environment variables."""

    # ============================================================================
    # Browser Configuration
    # ============================================================================
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit

    # Browser behavior
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Milliseconds to slow down operations

    # ============================================================================
    # Timeouts (milliseconds)
    # ============================================================================
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))  # 10 seconds
    LONG_TIMEOUT = int(os.getenv("LONG_TIMEOUT", "30000"))  # 30 seconds
    SHORT_TIMEOUT = int(os.getenv("SHORT_TIMEOUT", "5000"))  # 5 seconds

    # ============================================================================
    # Application URLs
    # ============================================================================
    # UI Systems Under Test
    SAUCE_URL = os.getenv("SAUCE_URL", "https://www.saucedemo.com")
    DEMOQA_URL = os.getenv("DEMOQA_URL", "https://demoqa.com")

    # API Systems Under Test
    REQRES_URL = os.getenv("REQRES_URL", "https://reqres.in/api")

    # ============================================================================
    # Test Credentials
    # ============================================================================
    # SauceDemo users
    SAUCE_USERNAME = os.getenv("SAUCE_USERNAME", "standard_user")
    SAUCE_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
    SAUCE_LOCKED_USER = os.getenv("SAUCE_LOCKED_USER", "locked_out_user")
    SAUCE_PROBLEM_USER = os.getenv("SAUCE_PROBLEM_USER", "problem_user")

    # ReqRes API (public test API uses fixed credentials)
    REQRES_EMAIL = os.getenv("REQRES_EMAIL", "eve.holt@reqres.in")
    REQRES_PASSWORD = os.getenv("REQRES_PASSWORD", "cityslicka")

    # ============================================================================
    # Test Artifacts & Reporting
    # ============================================================================
    # Base directory for all test outputs
    REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "reports"))

    # Artifact subdirectories (auto-created by conftest.py)
    SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
    TRACES_DIR = REPORTS_DIR / "traces"
    LOGS_DIR = REPORTS_DIR / "logs"
    VIDEOS_DIR = REPORTS_DIR / "videos"

    # Artifact behavior
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    TRACE_ON_FAILURE = os.getenv("TRACE_ON_FAILURE", "false").lower() == "true"
    VIDEO_ON_FAILURE = os.getenv("VIDEO_ON_FAILURE", "false").lower() == "true"

    # Screenshot settings
    SCREENSHOT_FULL_PAGE = True  # Capture entire page vs viewport only

    # ============================================================================
    # Test Execution Settings
    # ============================================================================
    # Parallel execution
    WORKERS = int(os.getenv("PYTEST_WORKERS", "1"))  # For pytest-xdist

    # Retry behavior (for flaky tests)
    FLAKY_TEST_RETRIES = int(os.getenv("FLAKY_TEST_RETRIES", "2"))
    FLAKY_TEST_DELAY = int(os.getenv("FLAKY_TEST_DELAY", "1"))  # seconds

    # ============================================================================
    # Environment Detection
    # ============================================================================
    CI = os.getenv("CI", "false").lower() == "true"  # Detect CI environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")  # local, ci, staging, etc.

    # ============================================================================
    # Logging
    # ============================================================================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE = REPORTS_DIR / "test_execution.log"

    # ============================================================================
    # Browser Context Settings (Playwright)
    # ============================================================================
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

    # Locale and timezone
    LOCALE = os.getenv("LOCALE", "en-US")
    TIMEZONE = os.getenv("TIMEZONE", "America/Vancouver")  # BC default

    # Device emulation (optional, set to enable mobile testing)
    DEVICE_NAME = os.getenv("DEVICE_NAME", None)  # e.g., "iPhone 12"

    # ============================================================================
    # API Testing Settings
    # ============================================================================
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # seconds
    API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", "3"))
    API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", "1"))  # seconds

    # ============================================================================
    # Feature Flags
    # ============================================================================
    # Enable/disable framework features for debugging
    ENABLE_SCREENSHOTS = os.getenv("ENABLE_SCREENSHOTS", "true").lower() == "true"
    ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    ENABLE_VIDEO = os.getenv("ENABLE_VIDEO", "false").lower() == "true"
    ENABLE_CONSOLE_CAPTURE = (
        os.getenv("ENABLE_CONSOLE_CAPTURE", "true").lower() == "true"
    )

    @classmethod
    def is_ci(cls) -> bool:
        """Check if running in CI environment."""
        return cls.CI

    @classmethod
    def get_browser_context_options(cls) -> dict:
        """
        Get Playwright browser context options.

        Returns:
            dict: Configuration for browser_context creation
        """
        return {
            "viewport": {
                "width": cls.VIEWPORT_WIDTH,
                "height": cls.VIEWPORT_HEIGHT,
            },
            "locale": cls.LOCALE,
            "timezone_id": cls.TIMEZONE,
            "ignore_https_errors": True,  # For demo sites with cert issues
        }

    @classmethod
    def get_launch_options(cls) -> dict:
        """
        Get Playwright browser launch options.

        Returns:
            dict: Configuration for browser.launch()
        """
        return {
            "headless": cls.HEADLESS,
            "slow_mo": cls.SLOW_MO,
        }

    @classmethod
    def ensure_directories(cls) -> None:
        """Create all required artifact directories if they don't exist."""
        for directory in [
            cls.REPORTS_DIR,
            cls.SCREENSHOTS_DIR,
            cls.TRACES_DIR,
            cls.LOGS_DIR,
            cls.VIDEOS_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_env_info(cls) -> dict:
        """
        Get current environment configuration summary.

        Useful for test reports and debugging.

        Returns:
            dict: Key configuration values
        """
        return {
            "environment": cls.ENVIRONMENT,
            "browser": cls.BROWSER,
            "headless": cls.HEADLESS,
            "ci": cls.is_ci(),
            "viewport": f"{cls.VIEWPORT_WIDTH}x{cls.VIEWPORT_HEIGHT}",
            "timeout": cls.DEFAULT_TIMEOUT,
            "artifacts_enabled": cls.SCREENSHOT_ON_FAILURE,
        }


# Auto-create directories on import (safe, idempotent)
Config.ensure_directories()
