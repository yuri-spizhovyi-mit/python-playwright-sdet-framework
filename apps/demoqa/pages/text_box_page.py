"""Text Box page object for DemoQA."""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class TextBoxPage(BaseDemoQAPage):
    """
    Page object representing the Text Box form.

    Responsibility:
    - Interact with the Text Box form
    - Read submitted output
    """

    URL_PATH = "text-box"

    # --- Page readiness anchor ---
    PAGE_HEADER = "h1:text('Text Box')"

    # --- Form inputs ---
    FULL_NAME_INPUT = "#userName"
    EMAIL_INPUT = "#userEmail"
    CURRENT_ADDRESS_INPUT = "#currentAddress"
    PERMANENT_ADDRESS_INPUT = "#permanentAddress"
    SUBMIT_BUTTON = "#submit"

    # --- Output ---
    OUTPUT_CONTAINER = "#output"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        """
        Assert that the Text Box page is loaded and ready.

        This is NOT a test assertion.
        This is a safety check to prevent mis-navigation usage.
        """
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()

    # ---------- Actions ----------

    def fill_full_name(self, value: str) -> None:
        """
        Fill the Full Name input field with the provided value.
        """
        self.page.fill(self.FULL_NAME_INPUT, value)

    def fill_email(self, value: str) -> None:
        """
        Fill the email input field with the provided value.
        """
        self.page.fill(self.EMAIL_INPUT, value)

    def fill_current_address(self, value: str) -> None:
        """
        Fill the current address input field with the provided value.
        """
        self.page.fill(self.CURRENT_ADDRESS_INPUT, value)

    def fill_permanent_address(self, value: str) -> None:
        """
        Fill the permanent address input field with the provided value.
        """
        self.page.fill(self.PERMANENT_ADDRESS_INPUT, value)

    def submit(self) -> None:
        """
        Click Submit button.
        """
        self.page.click(self.SUBMIT_BUTTON)

    def submit_form(
        self,
        *,
        full_name: str,
        email: str,
        current_address: str,
        permanent_address: str,
    ) -> None:
        """
        High-level intent method.
        Keeps tests readable and focused on behavior.
        """
        self.fill_full_name(full_name)
        self.fill_email(email)
        self.fill_current_address(current_address)
        self.fill_permanent_address(permanent_address)
        self.submit()

    # ---------- Queries ----------

    def output_text(self) -> str:
        """
        Returns raw output block text after submission.
        """
        return self.page.locator(self.OUTPUT_CONTAINER).inner_text()
