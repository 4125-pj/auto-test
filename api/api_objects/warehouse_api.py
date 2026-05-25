"""
仓库管理模块 API 对象
"""
from typing import Optional
from api.base_api import BaseAPI
from config.settings import Config


class WarehouseAPI(BaseAPI):
    """仓库管理相关接口（走管理后台地址）"""

    def __init__(self, token: str):
        super().__init__(base_url=Config.UI_BASE_URL + '/admin')
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    # ========== 仓库 ==========

    def save(self, name: str, warehouse_type: str, category_id: str,
             contact_name: str = '', mobile: str = '',
             detail_address: str = '', status: str = '1',
             order: int = 1, print_template: str = '',
             category_name: Optional[str] = None) -> dict:
        """
        新增仓库
        POST /admin/sales/warehouse/save
        type: 1=发货仓库, 3=退货仓库
        """
        body = {
            'type': warehouse_type,
            'status': status,
            'name': name,
            'contactName': contact_name,
            'mobile': mobile,
            'detailAddress': detail_address,
            'order': order,
            'printTemplate': print_template,
            'categoryId': category_id,
        }
        if category_name:
            body['categoryName'] = category_name
        resp = self.post('/sales/warehouse/save', json=body)
        return resp.json()

    def update(self, warehouse_id: str, name: str, warehouse_type: str, category_id: str,
               contact_name: str = '', mobile: str = '',
               detail_address: str = '', status: str = '1',
               order: int = 1, print_template: str = '',
               category_name: Optional[str] = None) -> dict:
        """
        编辑仓库
        PUT /admin/sales/warehouse/update
        """
        body = {
            'id': warehouse_id,
            'type': warehouse_type,
            'status': status,
            'name': name,
            'contactName': contact_name,
            'mobile': mobile,
            'detailAddress': detail_address,
            'order': order,
            'printTemplate': print_template,
            'categoryId': category_id,
        }
        if category_name:
            body['categoryName'] = category_name
        resp = self.put('/sales/warehouse/update', json=body)
        return resp.json()

    def list_page(self, page_num: int = 1, page_size: int = 10) -> dict:
        """
        仓库分页列表
        GET /admin/sales/warehouse/page
        """
        resp = self.get('/sales/warehouse/page', params={'pageNum': page_num, 'pageSize': page_size})
        return resp.json()
