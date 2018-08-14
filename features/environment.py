from selenium import webdriver
from time import sleep


def before_all(context):
    context.browser = webdriver.Chrome()


def after_all(context):
    # sleep(10)
    context.browser.quit()


def before_feature(context, feature):
    pass
