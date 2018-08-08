from django.test import TestCase
from django.contrib import auth

from accounts.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):
    ''' 用户模型测试 '''

    def test_user_is_valid_with_email_only(self):
        ''' 测试只通过email创建用户是有效的 '''
        user = User(email="a@b.com")
        user.full_clean  # 不该抛出异常

    def test_email_is_primary_key(self):
        ''' 测试email作为主键 '''
        user = User(email="a@b.com")
        self.assertEqual(user.pk, "a@b.com")

    def test_no_problem_with_auth_login(self):
        ''' 测试django的认证登录功能正常 '''
        user = User.objects.create(email="200612453@qq.com")
        user.backend = ""
        request = self.client.request().wsgi_request
        auth.login(request, user)  # 不该抛出异常


class TokenModelTest(TestCase):
    ''' 令牌模型测试 '''

    def test_links_user_with_auto_generated_uid(self):
        ''' 测试测试提交相同email的用户uid相同 '''
        token1 = Token.objects.create(email="a@b.com")
        token2 = Token.objects.create(email="a@b.com")
        self.assertEqual(token1.uid, token2.uid)
