"""
用户认证模块 API 对象
"""
from api.base_api import BaseAPI


class UserAPI(BaseAPI):
    """用户认证相关接口"""

    def login(self, username: str, password: str) -> dict:
        """
        登录
        POST /api/auth/login
        Body: {"username": "super", "password": "xxx"}
        Response: {"code": 200, "msg": null, "data": {"accessToken": "...", "expiresIn": 72000000}}
        """
        path = '/auth/login'
        body = {'username': username, 'password': password}
        resp = self.post(path, json=body)
        return resp.json()

    def get_token(self, username: str, password: str) -> str:
        """获取 accessToken（其他 API 对象可复用）"""
        data = self.login(username, password)
        assert data.get('code') == 200, f'登录失败: {data}'
        return data['data']['accessToken']
