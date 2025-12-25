"""
Test suite for verifying the authentication functionality of SauceDemo using Playwright.
"""

import pytest
from apps.saucedemo.pages.login_page import LoginPage
from apps.saucedemo.pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_login_success(page, sauce_creds):
    """Test that the user can login successfully and access the inventory page."""
    username, password = sauce_creds

    login = LoginPage(page).open()
    login.login(username, password)

    assert InventoryPage(page).is_loaded()
