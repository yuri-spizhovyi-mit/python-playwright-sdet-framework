"""
Slider page object for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class SliderPage(BaseDemoQAPage):
    """
    Page object representing the Slider widget.

    Responsibility:
    - Interact with the slider control
    - Read current slider value
    """

    URL_PATH = "slider"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Slider')"

    # ---------- Slider ----------
    SLIDER_INPUT = "input[type='range']"
    SLIDER_VALUE = "#sliderValue"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()

    # ---------- Actions ----------

    def set_value(self, value: int) -> None:
        """
        Set slider to a specific value using keyboard interaction.
        DemoQA slider range: 0–100, step 1
        """
        if not 0 <= value <= 100:
            raise ValueError("Slider value must be between 0 and 100")

        slider = self.page.locator(self.SLIDER_INPUT)
        slider.focus()

        # Reset to minimum first for deterministic behavior
        slider.press("Home")

        # Increment to desired value
        for _ in range(value):
            slider.press("ArrowRight")

    # ---------- Queries ----------

    def current_value(self) -> int:
        """
        Return current slider value as integer.
        """
        return int(self.page.locator(self.SLIDER_VALUE).input_value())
