# apps/saucedemo/pages/inventory_page.py
from apps.saucedemo.pages.base_sauce_page import BaseSaucePage

class InventoryPage(BaseSaucePage):
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'

    def assert_loaded(self):
        self.page.wait_for_selector(self.INVENTORY_CONTAINER, state="visible", timeout=10000)
