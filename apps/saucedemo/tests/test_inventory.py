"""Test suite for verifying the inventory functionality of SauceDemo using Playwright."""

import pytest
from apps.saucedemo.pages.inventory_page import InventoryPage
from apps.saucedemo.pages.login_page import LoginPage


@pytest.mark.smoke
def test_inventory_page_loaded(authenticated_page):
    """Test that the inventory page is loaded successfully."""
    inventory = InventoryPage(authenticated_page)

    assert inventory.is_loaded()
    assert inventory.get_title() == "Products"
    assert inventory.get_items_count() > 0


@pytest.mark.full
def test_add_item_to_cart(authenticated_page):
    """Test that the user can add an item to the cart."""
    inventory = InventoryPage(authenticated_page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    assert inventory.get_cart_count() == 1


@pytest.mark.full
def test_remove_item_from_cart(authenticated_page):
    """Test that the user can remove an item from the cart."""
    inventory = InventoryPage(authenticated_page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.remove_item_from_cart("Sauce Labs Backpack")
    assert inventory.get_cart_count() == 0


@pytest.mark.full
def test_logout(authenticated_page):
    """Test that the user can logout from the application and be redirected to the login page."""
    inventory = InventoryPage(authenticated_page)
    inventory.logout()
    login_page = LoginPage(authenticated_page)
    assert login_page.page.is_visible(login_page.LOGIN_BTN)
