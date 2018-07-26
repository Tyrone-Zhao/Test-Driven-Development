from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 小明听说有一个很酷的待办事项在线应用，于是去看了应用首页
        self.browser.get("http://localhost:8000")

        # 小明注意到网页的标题和头部都包含"To-Do"这个词
        assert "To-Do" in self.browser.title,\
            "Browser title was " + self.browser.title

        # 应用邀请他输入一个待办事项

        # 他在一个文本框中输入了"购买孔雀羽毛"
        # 它的爱好是购买稀有的东西收藏起来

        # 他按回车键后，页面更新了
        # 待办事项表格中显示了"1: 购买孔雀羽毛"

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“把孔雀羽毛收藏到家里”
        # 他做事很有条理

        # 页面再次更新，他的清单中显示了这两个待办事项

        # 小明想知道这个网站会否记住他的清单
        # 他看到网站为他生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 他访问那个URL，发现他的待办事项列表还在

        # 他很满意，去睡觉了


if __name__ == "__main__":
    unittest.main()
