from behave import given, when, then
from functional_tests.management.commands.create_session import \
    create_pre_authenticated_session
from django.conf import settings
from functional_tests.base import wait
from selenium.webdriver.common.keys import Keys


@wait
def wait_for_list_item(context, item_text):
    context.test.assertIn(
        item_text,
        context.browser.find_element_by_css_selector("#id_list_table").text
    )


@given(u': 我是一个已登录用户')
def given_i_am_logged_in(context):
    session_key = create_pre_authenticated_session(email="200612453@qq.com")
    # 为了设定cookie，我们要先访问网站
    # 而404页面是加载最快的
    context.browser.get(context.get_url("/404_no_such_url/"))
    context.browser.add_cookie(dict(
        name=settings.SESSION_COOKIE_NAME,
        value=session_key,
        path="/",
    ))


@when(u'<: 我在待办事项列表中创建第一个待办事项“{first_item_text}”')
def create_a_list(context, first_item_text):
    context.browser.get(context.get_url("/"))
    context.browser.find_element_by_id("id_text").send_keys(first_item_text)
    context.browser.find_element_by_id("id_text").send_keys(Keys.ENTER)
    wait_for_list_item(context, first_item_text)


@when(u'< 我又增加了一个待办事项“{item_text}”')
def add_an_item(context, item_text):
    context.browser.find_element_by_id("id_text").send_keys(item_text)
    context.browser.find_element_by_id("id_text").send_keys(Keys.ENTER)
    wait_for_list_item(context, item_text)


@when(u'< 我又在新的列表中创建了一个待办事项“{new_item_text}”')
def add_a_new_item(context, new_item_text):
    given_i_am_logged_in(context)
    create_a_list(context, new_item_text)


@then(u'<: 我在页面中发现了“{link_text}”超链接')
@wait
def see_a_link(context, link_text):
    context.browser.find_element_by_link_text(link_text)


@when(u'<: 我点击“{link_text}”超链接后')
def click_link(context, link_text):
    context.browser.find_element_by_link_text(link_text).click()


@then(u'<: 我看到了“{item_text}”的超链接')
@wait
def see_the_link(context, item_text):
    see_a_link(context, item_text)


@when(u'<: 我点击“{link_text}”的超链接后')
def click_the_link(context, link_text):
    click_link(context, link_text)


@then(u'<: 我进入了“{first_item_text}”的待办事项列表页面')
@wait
def on_list_page(context, first_item_text):
    first_row = context.browser.find_element_by_css_selector(
        '#id_list_table tr:first-child'
    )
    expected_row_text = '1: ' + first_item_text
    context.test.assertEqual(first_row.text, expected_row_text)
