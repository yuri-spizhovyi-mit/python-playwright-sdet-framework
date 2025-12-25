"""
Test suite for verifying the authentication functionality of SauceDemo using Playwright.
"""

import pytest
from apps.saucedemo.pages.login_page import LoginPage
from apps.saucedemo.pages.inventory_page import InventoryPage
from core.config import Config


@pytest.mark.smoke
@pytest.mark.full
def test_login_success(page):
    """Test that the user can login successfully and access the inventory page."""

    LoginPage(page).open().login(
        username=Config.SAUCE_STANDARD_USER,
        password=Config.SAUCE_PASSWORD,
    )

    assert InventoryPage(page).is_loaded()


@pytest.mark.full
def test_login_locked_out_user(page):
    """Test that the user cannot login with a locked out user."""
    login = LoginPage(page).open()
    login.login(
        Config.SAUCE_LOCKED_OUT_USER,
        Config.SAUCE_PASSWORD,
    )

    assert "locked out" in LoginPage(page).get_error_text().lower()


@pytest.mark.full
def test_login_invalid_credentials(page):
    """Test that the user cannot login with invalid credentials."""
    LoginPage(page).open().login(
        Config.SAUCE_INVALID_USER, Config.SAUCE_INVALID_PASSWORD
    )
    assert LoginPage(page).get_error_text()
