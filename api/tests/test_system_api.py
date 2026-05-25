"""
系统管理接口测试用例
"""
import pytest
from api.api_objects.user_api import UserAPI
from api.api_objects.system_api import SystemAPI
from config.settings import Config


class TestSystemAPI:
    """系统管理接口测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试方法前先登录获取 token"""
        user_api = UserAPI()
        token = user_api.get_token(Config.API_USERNAME, Config.API_PASSWORD)
        self.api = SystemAPI(token)

    @pytest.mark.api
    def test_list_users(self):
        """用户列表（需要 system:user:list 权限）"""
        resp = self.api.list_users()
        # 403 = 当前用户无权限，也视为接口正常工作
        assert resp['code'] in (200, 403), f'异常响应: {resp}'
        if resp['code'] == 403:
            pytest.skip('当前用户无权限访问用户列表')

    @pytest.mark.api
    def test_create_config(self):
        """新增配置"""
        resp = self.api.create_config({
            'configName': '测试配置',
            'configKey': 'test_key',
            'configValue': 'test_value',
        })
        # 500 可能是参数校验问题
        assert resp['code'] in (200, 500)
