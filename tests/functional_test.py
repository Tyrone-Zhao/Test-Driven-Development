from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        time.sleep(10)
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        ''' 辅助方法 '''
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 小明听说有一个很酷的待办事项在线应用，于是去看了应用首页
        self.browser.get("http://localhost:8000")

        # 小明注意到网页的标题和头部都包含"To-Do"这个词
        assert "待办事项" in self.browser.title,\
            "Browser title was " + self.browser.title

        # 应用邀请他输入一个待办事项
        inputbox = self.browser.find_elements_by_id("id_new_item")
        self.assertEqual(
            inputbox[0].get_attribute("placeholder"),
            "输入一个待办事项"
        )

        # 他在一个文本框中输入了"购买孔雀羽毛"
        # 它的爱好是购买稀有的东西收藏起来
        inputbox[0].send_keys("购买孔雀羽毛")

        # 他按回车键后，页面更新了
        # 待办事项表格中显示了"1: 购买孔雀羽毛"
        inputbox[0].send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table("1: 购买孔雀羽毛")

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“把孔雀羽毛收藏到家里”
        # 他做事很有条理
        inputbox[0] = self.browser.find_element_by_id("id_new_item")
        inputbox[0].send_keys("把孔雀羽毛收藏到家里")
        inputbox[0].send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面再次更新，他的清单中显示了这两个待办事项
        self.check_for_row_in_list_table("1: 购买孔雀羽毛")
        self.check_for_row_in_list_table("2: 把孔雀羽毛收藏到家里")

        # 小明想知道这个网站会否记住他的清单
        # 他看到网站为他生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能
        self.fail("Finish the test")

        # 他访问那个URL，发现他的待办事项列表还在

        # 他很满意，去睡觉了


if __name__ == "__main__":
    unittest.main()
