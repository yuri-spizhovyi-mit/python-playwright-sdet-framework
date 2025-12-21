from playwright.sync_api import sync_playwright


class BrowserManager:
    def __init__(self, browser_name: str = "chromium", headless: bool = True):
        self.browser_name = browser_name
        self.headless = headless
        self._pw = None
        self._browser = None

    def start(self):
        self._pw = sync_playwright().start()
        browser_type = getattr(self._pw, self.browser_name)
        self._browser = browser_type.launch(headless=self.headless)
        return self._browser

    def stop(self):
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()
