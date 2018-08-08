from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest


TEST_EMAIL = "200612453@qq.com"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # 小明访问这个很棒的超级列表网站
        # 第一次注意到导航栏中有"登录区域"
        # 看到要求输入电子邮件地址，他便输入了
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # 出现一条消息，告诉他邮件已经发出
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name("body").text
        ))

        # 他查看邮件，看到一条消息
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # 邮件中有个URL链接
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 他点了链接
        self.browser.get(url)

        # 他登录了
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Log out")
        )
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)
