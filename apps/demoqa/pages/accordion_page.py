"""
Accordion page object for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class AccordionPage(BaseDemoQAPage):
    """
    Page object representing the Accordion widget.

    Responsibility:
    - Open accordion sections
    - Observe accordion content visibility
    """

    URL_PATH = "accordian"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Accordian')"

    # ---------- Section headers ----------
    SECTION_HEADERS = {
        1: "#section1Heading",
        2: "#section2Heading",
        3: "#section3Heading",
    }

    # ---------- Section content ----------
    SECTION_CONTENT = {
        1: "#section1Content",
        2: "#section2Content",
        3: "#section3Content",
    }

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.SECTION_HEADERS[1])).to_be_visible()

    # ---------- Actions ----------

    def open_section(self, section: int) -> None:
        """Open accordion section by number (1–3)."""
        self.page.locator(self.SECTION_HEADERS[section]).click()

    # ---------- Queries ----------

    def is_section_open(self, section: int) -> bool:
        """Return True if accordion section content is visible."""
        return self.page.locator(self.SECTION_CONTENT[section]).is_visible()
