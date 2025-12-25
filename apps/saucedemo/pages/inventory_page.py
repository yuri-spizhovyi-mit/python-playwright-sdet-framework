"""Inventory page for SauceDemo application."""

from apps.saucedemo.pages.base_sauce_page import BaseSaucePage


class InventoryPage(BaseSaucePage):
    """SauceDemo inventory screen."""

    TITLE = ".title"
    INVENTORY_ITEM = ".inventory_item"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"

    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def is_loaded(self) -> bool:
        """Check that inventory page is loaded."""
        return self.page.is_visible(self.TITLE)

    def get_title(self) -> str:
        """Return inventory page title."""
        return self.page.text_content(self.TITLE) or ""

    def get_items_count(self) -> int:
        """Return number of inventory items displayed."""
        return self.page.locator(self.INVENTORY_ITEM).count()

    # --- Cart Actions ---

    def add_item_to_cart(self, item_name: str):
        """Add an item to the cart."""
        self.page.locator(f".inventory_item:has-text('{item_name}') button").click()

    def remove_item_from_cart(self, item_name: str):
        """Remove an item from the cart."""
        self.page.locator(f".inventory_item:has-text('{item_name}') button").click()

    def get_cart_count(self) -> int:
        """Return the number of items in the cart."""
        if self.page.is_visible(self.CART_BADGE):
            return int(self.page.text_content(self.CART_BADGE))
        return 0

    # --- Logout Actions ---

    def logout(self):
        """Logout from the application."""
        self.page.click(self.BURGER_MENU_BUTTON)
        self.page.click(self.LOGOUT_LINK)
