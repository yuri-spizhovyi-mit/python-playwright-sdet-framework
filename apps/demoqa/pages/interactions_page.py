"""
Interactions landing page for DemoQA application.
Navigation-only page object.
"""

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class InteractionsPage(BaseDemoQAPage):
    """
    Page object for DemoQA Interactions section.

    Responsibility:
    - Open Interactions section
    - Navigate to interaction feature pages via side menu

    Does NOT:
    - Perform drag, drop, resize, or sort actions
    """

    URL_PATH = "interaction"

    # ---------- Page readiness ----------
    PAGE_READY = ".left-pannel"

    # ---------- Side menu ----------
    SIDE_MENU_ITEMS = ".element-list .menu-list li"

    # ---------- Visible menu names ----------
    SORTABLE = "Sortable"
    SELECTABLE = "Selectable"
    RESIZABLE = "Resizable"
    DROPPABLE = "Droppable"
    DRAGGABLE = "Dragabble"

    # ---------- Navigation ----------

    def open_page(self) -> "InteractionsPage":
        """Open Interactions landing page."""
        self.open(self.URL_PATH)
        return self

    def is_loaded(self) -> bool:
        """Return True when Interactions section shell is visible."""
        return self.page.is_visible(self.PAGE_READY)

    def open_sortable(self) -> "InteractionsPage":
        """Open Sortable interaction page."""
        self._open_menu_item(self.SORTABLE)
        return self

    def open_selectable(self) -> "InteractionsPage":
        """Open Selectable interaction page."""
        self._open_menu_item(self.SELECTABLE)
        return self

    def open_resizable(self) -> "InteractionsPage":
        """Open Resizable interaction page."""
        self._open_menu_item(self.RESIZABLE)
        return self

    def open_droppable(self) -> "InteractionsPage":
        """Open Droppable interaction page."""
        self._open_menu_item(self.DROPPABLE)
        return self

    def open_draggable(self) -> "InteractionsPage":
        """Open Dragabble interaction page."""
        self._open_menu_item(self.DRAGGABLE)
        return self

    # ---------- Internal helpers ----------

    def _open_menu_item(self, name: str) -> None:
        """Click side menu item by visible text."""
        self.page.locator(self.SIDE_MENU_ITEMS).filter(has_text=name).click()
