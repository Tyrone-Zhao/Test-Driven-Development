from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 小明访问首页，不小心提交了一个空待办事项
        # 输入框中没有输入内容，他就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 首页刷新了，显示一个错误消息
        # 提示待办事项不能为空
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,
            "You can't have an empty list item"))

        # 他输入一些文字，然后再次提交，这次没问题了
        self.get_item_input_box().send_keys("买牛奶")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 买牛奶")

        # 他有点调皮，又提交了一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 在清单页面他看到了一个类似的错误消息
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,
            "You can't have an empty list item"))

        # 输入文字之后就没问题了
        self.get_item_input_box().send_keys("做壶茶")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 买牛奶")
        self.wait_for_row_in_list_table("2: 做壶茶")
