"""Browser lifecycle manager."""

from playwright.sync_api import sync_playwright, Browser, BrowserContext


class BrowserManager:
    """Manages Playwright browser instances."""

    def __init__(self, browser_type="chromium", headless=True):
        self.browser_type = browser_type
        self.headless = headless
        self.playwright = None
        self.browser = None

    def start(self) -> Browser:
        """Launch browser."""
        self.playwright = sync_playwright().start()
        browser_launcher = getattr(self.playwright, self.browser_type)
        self.browser = browser_launcher.launch(headless=self.headless)
        return self.browser

    def create_context(self, **kwargs) -> BrowserContext:
        """Create isolated browser context."""
        return self.browser.new_context(
            viewport={"width": 1920, "height": 1080}, **kwargs
        )

    def stop(self):
        """Cleanup resources."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
