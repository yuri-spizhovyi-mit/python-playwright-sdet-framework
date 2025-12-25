from apps.saucedemo.pages.base_sauce_page import BaseSaucePage


class InventoryPage(BaseSaucePage):
    """SauceDemo inventory screen."""

    INVENTORY_CONTAINER = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    PAGE_TITLE = ".title"

    def open(self, path: str = "inventory.html"):
        """Open the inventory page directly."""
        super().open(path)
        return self

    def is_loaded(self) -> bool:
        """Check that inventory page is loaded."""
        return self.page.is_visible(self.INVENTORY_CONTAINER)

    def get_title(self) -> str:
        """Return inventory page title."""
        return self.page.text_content(self.PAGE_TITLE) or ""

    def get_items_count(self) -> int:
        """Return number of inventory items displayed."""
        return self.page.locator(self.INVENTORY_ITEM).count()
