"""
UI 测试 Fixture - Playwright 浏览器管理
"""
import pytest
from playwright.sync_api import sync_playwright
from common.logger import logger
from config.settings import Config


BROWSER_LAUNCH_OPTS = {
    'chromium': {'channel': 'chrome', 'headless': Config.HEADLESS},
    'firefox': {'headless': Config.HEADLESS},
    'webkit': {'headless': Config.HEADLESS},
}

CONTEXT_OPTS = {
    'viewport': {'width': 1920, 'height': 1080},
    'ignore_https_errors': True,
}


@pytest.fixture(scope='function')
def page():
    """创建 Playwright 页面，测试结束后自动关闭"""
    browser_name = Config.BROWSER.lower()
    if browser_name not in BROWSER_LAUNCH_OPTS:
        raise ValueError(f'不支持的浏览器: {browser_name}，可选: {list(BROWSER_LAUNCH_OPTS.keys())}')

    with sync_playwright() as pw:
        browser = getattr(pw, browser_name).launch(**BROWSER_LAUNCH_OPTS[browser_name])
        context = browser.new_context(**CONTEXT_OPTS)
        _page = context.new_page()
        _page.set_default_timeout(Config.PAGE_LOAD_TIMEOUT)

        logger.info('Browser started: %s (headless=%s)', browser_name, Config.HEADLESS)

        yield _page

        context.close()
        browser.close()
        logger.info('Browser closed')
