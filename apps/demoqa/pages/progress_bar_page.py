"""
Progress Bar page object for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class ProgressBarPage(BaseDemoQAPage):
    """
    Page object representing the Progress Bar widget.

    Responsibility:
    - Control progress execution
    - Observe progress state
    """

    URL_PATH = "progress-bar"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Progress Bar')"

    # ---------- Controls ----------
    START_STOP_BTN = "#startStopButton"
    RESET_BTN = "#resetButton"

    # ---------- Progress ----------
    PROGRESS_BAR = "div[role='progressbar']"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.START_STOP_BTN)).to_be_visible()

    # ---------- Actions ----------

    def start(self) -> None:
        """Start the progress bar."""
        self.page.locator(self.START_STOP_BTN).click()

    def stop(self) -> None:
        """Stop the progress bar."""
        self.page.locator(self.START_STOP_BTN).click()

    def reset(self) -> None:
        """Reset progress bar."""
        self.page.locator(self.RESET_BTN).click()

    # ---------- Queries ----------

    def progress_value(self) -> int:
        """
        Return current progress value (0–100).
        """
        value = self.page.locator(self.PROGRESS_BAR).get_attribute("aria-valuenow")
        return int(value)
