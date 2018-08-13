from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # 小明是已登录用户
        self.create_pre_authenticated_session("200612453@qq.com")
        ming_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(ming_browser))

        # 他的朋友小花也在使用这个清单网站
        hua_browser = webdriver.Chrome()
        self.addCleanup(lambda: quit_if_possible(hua_browser))
        self.browser = hua_browser
        self.create_pre_authenticated_session("tyrone-zhao@qq.com")

        # 小明访问首页，新建一个清单
        self.browser = ming_browser
        self.browser.get(self.live_server_url)
        self.add_list_item("获取帮助")

        # 他看到"分享这个清单"选项
        share_box = self.browser.find_element_by_css_selector(
            "input[name='sharee']"
        )
        self.assertEqual(
            share_box.get_attribute("placeholder"),
            "tyrone-zhao@qq.com"
        )
