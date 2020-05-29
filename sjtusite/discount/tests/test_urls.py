# 引入Django.test提供的测试模块，这里选用的是TestCase类作为单元测试的模板。
from django.test import TestCase

from django.urls import reverse,resolve
from discount.views import show_discount,discount_type,discount_detail,delete_discount

class TestUrls(TestCase):
    # 测试不同的视图函数返回的url是否正确
    def test_show_discount_url(self):
        url=reverse('discount:show_discount')
        self.assertEqual(resolve(url).func,show_discount)

    def test_discount_type_url(self):
        url=reverse('discount:discount_type',args=[1])
        self.assertEqual(resolve(url).func,discount_detail)

    def test_discount_detail_url(self):
        url=reverse('discount:discount_detail',args=[1])
        self.assertEqual(resolve(url).func,discount_detail)

    def test_delete_discount_url(self):
        url=reverse('discount:discount_delete',args=[1])
        self.assertEqual(resolve(url).func,delete_discount)