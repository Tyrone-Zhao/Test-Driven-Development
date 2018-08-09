from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # 小明听说有一个很酷的待办事项在线应用，于是去看了应用首页
        self.browser.get(self.live_server_url)

        # 小明注意到网页的标题和头部都包含"To-Do"这个词
        assert "待办事项" in self.browser.title,\
            "Browser title was " + self.browser.title

        # 应用邀请他输入一个待办事项
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "输入一个待办事项"
        )

        # 他在一个文本框中输入了"购买孔雀羽毛"
        # 它的爱好是购买稀有的东西收藏起来
        # 他按回车键后，页面更新了
        # 待办事项表格中显示了"1: 购买孔雀羽毛"
        self.add_list_item("购买孔雀羽毛")

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“把孔雀羽毛收藏到家里”
        # 他做事很有条理
        # 页面再次更新，他的清单中显示了这两个待办事项
        self.add_list_item("把孔雀羽毛收藏到家里")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 小明新建一个待办事项清单
        self.browser.get(self.live_server_url)
        self.add_list_item("购买孔雀羽毛")

        # 他注意到清单有个唯一的URL
        ming_list_url = self.browser.current_url
        self.assertRegex(ming_list_url, "/lists/.+")

        # 现在一名叫做小花的新用户访问了网站

        # 我们使用一个新浏览器会话
        # 确保小明的信息不回从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 小花访问首页
        # 页面中看不到小明的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("购买孔雀羽毛", page_text)
        self.assertNotIn("把孔雀羽毛收藏到家里", page_text)

        # 小花输入一个新的待办事项，新建一个清单
        # 他不想小明一样兴趣盎然
        inputbox = self.get_item_input_box()
        self.add_list_item("买牛奶")

        # 小花获得了他的唯一URL
        hua_list_url = self.browser.current_url
        self.assertRegex(hua_list_url, "/lists/.+")
        self.assertNotEqual(hua_list_url, ming_list_url)

        # 这个页面还是没有小明的清单
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("购买孔雀羽毛", page_text)
        self.assertIn("买牛奶", page_text)

        # 两人都很满意，然后去睡觉了
