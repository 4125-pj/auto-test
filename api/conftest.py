"""
API 测试 Fixture - 自动登录获取 token
"""
import pytest
from api.api_objects.user_api import UserAPI
from api.base_api import BaseAPI
from config.settings import Config


@pytest.fixture(scope='session')
def admin_token() -> str:
    """登录 API 服务获取 token（session 级别，只登录一次）"""
    api = UserAPI()
    return api.get_token(Config.API_USERNAME, Config.API_PASSWORD)


@pytest.fixture(scope='session')
def backend_token() -> str:
    """登录管理后台获取 token — 含完整菜单权限"""
    api = BaseAPI(base_url=Config.UI_BASE_URL + '/admin')

    # 登录（带 captcha 标记）
    resp = api.post('/auth/login', json={
        'username': Config.UI_USERNAME,
        'password': Config.UI_PASSWORD,
        'captcha': True,
    })
    data = resp.json()
    assert data['code'] == 200, f'Admin login failed: {data}'
    token = data['data']['accessToken']

    # 登录后加载权限上下文（否则部分接口返回 403）
    api.session.headers.update({'Authorization': f'Bearer {token}'})
    api.get('/system/user/info')
    api.get('/system/menu/permissions')
    api.get('/system/menu/route-menu')

    return token


@pytest.fixture
def sys_api(admin_token):
    """已登录的系统管理 API 对象"""
    from api.api_objects.system_api import SystemAPI
    return SystemAPI(admin_token)


@pytest.fixture
def category_api(backend_token):
    """已登录的商品分类 API 对象"""
    from api.api_objects.category_api import CategoryAPI
    return CategoryAPI(backend_token)


@pytest.fixture
def goods_api(backend_token):
    """已登录的商品 API 对象"""
    from api.api_objects.goods_api import GoodsAPI
    return GoodsAPI(backend_token)
