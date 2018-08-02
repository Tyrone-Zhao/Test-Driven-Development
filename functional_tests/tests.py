from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time


MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

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

    def test_can_start_a_list_for_one_user(self):
        # 小明听说有一个很酷的待办事项在线应用，于是去看了应用首页
        self.browser.get(self.live_server_url)

        # 小明注意到网页的标题和头部都包含"To-Do"这个词
        assert "待办事项" in self.browser.title,\
            "Browser title was " + self.browser.title

        # 应用邀请他输入一个待办事项
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "输入一个待办事项"
        )

        # 他在一个文本框中输入了"购买孔雀羽毛"
        # 它的爱好是购买稀有的东西收藏起来
        inputbox.send_keys("购买孔雀羽毛")

        # 他按回车键后，页面更新了
        # 待办事项表格中显示了"1: 购买孔雀羽毛"
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: 购买孔雀羽毛")

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“把孔雀羽毛收藏到家里”
        # 他做事很有条理
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("把孔雀羽毛收藏到家里")
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，他的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table("1: 购买孔雀羽毛")
        self.wait_for_row_in_list_table("2: 把孔雀羽毛收藏到家里")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 小明新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("购买孔雀羽毛")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 购买孔雀羽毛")

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
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("买牛奶")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 买牛奶")

        # 小花获得了他的唯一URL
        hua_list_url = self.browser.current_url
        self.assertRegex(hua_list_url, "/lists/.+")
        self.assertNotEqual(hua_list_url, ming_list_url)

        # 这个页面还是没有小明的清单
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("购买孔雀羽毛", page_text)
        self.assertIn("买牛奶", page_text)

        # 两人都很满意，然后去睡觉了

    def test_layout_and_styling(self):
        # 小明访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 他看到输入框完美地居中显示
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )

        # 他新建了一个清单，看到输入框仍完美地居中显示
        inputbox.send_keys("测试")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 测试")
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )
