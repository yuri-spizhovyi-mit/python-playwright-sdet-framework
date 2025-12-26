"""Elements page for DemoQA application."""

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class ElementsPage(BaseDemoQAPage):
    """Page object for DemoQA Elements section."""

    URL_PATH = "elements"
    PAGE_TITLE = ".main-header"
    SIDE_MENU_ITEMS = ".element-list .menu-list li"
    # --- Elements widgets selectors ---
    TEXT_BOX_MENU = "Text Box"
    CHECK_BOX_MENU = "Check Box"
    RADIO_BUTTON_MENU = "Radio Button"
    # --- Text Box selectors ---
    FULL_NAME = "#userName"
    EMAIL = "#userEmail"
    CURRENT_ADDRESS = "#currentAddress"
    SUBMIT_BTN = "#submit"
    OUTPUT = "#output"

    def is_loaded(self) -> bool:
        """Check if elements page is loaded."""
        return self.page.is_visible(self.PAGE_TITLE)

    def get_title(self) -> str:
        """Get the title of the elements page."""
        return self.page.text_content(self.PAGE_TITLE) or ""

    def open_menu_item(self, name: str):
        """Open a menu item by name."""
        self.page.locator(self.SIDE_MENU_ITEMS).filter(has_text=name).click()

    def open_elements_item(self, name: str):
        """Open an Elements side menu item by visible name."""
        self.page.locator(self.SIDE_MENU_ITEMS).filter(has_text=name).click()
        return self

    def fill_text_box(self, name: str, email: str, address: str):
        """Fill the text box with the given name, email, and address."""
        self.page.fill(self.FULL_NAME, name)
        self.page.fill(self.EMAIL, email)
        self.page.fill(self.CURRENT_ADDRESS, address)
        self.page.click(self.SUBMIT_BTN)
        return self

    def output_visible(self) -> bool:
        """Check if the output is visible."""
        return self.page.is_visible(self.OUTPUT)
