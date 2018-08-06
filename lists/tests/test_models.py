from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


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

    def test_cannot_save_empty_list_items(self):
        ''' 测试数据库约束不能保存空的待办事项 '''
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
