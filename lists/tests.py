from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        ''' 判断访问URL后是否返回了正确的页面结果 '''
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        ''' 判断home页可以正确的传递一个待办事项的POST请求 '''
        response = self.client.post("/", data={"item_text": "一个新的待办事项"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "一个新的待办事项")

    def test_redirects_after_POST(self):
        ''' 判断处理完POST请求后可以正确的重定向 '''
        response = self.client.post("/", data={"item_text": "一个新的待办事项"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_only_saves_items_when_necessary(self):
        ''' 判断请求只保存需要的待办事项 '''
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_display_all_list_items(self):
        ''' 
            测试页面table可以显示多个待办事项, 
            空行表明:设置-使用-断言的单元测试典型结构 
        '''
        Item.objects.create(text="事项1")
        Item.objects.create(text="事项2")

        response = self.client.get("/")

        self.assertIn("事项1", response.content.decode())
        self.assertIn("事项2", response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        ''' 测试数据库保存和获取待办事项 '''
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
