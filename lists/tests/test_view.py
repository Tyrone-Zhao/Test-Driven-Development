from django.test import TestCase
from django.utils.html import escape
from django.http import HttpRequest
import unittest
from unittest.mock import patch, Mock
from django.contrib.auth import get_user_model

User = get_user_model()

from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)
from lists.views import new_list


class ShareListTest(TestCase):
    ''' 测试分享列表的功能 '''

    def test_post_redirects_to_lists_page(self):
        ''' 测试发送重定向请求到列表页 '''
        sharee = User.objects.create(email="tyrone-zhao@qq.com")
        list_ = List.objects.create()
        response = self.client.post(
            f"/lists/{list_.id}/share",
            data={"sharee": "tyrone-zhao@qq.com"}
        )
        self.assertRedirects(response, list_.get_absolute_url())

    def test_sharing_a_list_via_post(self):
        ''' 测试通过post请求分享了一个列表 '''
        sharee = User.objects.create(email="tyrone-zhao@qq.com")
        list_ = List.objects.create()
        self.client.post(
            f"/lists/{list_.id}/share",
            {"sharee": "tyrone-zhao@qq.com"}
        )
        self.assertIn(sharee, list_.shared_with.all())


class HomePageTest(TestCase):
    ''' 测试主页的显示 '''

    def test_home_page_returns_correct_html(self):
        ''' 判断访问URL后是否返回了正确的页面结果 '''
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_uses_item_form(self):
        ''' 测试首页使用了待办事项的表单 '''
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)


class ListViewTest(TestCase):
    ''' 测试待办事项列表视图 '''

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

    def test_passes_correct_list_to_template(self):
        ''' 测试模版可以接收到正确的待办事项列表 '''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{ correct_list.id }/")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        ''' 测试能在已存在列表中正确的保存一个POST请求 '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "已存在列表中的一个新的待办事项"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "已存在列表中的一个新的待办事项")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        ''' 测试已存在列表中保存一个POST请求后，页面能够正确的重定向 '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "已存在列表中的一个新的待办事项"}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_displays_item_form(self):
        ''' 测试待办事项列表中的表单显示 '''
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        ''' 辅助方法，发送无效POST输入到/lists/id/ '''
        list_ = List.objects.create()
        return self.client.post(
            f"/lists/{list_.id}/",
            data={"text": ""}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        ''' 测试数据库不保存表单的无效输入 '''
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        ''' 测试表单无效输入返回待办事项模版 '''
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        ''' 测试无效输入后表单被正常传递给模版 '''
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        ''' 测试表单无效输入的页面错误提示 '''
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        ''' 判断重复事项校验返回的错误结果出现在list.html模版 '''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="textey")
        response = self.client.post(
            f"/lists/{list1.id}/",
            data={"text": "textey"}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)


class NewListViewIntegratedTest(TestCase):
    ''' 测试新建待办事项列表 '''

    def test_can_save_a_POST_request(self):
        ''' 判断list_new可以正确的传递一个待办事项的POST请求 '''
        self.client.post("/lists/new", data={"text": "一个新的待办事项"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "一个新的待办事项")

    def test_for_invalid_input_doesnt_save_but_shows_errors(self):
        ''' 测试无效输入在首页显示错误消息 '''
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        ''' 测试用户登录后创建待办事项后，当前列表回归属于当前用户 '''
        user = User.objects.create(email="200612453@qq.com")
        self.client.force_login(user)
        self.client.post("/lists/new", data={"text": "新事项"})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class MyListsTest(TestCase):
    ''' 我的列表页面测试 '''

    def test_my_lists_url_renders_my_lists_template(self):
        ''' 测试我的待办事项列表url能渲染对应的模版 '''
        User.objects.create(email="200612453@qq.com")
        response = self.client.get("/lists/users/200612453@qq.com/")
        self.assertTemplateUsed(response, "my_lists.html")

    def test_passes_correct_owner_to_template(self):
        ''' 测试传递了正确的待办事项列表所有者，到模版 '''
        User.objects.create(email="200612453@qq.com")
        correct_user = User.objects.create(email="jiaowoyuluo@vip.qq.com")
        response = self.client.get("/lists/users/jiaowoyuluo@vip.qq.com/")
        self.assertEqual(response.context["owner"], correct_user)


@patch("lists.views.NewListForm")
class NewListViewUnitTest(unittest.TestCase):
    ''' 新的列表视图测试类 '''

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST["text"] = "新的待办事项"
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        ''' 测试列表视图传递POST数据到新列表表单 '''
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        ''' 测试表单有效时对所有者的保存功能 '''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch("lists.views.redirect")
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mockNewListForm
    ):
        ''' 测试表单有效时视图会重定向到一个显示刚刚提交的表单的页面 '''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(
            str(mock_form.save().get_absolute_url.return_value))

    @patch("lists.views.render")
    def test_renders_home_template_with_form_if_form_invalid(
        self, mock_render, mockNewListForm
    ):
        ''' 测试如果表单无效，那么返回主页模版 '''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, "home.html", {"form": mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        ''' 测试form内容无效时不应该保存 '''
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)
