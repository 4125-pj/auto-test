"""
全局 Pytest Fixture 和 Hook
"""
import pytest
from datetime import datetime
from common.logger import logger


@pytest.fixture(scope='session', autouse=True)
def session_setup():
    """全局测试开始/结束"""
    logger.info('=' * 60)
    logger.info('Test started: %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.info('=' * 60)
    yield
    logger.info('=' * 60)
    logger.info('Test finished: %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.info('=' * 60)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时截图（Playwright）"""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        page = item.funcargs.get('page')
        if page:
            from common.utils import screenshot_path
            path = screenshot_path(item.name)
            page.screenshot(path=path)
            logger.error('Screenshot saved: %s', path)
