from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import time
import poplib
import base64

from .base import FunctionalTest


SUBJECT = "你的超级表登录链接"


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        ''' 用POP3客户端获取真实邮件 '''
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL("pop.qq.com")
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ["QQ_PASSWORD"])
            while time.time() - start < 60:
                # 获取最新的10封邮件
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print("getting msg", i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode() for l in lines]
                    new_lines = []
                    for l in lines:
                        if "Subject" in l and "Jenkins" not in l:
                            print(l)
                            try:
                                subject = base64.b64decode(l[19:]).decode()
                            except:
                                subject = base64.b64decode(
                                    subject[11:-4]).decode()
                            if subject == SUBJECT:
                                email_id = i
                                new_lines.append(f"Subject: {subject}")
                        else:
                            new_lines.append(l)
                            body = "\n".join(new_lines)
                    print(body)
                    return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # 小明访问这个很棒的超级列表网站
        # 第一次注意到导航栏中有"登录区域"
        # 看到要求输入电子邮件地址，他便输入了
        if self.staging_server:
            test_email = "jiaowoyuluo@vip.qq.com"
        else:
            test_email = "200612453@qq.com"

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # 出现一条消息，告诉他邮件已经发出
        self.wait_for(lambda: self.assertIn(
            "请在你的邮箱中查收邮件",
            self.browser.find_element_by_tag_name("body").text
        ))

        # 他查看邮件，看到一条消息
        body = self.wait_for_email(test_email, SUBJECT)

        # 邮件中有个URL链接
        self.assertIn("请使用此链接登录", body)
        url_search = re.search(r"http://.+/.+$", body)
        if not url_search:
            self.fail(f"邮件内容中未发现登录链接:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 他点了链接
        self.browser.get(url)

        # 他登录了！
        self.wait_to_be_logged_in(email=test_email)

        # 现在他要退出
        self.browser.find_element_by_link_text("注销").click()

        # 他退出了
        self.wait_to_be_logged_out(email=test_email)

        # 他通过输入邮件地址的方式再次登录了
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # 出现一条消息，告诉他邮件已经发出
        self.wait_for(lambda: self.assertIn(
            "请在你的邮箱中查收邮件",
            self.browser.find_element_by_tag_name("body").text
        ))

        # 他查看邮件，看到一条消息
        body = self.wait_for_email(test_email, SUBJECT)

        # 邮件中有个URL链接
        self.assertIn("请使用此链接登录", body)
        url_search = re.search(r"http://.+/.+$", body)
        if not url_search:
            self.fail(f"邮件内容中未发现登录链接:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 他点了链接
        self.browser.get(url)

        # 他登录了！
        self.wait_to_be_logged_in(email=test_email)

        # 现在他要退出
        self.browser.find_element_by_link_text("注销").click()

        # 他退出了
        self.wait_to_be_logged_out(email=test_email)
