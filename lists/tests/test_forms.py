from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class ItemFormTest(TestCase):

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
