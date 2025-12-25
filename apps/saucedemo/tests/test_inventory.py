"""Test suite for verifying the inventory functionality of SauceDemo using Playwright."""

import pytest
from apps.saucedemo.pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_inventory_page_loaded(authenticated_page):
    """Test that the inventory page is loaded successfully."""
    inventory = InventoryPage(authenticated_page)

    assert inventory.is_loaded()
    assert inventory.get_title() == "Products"
    assert inventory.get_items_count() > 0
