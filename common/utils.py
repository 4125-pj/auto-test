"""
工具函数
"""
import json
import time
from pathlib import Path
from config.settings import Config


def read_json(file_name: str) -> dict:
    """从 data 目录读取 JSON 文件"""
    file_path = Config.DATA_DIR / file_name
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def timestamp() -> str:
    """返回当前时间戳字符串 yyyyMMdd_HHmmss"""
    return time.strftime('%Y%m%d_%H%M%S')


def screenshot_path(name: str) -> str:
    """生成截图保存路径"""
    return str(Config.SCREENSHOT_DIR / f'{name}_{timestamp()}.png')
