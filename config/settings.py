"""
项目全局配置
从 .env 文件读取环境变量，提供统一的配置接口
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent

# 加载 .env 文件
load_dotenv(ROOT_DIR / '.env', encoding='utf-8')


class Config:
    """所有配置项"""

    # ---------- 被测系统 ----------
    BASE_URL = os.getenv('BASE_URL', 'http://localhost')
    PROJECT_NAME = os.getenv('PROJECT_NAME', '自动化测试')

    # ---------- API ----------
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost/api')
    API_USERNAME = os.getenv('API_USERNAME', '')
    API_PASSWORD = os.getenv('API_PASSWORD', '')

    # ---------- Playwright ----------
    BROWSER = os.getenv('BROWSER', 'chromium')   # chromium / firefox / webkit
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30000'))

    # ---------- UI 登录 ----------
    UI_BASE_URL = os.getenv('UI_BASE_URL', 'http://localhost')
    UI_USERNAME = os.getenv('UI_USERNAME', '')
    UI_PASSWORD = os.getenv('UI_PASSWORD', '')

    # ---------- 报告 ----------
    REPORT_TITLE = os.getenv('REPORT_TITLE', '自动化测试报告')

    # ---------- 路径 ----------
    REPORT_DIR = ROOT_DIR / 'reports'
    LOG_DIR = ROOT_DIR / 'logs'
    DATA_DIR = ROOT_DIR / 'data'
    SCREENSHOT_DIR = ROOT_DIR / 'screenshots'


# 确保目录存在
for _dir in [Config.REPORT_DIR, Config.LOG_DIR, Config.DATA_DIR, Config.SCREENSHOT_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)
