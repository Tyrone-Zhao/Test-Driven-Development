from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        ''' 判断访问URL后是否返回了正确的页面结果 '''
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        ''' 测试数据库可以保存和获取待办事项 '''
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "第一个待办事项"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "第二个待办事项"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "第一个待办事项")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "第二个待办事项")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        ''' 测试清单视图使用了和首页不同的模版 '''
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_only_items_for_that_list(self):
        ''' 测试应用首页可以显示创建过的待办事项 '''
        correct_list = List.objects.create()
        Item.objects.create(text="事项1", list=correct_list)
        Item.objects.create(text="事项2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="其他待办事项1", list=other_list)
        Item.objects.create(text="其他待办事项2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "事项1")
        self.assertContains(response, "事项2")
        self.assertNotContains(response, "其他待办事项1")
        self.assertNotContains(response, "其他待办事项2")


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        ''' 判断list_new可以正确的传递一个待办事项的POST请求 '''
        self.client.post("/lists/new", data={"item_text": "一个新的待办事项"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "一个新的待办事项")

    def test_redirects_after_POST(self):
        ''' 判断处理完POST请求后可以正确的重定向到指定新建清单的URL '''
        response = self.client.post("/lists/new",
                                    data={"item_text": "一个新的待办事项"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        ''' 测试能在已存在列表中正确的保存一个POST请求 '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "已存在列表中的一个新的待办事项"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "已存在列表中的一个新的待办事项")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        ''' 测试已存在列表中保存一个POST请求后，页面能够正确的重定向 '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "已存在列表中的一个新的待办事项"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
