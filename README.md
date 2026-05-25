# 自动化测试项目

## 技术栈

- **UI自动化**: Selenium + webdriver-manager
- **接口自动化**: requests + pytest
- **测试报告**: pytest-html

## 项目结构

```
├── config/           # 配置文件
│   └── settings.py   # 全局配置（从 .env 读取）
├── api/              # API 自动化
│   ├── base_api.py   # 请求基类
│   ├── api_objects/  # API 对象层（按模块）
│   └── tests/        # 接口测试用例
├── ui/               # UI 自动化
│   ├── base_page.py  # 页面基类
│   ├── pages/        # Page Objects（按页面）
│   ├── conftest.py   # 浏览器 fixture
│   └── tests/        # UI 测试用例
├── common/           # 公共模块
│   ├── logger.py     # 日志
│   └── utils.py      # 工具函数
├── .env              # 环境配置（Git ignored）
├── pytest.ini        # Pytest配置
└── requirements.txt  # 依赖包
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 修改配置

编辑 `.env` 文件，填写被测系统的实际地址和账号密码。

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行 API 测试
pytest api/tests/

# 运行 UI 测试
pytest ui/tests/

# 运行冒烟测试
pytest -m smoke

# 生成 HTML 报告
pytest --html=reports/report.html --self-contained-html

# 多线程运行
pytest -n 4
```

## 编写测试

### API 测试

```python
# 1. 在 api/api_objects/ 中创建 API 对象
class MyAPI(BaseAPI):
    def get_data(self):
        return self.get('/path')

# 2. 在 api/tests/ 中编写测试
class TestMyAPI:
    def test_get_data(self):
        api = MyAPI()
        resp = api.get_data()
        assert resp['code'] == 0
```

### UI 测试

```python
# 1. 在 ui/pages/ 中创建 Page Object
class MyPage(BasePage):
    _btn = (By.ID, 'submit')
    def click_btn(self):
        self.click(self._btn)

# 2. 在 ui/tests/ 中编写测试（使用 driver fixture）
class TestMyPage:
    def test_click(self, driver):
        page = MyPage(driver)
        page.click_btn()
```
