from django.test import TestCase

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
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

    def test_form_save_handles_saving_to_a_list(self):
        ''' 测试表单可以处理待办事项列表的存储操作 '''
        list_ = List.objects.create()
        form = ItemForm(data={"text": "do me"})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, "do me")
        self.assertEqual(new_item.list, list_)


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
