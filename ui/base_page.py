"""
Page Object 基类 - 封装 Playwright 常用操作
"""
from playwright.sync_api import Page
from common.logger import logger


class BasePage:
    """所有 Page Object 的基类"""

    def __init__(self, page: Page):
        self.page = page

    # ========== 元素定位 ==========

    def locator(self, selector: str):
        """获取元素定位器"""
        return self.page.locator(selector)

    # ========== 常用操作 ==========

    def click(self, selector: str):
        """点击元素"""
        self.page.locator(selector).click()
        logger.info('Click: %s', selector)

    def input_text(self, selector: str, text: str):
        """输入文本（先清空再输入）"""
        loc = self.page.locator(selector)
        loc.fill('')
        loc.fill(text)
        logger.info('Input [%s]: %s', selector, text)

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        return self.page.locator(selector).text_content() or ''

    def is_visible(self, selector: str) -> bool:
        """判断元素是否可见"""
        return self.page.locator(selector).is_visible()

    def get_title(self) -> str:
        """获取当前页面标题"""
        return self.page.title()

    def get_url(self) -> str:
        """获取当前页面 URL"""
        return self.page.url

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """等待元素出现"""
        self.page.wait_for_selector(selector, timeout=timeout)

    # ========== 辅助 ==========

    def screenshot(self, name: str):
        """截图"""
        from common.utils import screenshot_path
        path = screenshot_path(name)
        self.page.screenshot(path=path)
        logger.info('Screenshot saved: %s', path)
