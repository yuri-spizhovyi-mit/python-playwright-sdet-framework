"""Elements landing page for DemoQA application."""

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class ElementsPage(BaseDemoQAPage):
    """Page object for DemoQA Elements section (navigation only)."""

    URL_PATH = "elements"

    # Page readiness (app shell)
    PAGE_READY = ".left-pannel"

    # Side menu
    SIDE_MENU_ITEMS = ".element-list .menu-list li"

    # Visible menu names (not selectors)
    TEXT_BOX = "Text Box"
    CHECK_BOX = "Check Box"
    RADIO_BUTTON = "Radio Button"

    def is_loaded(self) -> bool:
        """
        Return True when Elements section shell and side menu are visible.
        """
        panel_visible = self.page.is_visible(self.PAGE_READY)
        menu_visible = self.page.locator(self.SIDE_MENU_ITEMS).first.is_visible()

        return panel_visible and menu_visible

    def open_text_box(self):
        """Open Text Box page from Elements menu."""
        self._open_menu_item(self.TEXT_BOX)
        return self

    def open_check_box(self):
        """Open Check Box page from Elements menu."""
        self._open_menu_item(self.CHECK_BOX)
        return self

    def open_radio_button(self):
        """Open Radio Button page from Elements menu."""
        self._open_menu_item(self.RADIO_BUTTON)
        return self

    def _open_menu_item(self, name: str):
        """Internal helper to open a side menu item."""
        menu_items = self.page.locator(self.SIDE_MENU_ITEMS)

        # Ensure side menu is fully rendered and interactable
        menu_items.first.wait_for(state="visible")

        menu_items.filter(has_text=name).first.click()
