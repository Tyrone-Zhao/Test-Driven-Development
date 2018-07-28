from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        ''' 判断访问URL后是否返回了正确的页面结果 '''
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        ''' 判断home页可以正确的接收一个待办事项的POST请求 '''
        response = self.client.post("/", data={"item_text": "一个新的待办事项"})
        self.assertIn("一个新的待办事项", response.content.decode())
        self.assertTemplateUsed(response, "home.html")
