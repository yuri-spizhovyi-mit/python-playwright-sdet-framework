from apps.saucedemo.pages.base_sauce_page import BaseSaucePage


class LoginPage(BaseSaucePage):
    USERNAME = '[data-test="username"]'
    PASSWORD = '[data-test="password"]'
    LOGIN_BTN = '[data-test="login-button"]'
    ERROR = '[data-test="error"]'

    def open(self):
        super().open("")  # login is the root page
        return self

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME, username)
        self.page.fill(self.PASSWORD, password)
        self.page.click(self.LOGIN_BTN)

    def get_error_text(self) -> str:
        return self.page.text_content(self.ERROR) or ""
