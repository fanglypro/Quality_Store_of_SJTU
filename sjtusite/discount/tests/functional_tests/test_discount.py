from selenium import webdriver
from discount.models import Discount
from shop.models import Shop,ShopType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestDiscount(StaticLiveServerTestCase):
    # 添加数据
    def setUp(self):
        self.browser = webdriver.Chrome('discount/tests/functional_tests/chromedriver.exe')
        shopt=ShopType.objects.create(type_name="吃的")
        shop=Shop.objects.create(name="一餐",shop_type=shopt,content="营业")
        self.dis1 = Discount.objects.create(shop=shop,body="八折")
        self.list_url = self.live_server_url + reverse('shop:shop_list')
        self.type_url = self.live_server_url + reverse('shop:shop_with_type',args=[shopt.pk])
        self.detail_url = self.live_server_url + reverse('shop:shop_detail',args=[shop.pk])
        self.dis_list_url = self.live_server_url + reverse('discount:show_discount')
        self.dis_type_url = self.live_server_url + reverse('discount:discount_type',args=[shopt.pk])
        self.dis_detail_url = self.live_server_url + reverse('discount:discount_detail',args=[shop.pk])

    # 关闭测试页面
    def tearDown(self):
        self.browser.close()

    # 测试shop_list,shop_with_type,shop_detail三个页面中的优惠信息能否正确显示
    def test_show_discount_on_shop_list(self):
        self.browser.get(self.dis_list_url)
        dis = self.browser.find_element_by_tag_name('b').text
        self.assertEqual(dis,"八折")

    def test_show_discount_on_shop_with_type(self):
        self.browser.get(self.dis_type_url)
        dis = self.browser.find_element_by_tag_name('b').text
        self.assertEqual(dis,"八折")

    def test_show_discount_on_shop_detail(self):
        self.browser.get(self.dis_detail_url)
        dis = self.browser.find_element_by_tag_name('strong').text
        self.assertEqual(dis,"七折")

    # 测试shop_list,shop_with_type,shop_detail三个页面中的'显示优惠信息', '返回'链接能否跳转到正确页面
    def test_url_redirections_on_shop_list(self):
        self.browser.get(self.list_url)
        self.browser.find_element_by_link_text('显示优惠信息').click()
        show_dis_url = self.browser.current_url
        self.browser.find_element_by_link_text('返回').click()
        return_url = self.browser.current_url
        self.assertEqual(show_dis_url,self.dis_list_url + '?page=1')
        self.assertEqual(return_url,self.list_url + '?page=1')

    def test_url_redirections_on_shop_with_type(self):
        self.browser.get(self.type_url)
        self.browser.find_element_by_link_text('显示优惠信息').click()
        dis_type_url = self.browser.current_url
        self.browser.find_element_by_link_text('返回').click()
        return_type_url = self.browser.current_url
        self.assertEqual(dis_type_url,self.dis_type_url)
        self.assertEqual(return_type_url,self.type_url + '?page=1')

    def test_url_redirections_on_shop_detail(self):
        self.browser.get(self.detail_url)
        self.browser.find_element_by_link_text('优惠').click()
        dis_detail_url = self.browser.current_url
        self.browser.find_element_by_class_name('glyphicon-circle-arrow-left').click()
        return_detail_url = self.browser.current_url
        self.assertEqual(dis_detail_url,self.dis_detail_url)
        self.assertEqual(return_detail_url,self.detail_url)
