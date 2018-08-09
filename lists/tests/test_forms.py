from django.test import TestCase
from unittest.mock import patch, Mock
import unittest

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm, NewListForm
)
from lists.models import Item, List


class ItemFormTest(TestCase):
    ''' 待办事项表单测试 '''

    # def test_form_renders_text_input(self):
    #     ''' 显示表单输入框的渲染内容 '''
    #     form = ItemForm()
    #     self.fail(form.as_p())

    def test_form_item_input_has_placeholder_and_css_classes(self):
        ''' 测试表单输入框的属性包含placeholder和class '''
        form = ItemForm()
        self.assertIn('placeholder="输入一个待办事项"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        ''' 测试表单对空元素的校验 '''
        form = ItemForm(data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["text"],
            [EMPTY_ITEM_ERROR]
        )


class NewListFormTest(unittest.TestCase):
    ''' 新的待办事项列表表单测试 '''

    @patch("lists.forms.List.create_new")
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self, mock_List_create_new
    ):
        ''' 测试从未认证的用户表单请求中保存新的待办事项列表 '''
        user = Mock(is_authenticated=False)
        form = NewListForm(data={"text": "新的待办事项"})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text="新的待办事项"
        )

    @patch("lists.forms.List.create_new")
    def test_save_creates_new_list_with_owner_if_user_authenticated(
        self, mock_List_create_new
    ):
        ''' 测试从已认证的用户表单请求中保存新的待办事项列表 '''
        user = Mock(is_authenticated=True)
        form = NewListForm(data={"text": "新的待办事项"})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text="新的待办事项", owner=user
        )

    @patch("lists.forms.List.create_new")
    def test_save_returns_new_list_object(self, mock_List_create_new):
        ''' 测试create_new方法调用后，返回一个新的待办事项列表对象 '''
        user = Mock(is_authenticated=True)
        form = NewListForm(data={"text": "新的待办事项"})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)


class ExistingListItemFormTest(TestCase):
    ''' 已存在的列表表单测试 '''

    def test_form_renders_item_text_input(self):
        ''' 测试表单渲染待办事项的文本 '''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="输入一个待办事项"', form.as_p())

    def test_form_validation_for_blank_items(self):
        ''' 测试表单对空待办事项的校验 '''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        ''' 测试表单对重复待办事项的校验 '''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="no twins!")
        form = ExistingListItemForm(for_list=list_, data={"text": "no twins!"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        ''' 测试表单存储 '''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={"text": "hi"})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
