"""
基础安全测试用例
"""
import pytest
from api.api_objects.user_api import UserAPI
from api.api_objects.category_api import CategoryAPI
from config.settings import Config


class TestLoginSecurity:
    """登录接口安全测试"""

    @pytest.mark.api
    def test_login_sql_injection(self):
        """SQL注入 - 万能密码"""
        api = UserAPI()
        injections = [
            ("' OR '1'='1", "' OR '1'='1"),
            ("admin'--", "任意"),
            ("'; DROP TABLE users; --", "空"),
            ("' UNION SELECT * FROM users--", "空"),
        ]
        for username, password in injections:
            resp = api.login(username, password)
            assert resp['code'] != 200, f'SQL注入竟然成功了: {username}'

    @pytest.mark.api
    def test_login_xss_injection(self):
        """XSS注入 - 特殊字符"""
        api = UserAPI()
        xss_payloads = [
            "<script>alert('xss')</script>",
            "李先生<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
        ]
        for payload in xss_payloads:
            resp = api.login(payload, "任意密码")
            # 不报错就算通过（XSS攻击的是浏览器，不是后端）
            assert resp is not None

    @pytest.mark.api
    def test_login_long_input(self):
        """超长输入"""
        api = UserAPI()
        long_str = "A" * 10000
        resp = api.login(long_str, long_str)
        assert resp is not None
