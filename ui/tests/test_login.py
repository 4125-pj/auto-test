"""
登录功能 UI 测试用例 (Playwright)
"""
import pytest
from ui.pages.login_page import LoginPage
from config.settings import Config


class TestLogin:
    """登录测试"""

    @pytest.mark.smoke
    @pytest.mark.ui
    def test_login_success(self, page):
        """登录成功"""
        page.goto(f'{Config.UI_BASE_URL}/#/auth/login')
        login_page = LoginPage(page)
        login_page.login(Config.UI_USERNAME, Config.UI_PASSWORD)
        login_page.slide_verify()
        login_page.click_login()
        login_page.wait_for_success()
        assert '/#/dashboard/analytics' in page.url

    @pytest.mark.ui
    def test_login_fail_wrong_password(self, page):
        """登录失败 - 错误密码"""
        page.goto(f'{Config.UI_BASE_URL}/#/auth/login')
        login_page = LoginPage(page)
        login_page.login(Config.UI_USERNAME, 'wrong_password')
        login_page.slide_verify()
        login_page.click_login()
        # 失败后应停留在登录页
        assert '/#/auth/login' in page.url
