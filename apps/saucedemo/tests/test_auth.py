import pytest
from apps.saucedemo.pages.login_page import LoginPage
from apps.saucedemo.pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_login_success(page, sauce_creds):
    username, password = sauce_creds

    login = LoginPage(page).open()
    login.login(username, password)

    InventoryPage(page).assert_loaded()
    assert False
