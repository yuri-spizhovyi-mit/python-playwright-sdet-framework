# apps/saucedemo/pages/inventory_page.py
from apps.saucedemo.pages.base_sauce_page import BaseSaucePage


class InventoryPage(BaseSaucePage):
    """Page object for the Sauce Demo Inventory page."""

    INVENTORY_CONTAINER = '[data-test="inventory-container"]'

    def assert_loaded(self):
        self.page.wait_for_selector(
            self.INVENTORY_CONTAINER, state="visible", timeout=10000
        )
