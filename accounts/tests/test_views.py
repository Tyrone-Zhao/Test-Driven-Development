from django.test import TestCase
from unittest.mock import patch, call

from accounts.models import Token
import accounts.views


class SendLoginEmailViewTest(TestCase):
    ''' 发送登录邮件的视图测试 '''

    def test_redirects_to_home_page(self):
        ''' 测试发送邮件后重定向到首页 '''
        response = self.client.post("/accounts/send_login_email", data={
            "email": "200612453@qq.com"
        })
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        ''' 测试post请求可以成功发送邮件 '''
        self.client.post("/accounts/send_login_email", data={
            "email": "200612453@qq.com"
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "你的超级表登录链接")
        self.assertEqual(from_email, "tyrone-zhao@qq.com")
        self.assertEqual(to_list, ["200612453@qq.com"])

    def test_adds_success_message(self):
        ''' 测试发送邮件成功的消息 '''
        response = self.client.post("/accounts/send_login_email", data={
            "email": "200612453@qq.com"
        }, follow=True)
        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "请在你的邮箱中查收邮件，我们会把登录链接发送给你。"
        )
        self.assertEqual(message.tags, "success")


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    ''' 登录视图测试 '''

    def test_redirects_to_home_page(self, mock_auth):
        ''' 测试登录后重定向到首页 '''
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")

    def test_create_token_associated_with_email(self, mock_auth):
        ''' 测试在数据库中为对应的邮件地址创建了token '''
        self.client.post("/accounts/send_login_email", data={
            "email": "200612453@qq.com"
        })
        token = Token.objects.first()
        self.assertEqual(token.email, "200612453@qq.com")

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail,
                                                 mock_auth):
        ''' 测试含有token的登录链接被发送到指定邮件地址 '''
        self.client.post("/accounts/send_login_email", data={
            "email": "200612453@qq.com"
        })

        token = Token.objects.first()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        ''' 测试认证时所调用的参数 '''
        self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid="abcd123")
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        ''' 
            测试authenticate是否返回了一个用户，以供auth.login方法使用
            测试login调用的参数是不是视图收到的请求对象
        '''
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        ''' 测试未认证的用户不能登录 '''
        mock_auth.authenticate.return_value = None
        self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(mock_auth.login.called, False)
