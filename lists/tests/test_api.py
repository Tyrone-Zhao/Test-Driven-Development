import json
from django.test import TestCase

from lists.models import List, Item
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR


class ListAPITest(TestCase):
    base_url = "/api/lists/{}/"

    def test_get_returns_json_200(self):
        ''' 测试get接口返回了200的json '''
        list_ = List.objects.create()
        response = self.client.get(self.base_url.format(list_.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

    def test_get_returns_items_for_correct_list(self):
        ''' 测试api返回指定清单的所有待办事项 '''
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text="待办事项1")
        our_list = List.objects.create()
        item1 = Item.objects.create(list=our_list, text="待办事项1")
        item2 = Item.objects.create(list=our_list, text="待办事项2")
        response = self.client.get(self.base_url.format(our_list.id))
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            [
                {"id": item1.id, "text": item1.text},
                {"id": item2.id, "text": item2.text}
            ]
        )

    def test_POSTing_a_new_item(self):
        ''' 测试通过post请求创建一个新的待办事项 '''
        list_ = List.objects.create()
        response = self.client.post(
            self.base_url.format(list_.id),
            {"text": "新的待办事项"},
        )
        self.assertEqual(response.status_code, 201)
        new_item = list_.item_set.get()
        self.assertEqual(new_item.text, "新的待办事项")

    def post_empty_input(self):
        ''' post方法发送空数据 '''
        list_ = List.objects.create()
        return self.client.post(
            self.base_url.format(list_.id),
            data={"text": ""}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        ''' 测试无效输入不会被保存 '''
        self.post_empty_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_return_error_code(self):
        ''' 测试无效输入返回错误状态码 '''
        response = self.post_empty_input()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            {"error": EMPTY_ITEM_ERROR}
        )

    def test_duplicate_items_error(self):
        ''' 测试提交重复事项会返回错误码 '''
        list_ = List.objects.create()
        self.client.post(
            self.base_url.format(list_.id), data={"text": "thing"}
        )
        response = self.client.post(
            self.base_url.format(list_.id), data={"text": "thing"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode("utf8")),
            {"error": DUPLICATE_ITEM_ERROR}
        )
