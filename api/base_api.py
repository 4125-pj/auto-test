"""
API 基类 - 封装 requests，提供统一的请求入口
"""
import requests
import json
from common.logger import logger
from config.settings import Config


class BaseAPI:
    """所有 API 对象的基类"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or Config.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        # 如果需要 Basic Auth，可以在这里设置
        # self.session.auth = (Config.API_USERNAME, Config.API_PASSWORD)

    def _log_request(self, method, url, **kwargs):
        logger.info('>>> %s %s', method.upper(), url)
        if kwargs.get('params'):
            logger.debug('  params: %s', kwargs['params'])
        if kwargs.get('json'):
            logger.debug('  body: %s', json.dumps(kwargs['json'], ensure_ascii=False))
        if kwargs.get('data'):
            logger.debug('  data: %s', kwargs['data'])

    def _log_response(self, resp: requests.Response):
        logger.info('<<< %s %s [%s]', resp.request.method, resp.url, resp.status_code)
        try:
            logger.debug('  body: %s', json.dumps(resp.json(), ensure_ascii=False))
        except Exception:
            logger.debug('  body: %s', resp.text[:500])

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """通用的请求方法"""
        url = self.base_url.rstrip('/') + '/' + path.lstrip('/')
        self._log_request(method, url, **kwargs)
        resp = self.session.request(method, url, **kwargs)
        self._log_response(resp)
        return resp

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request('GET', path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request('POST', path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request('PUT', path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request('DELETE', path, **kwargs)

    def close(self):
        self.session.close()
