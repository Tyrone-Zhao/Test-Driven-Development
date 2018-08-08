from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import os


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self):
        time.sleep(10)
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        ''' 重构后的辅助方法 '''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        ''' 函数式编程的等待方法 '''
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        ''' 重构功能测试中需要定位id_new_item的输入框 '''
        return self.browser.find_element_by_id("id_text")

    def wait_to_be_logged_in(self, email):
        ''' 等待登录成功 '''
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("注销")
        )
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        ''' 等待注销成功 '''
        self.wait_for(
            lambda: self.browser.find_element_by_name("email")
        )
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)
