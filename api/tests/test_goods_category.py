"""
商品分类接口测试用例
"""
import pytest
from api.api_objects.category_api import CategoryAPI


class TestGoodsCategory:
    """商品分类测试"""

    @pytest.mark.api
    def test_create_category(self, category_api: CategoryAPI):
        """新增商品分类"""
        resp = category_api.save_category(name='A类商品', status='1', order=1)
        assert resp['code'] in (200, 201), f'异常响应: {resp}'

    @pytest.mark.api
    def test_list_categories(self, category_api: CategoryAPI):
        """商品分类分页列表"""
        resp = category_api.list_categories()
        assert resp['code'] == 200, f'查询失败: {resp}'
        assert 'rows' in resp or 'data' in resp
