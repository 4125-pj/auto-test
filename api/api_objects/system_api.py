"""
系统模块 API 对象 - 若依(RuoYi)框架标准接口
"""
from api.base_api import BaseAPI


class SystemAPI(BaseAPI):
    """系统管理相关接口（需要 token 鉴权）"""

    def __init__(self, token: str):
        super().__init__()
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    # ========== 用户管理 ==========

    def list_users(self, page_num: int = 1, page_size: int = 10) -> dict:
        """用户列表 GET /system/user/list"""
        resp = self.get('/system/user/list', params={'pageNum': page_num, 'pageSize': page_size})
        return resp.json()

    # ========== 配置管理 ==========

    def create_config(self, config_data: dict) -> dict:
        """新增参数配置 POST /system/config"""
        resp = self.post('/system/config', json=config_data)
        return resp.json()

    def get_config(self, config_id: int) -> dict:
        """查询参数配置 GET /system/config/{id}"""
        resp = self.get(f'/system/config/{config_id}')
        return resp.json()

    def list_configs(self, page_num: int = 1, page_size: int = 10) -> dict:
        """配置列表 GET /system/config/list"""
        resp = self.get('/system/config/list', params={'pageNum': page_num, 'pageSize': page_size})
        return resp.json()
