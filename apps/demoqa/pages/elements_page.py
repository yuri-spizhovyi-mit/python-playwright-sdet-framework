"""Elements page for DemoQA application."""
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class ElementsPage(BaseDemoQAPage):
    """Page object for DemoQA Elements section."""

    URL_PATH = "elements"
    PAGE_TITLE = ".main-header"
    SIDE_MENU_ITEMS = ".element-list .menu-list li"

    def is_loaded(self) -> bool:
        """Check if elements page is loaded."""
        return self.page.is_visible(self.PAGE_TITLE)

    def get_title(self) -> str:
        """Get the title of the elements page."""
        return self.page.text_content(self.PAGE_TITLE) or ""

    def open_menu_item(self, name: str):
        """Open a menu item by name."""
        self.page.locator(self.SIDE_MENU_ITEMS).filter(has_text=name).click()
