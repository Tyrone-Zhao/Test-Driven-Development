from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 小明访问首页，不小心提交了一个空待办事项
        # 输入框中没有输入内容，他就按下了回车键

        # 首页刷新了，显示一个错误消息
        # 提示待办事项不能为空

        # 他输入一些文字，然后再次提交，这次没问题了

        # 他有点调皮，又提交了一个空待办事项

        # 在清单页面他看到了一个类似的错误消息

        # 输入文字之后就没问题了
        self.fail("write me!")
