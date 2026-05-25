"""
商品 API 对象
"""
from typing import Optional
from api.base_api import BaseAPI
from config.settings import Config


class GoodsAPI(BaseAPI):
    """商品相关接口（走管理后台地址）"""

    def __init__(self, token: str):
        super().__init__(base_url=Config.UI_BASE_URL + '/admin')
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def save(self, name: str, category_id: str, sale_price: float,
             alias_name: str = '', status: str = '1', order: int = 1,
             is_main: str = '1', category_name: Optional[str] = None,
             warehouse_list: Optional[list] = None) -> dict:
        """
        新增商品
        POST /admin/sales/goods/save
        """
        body = {
            'isMain': is_main,
            'status': status,
            'name': name,
            'aliasName': alias_name or name,
            'salePrice': sale_price,
            'order': order,
            'categoryId': category_id,
            'warehouseList': warehouse_list or [],
        }
        if category_name:
            body['goodsCategoryName'] = category_name
        resp = self.post('/sales/goods/save', json=body)
        return resp.json()

    def list_page(self, page_num: int = 1, page_size: int = 10) -> dict:
        """商品分页列表"""
        resp = self.get('/sales/goods/page', params={'pageNum': page_num, 'pageSize': page_size})
        return resp.json()

    def delete_goods(self, goods_id: str) -> dict:
        """删除商品"""
        resp = super().delete(f'/sales/goods/delete/{goods_id}')
        return resp.json()
