"""
商品管理接口测试用例
"""
import pytest
from api.api_objects.goods_api import GoodsAPI
from api.api_objects.category_api import CategoryAPI
from api.api_objects.warehouse_api import WarehouseAPI


class TestGoods:
    """商品管理测试"""

    @pytest.fixture
    def goods_data(self, backend_token: str):
        """获取商品所需的基础数据（分类、仓库）"""
        cat_api = CategoryAPI(backend_token)
        cat_resp = cat_api.list_categories()
        if cat_resp['code'] != 200 or not cat_resp.get('data', {}).get('items'):
            pytest.skip('没有可用的商品分类')
        c = cat_resp['data']['items'][0]

        wh_api = WarehouseAPI(backend_token)
        wh_resp = wh_api.list_page()
        if wh_resp['code'] == 200 and wh_resp.get('data', {}).get('items'):
            warehouse_list = [
                {'label': '', 'value': '', 'warehouseType': w['type'],
                 'isDefault': '1', 'count': 0, 'warehouseId': w['id']}
                for w in wh_resp['data']['items']
            ]
        else:
            warehouse_list = []

        return c['id'], c['name'], warehouse_list

    @pytest.mark.api
    def test_create_goods(self, goods_api: GoodsAPI, goods_data):
        """新增商品"""
        category_id, category_name, warehouse_list = goods_data
        resp = goods_api.save(
            name='天麻酒',
            category_id=category_id,
            category_name=category_name,
            sale_price=99,
            alias_name='天麻酒',
            order=1,
            warehouse_list=warehouse_list,
        )
        assert resp['code'] in (200, 201), f'创建失败: {resp}'

    @pytest.mark.api
    def test_list_goods(self, goods_api: GoodsAPI):
        """商品分页列表"""
        resp = goods_api.list_page()
        assert resp['code'] == 200, f'查询失败: {resp}'
        assert resp.get('data', {}).get('items') is not None
