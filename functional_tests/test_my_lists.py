from django.conf import settings

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        ''' 创建之前的认证会话 '''
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## 为了设定cookie, 我们要先访问网站
        # 而404页面是加载最快的
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path="/",
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        ''' 测试登录用户的待办事项列表已经被保存 '''
        # 小明是已登录用户
        self.create_pre_authenticated_session("200612453@qq.com")

        # 他访问首页，新建一个清单
        self.browser.get(self.live_server_url)
        self.add_list_item("上午睡小")
        self.add_list_item("下午大脑")
        first_list_url = self.browser.current_url

        # 他第一次看到"我的待办事项列表"链接
        self.browser.find_element_by_link_text("我的待办事项列表").click()

        # 他看到这个页面中有他创建的清单
        # 而且清单根据第一个待办事项命名
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("上午睡小")
        )
        self.browser.find_element_by_link_text("上午睡小").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # 他决定再建一个清单试试
        self.browser.get(self.live_server_url)
        self.add_list_item("晚上好啊")
        second_list_url = self.browser.current_url

        # 在"我的待办事项列表"页面，这个新建的清单也显示出来了
        self.browser.find_element_by_link_text("我的待办事项列表").click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("晚上好啊")
        )
        self.browser.find_element_by_link_text("晚上好啊").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # 他退出后，"我的待办事项列表"链接不见了
        self.browser.find_element_by_link_text("注销").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text("我的待办事项列表"),
            []
        ))
