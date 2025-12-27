"""
Widgets landing page for DemoQA application.
Navigation-only page object.
"""

from __future__ import annotations

from typing import Self

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class WidgetsPage(BaseDemoQAPage):
    """
    Page object for DemoQA Widgets section (navigation only).

    Responsibility:
    - Open widget sub-pages via side menu
    """

    URL_PATH = "widgets"

    # ---------- Page readiness ----------
    PAGE_READY = ".left-pannel"

    # ---------- Side menu ----------
    SIDE_MENU_ITEMS = ".element-list .menu-list li"

    # ---------- Visible menu names ----------
    ACCORDIAN = "Accordian"
    AUTO_COMPLETE = "Auto Complete"
    DATE_PICKER = "Date Picker"
    SLIDER = "Slider"
    PROGRESS_BAR = "Progress Bar"
    TABS = "Tabs"
    TOOL_TIPS = "Tool Tips"
    MENU = "Menu"
    SELECT_MENU = "Select Menu"

    def open_page(self) -> Self:
        """Open Widget page"""
        self.open(self.URL_PATH)
        return self

    # ---------- Readiness ----------

    def is_loaded(self) -> bool:
        """
        Return True when Widgets section shell is visible.
        """
        return self.page.is_visible(self.PAGE_READY)

    # ---------- Navigation ----------

    def open_accordian(self) -> Self:
        self._open_menu_item(self.ACCORDIAN)
        return self

    def open_auto_complete(self) -> Self:
        self._open_menu_item(self.AUTO_COMPLETE)
        return self

    def open_date_picker(self) -> Self:
        self._open_menu_item(self.DATE_PICKER)
        return self

    def open_slider(self) -> Self:
        self._open_menu_item(self.SLIDER)
        return self

    def open_progress_bar(self) -> Self:
        self._open_menu_item(self.PROGRESS_BAR)
        return self

    def open_tabs(self) -> Self:
        self._open_menu_item(self.TABS)
        return self

    def open_tool_tips(self) -> Self:
        self._open_menu_item(self.TOOL_TIPS)
        return self

    def open_menu(self) -> Self:
        self._open_menu_item(self.MENU)
        return self

    def open_select_menu(self) -> Self:
        self._open_menu_item(self.SELECT_MENU)
        return self

    # ---------- Internal ----------

    def _open_menu_item(self, name: str):
        """
        Internal helper to open a widget page by visible menu text.
        """
        self.page.locator(self.SIDE_MENU_ITEMS).filter(has_text=name).click()
