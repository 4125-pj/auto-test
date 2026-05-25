"""
商品分类 API 对象
"""
from api.base_api import BaseAPI
from config.settings import Config


class CategoryAPI(BaseAPI):
    """商品分类相关接口（走管理后台地址）"""

    def __init__(self, token: str):
        super().__init__(base_url=Config.UI_BASE_URL + '/admin')
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def save_category(self, name: str, status: str = '1', order: int = 1) -> dict:
        """新增商品分类"""
        resp = self.post('/sales/goods-category/save', json={
            'status': status, 'name': name, 'order': order,
        })
        return resp.json()

    def list_categories(self, page_num: int = 1, page_size: int = 10) -> dict:
        """商品分类分页列表"""
        resp = self.get('/sales/goods-category/page', params={'pageNum': page_num, 'pageSize': page_size})
        return resp.json()
