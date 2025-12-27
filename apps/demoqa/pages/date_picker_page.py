"""
Date Picker page object for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class DatePickerPage(BaseDemoQAPage):
    """
    Page object representing the Date Picker widget.

    Responsibility:
    - Set date values via inputs
    - Read selected date values
    """

    URL_PATH = "date-picker"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Date Picker')"

    # ---------- Inputs ----------
    DATE_INPUT = "#datePickerMonthYearInput"
    DATE_TIME_INPUT = "#dateAndTimePickerInput"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()

    # ---------- Actions ----------

    def set_date(self, value: str) -> None:
        """
        Set date using MM/DD/YYYY format.
        """
        field = self.page.locator(self.DATE_INPUT)
        field.click()
        field.fill(value)
        field.press("Enter")

    def set_date_time(self, value: str) -> None:
        """
        Set date and time using visible input value.
        Example: 'December 25, 2025 10:30 AM'
        """
        field = self.page.locator(self.DATE_TIME_INPUT)
        field.click()
        field.fill(value)
        field.press("Enter")

    # ---------- Queries ----------

    def date_value(self) -> str:
        """
        Return selected date value.
        """
        return self.page.locator(self.DATE_INPUT).input_value()

    def date_time_value(self) -> str:
        """
        Return selected date and time value.
        """
        return self.page.locator(self.DATE_TIME_INPUT).input_value()
