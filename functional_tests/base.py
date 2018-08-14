from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from datetime import datetime
from django.conf import settings
import time
import os

from .server_tools import reset_database, create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


MAX_WAIT = 10
SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "screendumps"
)


def wait(fn):
    ''' 装饰器，不断调用指定的函数，并捕获常规的异常，直到超时为止 '''
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            self.live_server_url = "http://" + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()  # 测试失败自动截图
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def create_pre_authenticated_session(self, email):
        ''' 创建之前的认证会话 '''
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## 为了设定cookie, 我们要先访问网站
        # 而404页面是加载最快的
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path="/",
        ))

    def _test_has_failed(self):
        ''' 判断测试是否失败 '''
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        ''' 截图函数 '''
        filename = self._get_filename() + ".png"
        print("屏幕已截图到", filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        ''' 输出html '''
        filename = self._get_filename() + ".html"
        print("页面HTML保存到", filename)
        with open(filename, "w") as f:
            f.write(self.browser.page_source.decode("utf8"))

    def _get_filename(self):
        ''' 生成唯一的文件名，包含测试方法和测试类的名字以及时间戳 '''
        timestamp = datetime.now().isoformat().replace(":", ".")[:19]
        return "{folder}/{classname}.{method}-window{windowid}-{timestamp}"\
            .format(
                folder=SCREEN_DUMP_LOCATION,
                classname=self.__class__.__name__,
                method=self._testMethodName,
                windowid=self._windowid,
                timestamp=timestamp
            )

    def get_item_input_box(self):
        ''' 重构功能测试中需要定位id_new_item的输入框 '''
        return self.browser.find_element_by_id("id_text")

    def add_list_item(self, item_text):
        ''' 抽象在待办事项输入框中输入文本的操作 '''
        num_rows = len(self.browser.find_elements_by_css_selector(
            "#id_list_table tr"
        ))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f"{item_number}: {item_text}")

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        ''' 等待待办事项输入框出现在页面中 '''
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        ''' 等待登录成功 '''
        self.browser.find_element_by_link_text("注销")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        ''' 等待注销成功 '''
        self.browser.find_element_by_name("email")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)
