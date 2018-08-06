from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR


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
