from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

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

    def test_shared_with_response(self):
        ''' 测试清单能否响应shared_with.add方法 '''
        user = User.objects.create(email="tyrone-zhao@qq.com")
        list_ = List.objects.create()
        list_.shared_with.add(user.email)
        self.assertIn(user, list_.shared_with.all())

    def test_get_absolute_url(self):
        ''' 测试Django的模型对象URL '''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_create_new_creates_list_and_first_item(self):
        ''' 测试create_new方法创建了事项列表和首个待办事项显示 '''
        List.create_new(first_item_text="新的待办事项")
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "新的待办事项")
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        ''' 测试create_new方法可选是否保存所有者 '''
        user = User.objects.create()
        List.create_new(first_item_text="新的待办事项", owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owners(self):
        ''' 测试List模型可以保存owner属性 '''
        List(owner=User())  # 不该抛出异常

    def test_list_owner_is_optional(self):
        ''' 测试list的owner属性为可选 '''
        List().full_clean()  # 不该抛出异常

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

    def test_create_returns_new_list_object(self):
        ''' 测试create_new方法创建新列表后返回一个列表对象 '''
        returned = List.create_new(first_item_text="新的待办事项")
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
        ''' 测试待办事项列表的name属性返回第一个待办事项的文本 '''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="第一个待办事项")
        Item.objects.create(list=list_, text="第二个待办事项")
        self.assertEqual(list_.name, "第一个待办事项")
