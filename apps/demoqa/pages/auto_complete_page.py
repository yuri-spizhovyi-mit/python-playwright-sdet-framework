"""
Auto Complete page object for DemoQA application.
"""

from playwright.sync_api import Page, expect

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class AutoCompletePage(BaseDemoQAPage):
    """
    Page object representing the Auto Complete widget.

    Responsibilities:
    - Type into auto-complete inputs
    - Select suggestions (mouse / keyboard)
    - Manage single & multi-value states
    - Query UI state safely (React Select aware)
    """

    URL_PATH = "auto-complete"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Auto Complete')"

    # ---------- Inputs ----------
    MULTI_COLOR_INPUT = "#autoCompleteMultipleInput"
    SINGLE_COLOR_INPUT = "#autoCompleteSingleInput"

    # ---------- Suggestions ----------
    SUGGESTION_ITEMS = ".auto-complete__option"

    # ---------- Selected values ----------
    MULTI_SELECTED_VALUES = ".auto-complete__multi-value__label"
    SINGLE_SELECTED_VALUE = ".auto-complete__single-value"

    # ---------- Remove buttons ----------
    MULTI_REMOVE_BUTTON = ".auto-complete__multi-value__remove"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.SINGLE_COLOR_INPUT)).to_be_visible()

    # ======================================================================
    # Single-value input actions
    # ======================================================================

    def type_single(self, value: str) -> None:
        """Type text into single-value input."""
        self.page.locator(self.SINGLE_COLOR_INPUT).fill(value)

    def select_first_suggestion(self) -> None:
        """Select first visible suggestion using mouse."""
        self.page.locator(self.SUGGESTION_ITEMS).first.click()

    def confirm_with_enter(self) -> None:
        """Confirm selection using Enter key."""
        self.page.locator(self.SINGLE_COLOR_INPUT).press("Enter")

    def clear_single_input(self) -> None:
        """Clear single-value input via keyboard (React Select safe)."""
        input_box = self.page.locator(self.SINGLE_COLOR_INPUT)
        input_box.click()
        input_box.press("Control+A")
        input_box.press("Backspace")

    # ======================================================================
    # Multi-value input actions
    # ======================================================================

    def add_multiple(self, values: list[str]) -> None:
        """
        Add multiple values to multi-select input.
        Duplicate-safe and React Select aware.
        """
        for value in values:
            self.page.locator(self.MULTI_COLOR_INPUT).fill(value)

            suggestions = self.page.locator(self.SUGGESTION_ITEMS).filter(
                has_text=value
            )

            # React Select hides already-selected options
            if suggestions.count() > 0:
                suggestions.first.click()

    def remove_value(self, value: str) -> None:
        """Remove selected value from multi-input."""
        labels = self.page.locator(self.MULTI_SELECTED_VALUES)

        for i in range(labels.count()):
            if labels.nth(i).inner_text() == value:
                self.page.locator(self.MULTI_REMOVE_BUTTON).nth(i).click()
                return

    # ======================================================================
    # Queries
    # ======================================================================

    def has_suggestions(self) -> bool:
        """Return True if suggestion list contains items."""
        return self.page.locator(self.SUGGESTION_ITEMS).count() > 0

    def single_value(self) -> str:
        """
        Return selected single value.
        Empty string if value is not present (React Select behavior).
        """
        locator = self.page.locator(self.SINGLE_SELECTED_VALUE)
        return locator.inner_text() if locator.count() > 0 else ""

    def multi_values(self) -> list[str]:
        """Return selected multi-values."""
        return self.page.locator(self.MULTI_SELECTED_VALUES).all_inner_texts()

    def select_suggestion(self, value: str) -> None:
        """Select a specific suggestion by visible text."""
        self.page.locator(self.SUGGESTION_ITEMS).filter(
            has_text=value
        ).first.click()
