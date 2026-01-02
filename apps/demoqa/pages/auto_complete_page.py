"""
Auto Complete page object for DemoQA application.
"""

from playwright.sync_api import Page, expect

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class AutoCompletePage(BaseDemoQAPage):
    """
    Page object representing the Auto Complete widget.

    Responsibility:
    - Enter values into auto-complete inputs
    - Select suggestions
    - Read selected values
    """

    URL_PATH = "auto-complete"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Auto Complete')"

    # ---------- Inputs ----------
    MULTI_COLOR_INPUT = "#autoCompleteMultipleInput"
    SINGLE_COLOR_INPUT = "#autoCompleteSingleInput"

    # ---------- Suggestions ----------
    SUGGESTION_ITEMS = ".auto-complete__menu div"

    # ---------- Selected values ----------
    MULTI_SELECTED_VALUES = ".auto-complete__multi-value__label"
    SINGLE_SELECTED_VALUE = ".auto-complete__single-value"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.MULTI_COLOR_INPUT)).to_be_visible()

    # ---------- Actions ----------

    def add_multi_color(self, value: str) -> None:
        """Add a color to multi-select input."""
        self.page.locator(self.MULTI_COLOR_INPUT).fill(value)
        self.page.locator(self.SUGGESTION_ITEMS).filter(has_text=value).first.click()

    def set_single_color(self, value: str) -> None:
        """Set value in single-select input."""
        self.page.locator(self.SINGLE_COLOR_INPUT).fill(value)
        self.page.locator(self.SUGGESTION_ITEMS).filter(has_text=value).first.click()

    # ---------- Queries ----------

    def multi_selected_values(self) -> list[str]:
        """Return selected values from multi-select."""
        return self.page.locator(self.MULTI_SELECTED_VALUES).all_inner_texts()

    def single_selected_value(self) -> str:
        """Return selected value from single-select."""
        return self.page.locator(self.SINGLE_SELECTED_VALUE).inner_text()
