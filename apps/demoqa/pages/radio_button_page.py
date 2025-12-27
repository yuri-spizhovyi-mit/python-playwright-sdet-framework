"""
Radio Button page object for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class RadioButtonPage(BaseDemoQAPage):
    """
    Page object representing the Radio Button page.

    Responsibility:
    - Select radio button options
    - Read selected value from result output
    """

    URL_PATH = "radio-button"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Radio Button')"

    # ---------- Radio controls ----------
    RADIO_LABEL = "label"
    RADIO_INPUT = "input[type='radio']"

    # ---------- Radio labels ----------
    YES_LABEL = "label[for='yesRadio']"
    IMPRESSIVE_LABEL = "label[for='impressiveRadio']"
    NO_LABEL = "label[for='noRadio']"

    # ---------- Output ----------
    RESULT_TEXT = ".text-success"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()

    # ---------- Actions ----------

    def select_yes(self) -> None:
        """
        Select the 'Yes' radio button option.
        """
        self.page.locator(self.YES_LABEL).check()

    def select_impressive(self) -> None:
        """
        Select the 'Impressive' radio button option.
        """
        self.page.locator(self.IMPRESSIVE_LABEL).check()

    def select_no(self) -> None:
        """
        Attempting to select 'No' should have no effect
        (it is disabled on DemoQA).
        """
        return

    # ---------- Queries ----------

    def selected_value(self) -> str | None:
        """
        Return selected radio button value from result panel.
        """
        result = self.page.locator(self.RESULT_TEXT)
        return result.inner_text() if result.is_visible() else None
