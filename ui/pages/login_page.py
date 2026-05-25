"""
登录页面 Page Object (Playwright)
"""
import time
from ui.base_page import BasePage
from common.logger import logger


class LoginPage(BasePage):
    """登录页面"""

    # 页面元素定位
    _username_input = 'input[name="username"]'
    _password_input = 'input[name="password"]'
    _login_btn = 'button[aria-label="login"]'
    _slider = '[name="captcha-action"]'
    _track = '[name="captcha"]'

    def login(self, username: str, password: str):
        """输入用户名密码"""
        self.input_text(self._username_input, username)
        self.input_text(self._password_input, password)

    def slide_verify(self, max_retries: int = 2):
        """拖拽滑块验证（失败自动重试）"""
        import random

        for attempt in range(1, max_retries + 2):
            logger.info('Slide verify: attempt %d', attempt)
            track = self.page.locator(self._track)
            box = track.bounding_box()
            if not box:
                raise Exception('Slider track not found')

            start_x = box['x'] + 20
            start_y = box['y'] + box['height'] / 2 + random.uniform(-2, 2)
            end_x = box['x'] + box['width'] - 5
            steps = 100

            # 按住滑块拖动
            self.page.mouse.move(start_x, start_y)
            self.page.mouse.down()
            for i in range(1, steps + 1):
                x = start_x + (end_x - start_x) * i / steps
                self.page.mouse.move(x, start_y + random.uniform(-1, 1))
                time.sleep(0.008 + random.uniform(0, 0.005))
            time.sleep(0.1)
            self.page.mouse.up()

            # 验证滑块是否到达终点
            left_value = self.page.evaluate(
                "document.querySelector('[name=\"captcha-action\"]').style.left"
            )
            logger.info('Slider left after attempt %d: %s', attempt, left_value)

            if left_value and 'px' in left_value and int(left_value.replace('px', '')) > 200:
                logger.info('Slide verify: passed on attempt %d', attempt)
                return

            time.sleep(0.5)

        logger.warning('Slide verify: all attempts failed, proceeding anyway')

    def click_login(self):
        """点击登录按钮"""
        self.click(self._login_btn)

    def wait_for_success(self, timeout: int = 20000):
        """等待登录成功跳转"""
        self.page.wait_for_url('**/dashboard/**', timeout=timeout)
