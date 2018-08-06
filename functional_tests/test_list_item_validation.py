from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 小明访问首页，不小心提交了一个空待办事项
        # 输入框中没有输入内容，他就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器截获了请求
        # 清单页面不会加载
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            "#id_text:invalid"))

        # 他在待办事项中输入了一些文字
        # 错误消失了
        self.get_item_input_box().send_keys("买牛奶")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            "#id_text:valid"
        ))

        # 现在能提交了
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 买牛奶")

        # 他打算再提交一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器这次也不会放行
        self.wait_for_row_in_list_table("1: 买牛奶")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            "#id_text:invalid"))

        # 输入一些文字后就能纠正这个错误
        self.get_item_input_box().send_keys("做壶茶")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            "#id_text:valid"))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 买牛奶")
        self.wait_for_row_in_list_table("2: 做壶茶")

    def test_cannot_add_duplicate_items(self):
        # 小明访问首页，新建一个清单
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("买双鞋")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 买双鞋")

        # 他不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys("买双鞋")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 他看到一条有帮助的错误消息
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,
            "You've already got this in your list"))
