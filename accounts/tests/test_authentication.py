from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User

user = get_user_model()


class AuthenticateTest(TestCase):
    ''' 认证测试类 '''

    def test_returns_None_if_no_such_token(self):
        ''' 测试数据库无指定token返回None '''
        result = PasswordlessAuthenticationBackend().authenticate(
            "没有指定token"
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        ''' 测试如果token存在, 用户不存在时，返回新建用户 '''
        email = "200612453@qq.com"
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        ''' 测试如果token存在，用户也存在时，返回已存在的用户 '''
        email = "200612453@qq.com"
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    ''' 获取用户测试 '''

    def test_gets_user_by_email(self):
        ''' 测试根据电子邮件地址获取用户 '''
        User.objects.create(email="tyrone-zhao@qq.com")
        desired_user = User.objects.create(email="200612453@qq.com")
        found_user = PasswordlessAuthenticationBackend().get_user(
            "200612453@qq.com"
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        ''' 测试如果根据电子邮件地址获取不到用户则返回None '''
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user("200612453@qq.com")
        )
