"""
用户认证接口测试用例
对应 API: POST /api/auth/login
"""
import pytest
from api.api_objects.user_api import UserAPI
from config.settings import Config


class TestLogin:
    """登录接口测试"""

    def setup_method(self):
        self.user_api = UserAPI()

    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_success(self):
        """登录成功 - 正确用户名密码"""
        resp = self.user_api.login(Config.API_USERNAME, Config.API_PASSWORD)
        assert resp['code'] == 200, f'登录失败: {resp}'
        assert 'accessToken' in resp['data'], '响应中没有 accessToken'
        assert resp['data']['expiresIn'] > 0, 'token 过期时间异常'
        # 验证 token 格式 (JWT: xxx.yyy.zzz)
        token = resp['data']['accessToken']
        assert token.count('.') == 2, f'token 格式异常: {token[:20]}...'

    @pytest.mark.api
    def test_login_fail_wrong_password(self):
        """登录失败 - 错误密码"""
        resp = self.user_api.login(Config.API_USERNAME, 'wrong_password')
        # 预期返回非 200 的 code
        assert resp['code'] != 200

    @pytest.mark.api
    def test_login_fail_empty_username(self):
        """登录失败 - 用户名为空"""
        resp = self.user_api.login('', Config.API_PASSWORD)
        assert resp['code'] != 200

    @pytest.mark.api
    def test_login_fail_empty_password(self):
        """登录失败 - 密码为空"""
        resp = self.user_api.login(Config.API_USERNAME, '')
        assert resp['code'] != 200

    @pytest.mark.api
    def test_get_token(self):
        """获取 token 辅助方法"""
        token = self.user_api.get_token(Config.API_USERNAME, Config.API_PASSWORD)
        assert isinstance(token, str) and len(token) > 50
        assert token.count('.') == 2
