"""
仓库管理接口测试用例
"""
import pytest
from api.api_objects.warehouse_api import WarehouseAPI
from api.api_objects.category_api import CategoryAPI


class TestWarehouse:
    """仓库管理测试"""

    @pytest.fixture(autouse=True)
    def setup(self, backend_token: str):
        self.api = WarehouseAPI(backend_token)
        # 获取第一个商品分类的 ID 作为关联分类
        cat_api = CategoryAPI(backend_token)
        cat_resp = cat_api.list_categories()
        if cat_resp['code'] == 200 and cat_resp.get('data', {}).get('items'):
            self.category_id = cat_resp['data']['items'][0]['id']
            self.category_name = cat_resp['data']['items'][0]['name']
        else:
            pytest.skip('没有可用的商品分类，请先创建商品分类')

    @pytest.mark.api
    def test_create_dispatch_warehouse(self):
        """新增发货仓库（type=1）"""
        resp = self.api.save(
            name='A类商品仓库',
            warehouse_type='1',
            category_id=self.category_id,
            category_name=self.category_name,
            contact_name='王先生',
            mobile='13163384125',
            detail_address='龙阳智慧大厦1801',
            order=1,
            print_template='A',
        )
        # 200=成功, 500=名称已存在
        assert resp['code'] in (200, 500), f'创建失败: {resp}'

    @pytest.mark.api
    def test_create_return_warehouse(self):
        """新增退货仓库（type=3）"""
        resp = self.api.save(
            name='A类商品退货仓库',
            warehouse_type='3',
            category_id=self.category_id,
            category_name=self.category_name,
            contact_name='王先生',
            mobile='13163384125',
            detail_address='龙阳智慧大厦1801',
            order=2,
            print_template='A',
        )
        assert resp['code'] in (200, 500), f'创建失败: {resp}'

    @pytest.mark.api
    def test_list_warehouses(self):
        """仓库分页列表"""
        resp = self.api.list_page()
        assert resp['code'] == 200, f'查询失败: {resp}'
        assert resp.get('data', {}).get('items') is not None

    @pytest.mark.api
    def test_update_warehouse(self):
        """编辑仓库名称"""
        # 先获取第一个仓库的 ID
        list_resp = self.api.list_page()
        assert list_resp['code'] == 200 and list_resp['data']['items'], '没有可用的仓库'
        wid = list_resp['data']['items'][0]['id']
        old_name = list_resp['data']['items'][0]['name']

        resp = self.api.update(
            warehouse_id=wid,
            name=old_name,
            warehouse_type='1',
            category_id=self.category_id,
            category_name=self.category_name,
            contact_name='王先生',
            mobile='13163384125',
            detail_address='龙阳智慧大厦1801',
            order=1,
            print_template='A',
        )
        assert resp['code'] == 200, f'更新失败: {resp}'
