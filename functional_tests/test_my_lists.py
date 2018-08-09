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
        email = "200612453@qq.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # 小明是已登录用户
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
