from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        ''' 测试待办事项的默认字符串 '''
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        ''' 测试待办事项和列表的相关性 '''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        ''' 测试数据库约束不能保存空的待办事项 '''
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_string_representation(self):
        ''' 测试待办事项的字符串呈现 '''
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        ''' 测试Django的模型对象URL '''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_duplicate_items_are_invalid(self):
        ''' 测试重复提交待办事项的无效提示 '''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="bla")
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text="bla")
            item.full_clean()

    def test_CAN_save_item_to_different_lists(self):
        ''' 测试不同待办事项列表的重复内容可以提交成功 '''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="bla")
        item = Item(list=list2, text="bla")
        item.full_clean()

    def test_list_ordering(self):
        ''' 测试待办事项列表的顺序 '''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="i1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="3")
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3])
