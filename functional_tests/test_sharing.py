from selenium import webdriver
from time import sleep

from .base import FunctionalTest
from .list_page import ListPage
from .my_list_page import MyListPage


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
        self.browser.get(self.live_server_url)

        # 他的朋友小花也在使用这个清单网站
        hua_browser = webdriver.Chrome()
        self.browser = hua_browser
        self.addCleanup(lambda: quit_if_possible(hua_browser))
        self.create_pre_authenticated_session("tyrone-zhao@qq.com")
        self.browser.get(self.live_server_url)

        # 小明访问首页，新建一个清单
        self.browser = ming_browser
        list_page = ListPage(self).add_list_item("获取帮助")

        # 他看到"分享这个清单"选项
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute("placeholder"),
            "your-friend@example.com"
        )

        # 他分享自己的清单后，页面更新了
        # 提示已经分享给小花
        ListPage(self).share_list_with("tyrone-zhao@qq.com")

        # 现在小花在他的浏览器中访问清单页面
        self.browser = hua_browser
        MyListPage(self).go_to_my_lists_page()

        # 在清单页面，小花看到这个清单属于小明
        self.wait_for(lambda: self.assertIn(
            "200612453@qq.com",
            list_page.get_list_owner(),
        ))

        # 小花查看了这个清单
        self.browser.find_element_by_link_text("获取帮助").click()

        # 他在这个清单中添加一个待办事项
        list_page.add_list_item("你好 小明!")

        # 小明刷新页面后，看到小花添加的内容
        ming_browser.refresh()
        list_page.wait_for_row_in_list_table("你好 小明!", 2)
