from django.test import TestCase
from lists.models import Item


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


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "第一个列表项"
        first_item.save()

        second_item = Item()
        second_item.text = "第二个列表项"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "第一个列表项")
        self.assertEqual(second_saved_item.text, "第二个列表项")
