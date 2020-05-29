from django.test import TestCase,Client
from django.urls import reverse
from discount.models import Discount
from shop.models import Shop,ShopType

class TestViews(TestCase):
    # 添加数据
    def setUp(self):
        self.shopt = ShopType.objects.create(type_name="吃的")
        self.shop = Shop.objects.create(name="三餐",shop_type=self.shopt,content="营业")
        self.client = Client()
        self.show_discount_url = reverse('discount:show_discount')
        self.discount_type_url = reverse('discount:discount_type',args=[self.shopt.pk])
        self.discount_detail_url = reverse('discount:discount_detail',args=[self.shop.pk])
        self.delete_discount_url = reverse('discount:discount_detail',args=[self.shop.pk])

    # 分别测试视图函数的请求是否被正确处理，是否使用了正确的模板
    def test_show_discount(self):
        response = self.client.get(self.show_discount_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'dis_list.html')

    def test_discount_type(self):
        response = self.client.get(self.discount_type_url)
        self.assertEqual(response.status_code,404)
        self.assertTemplateUsed(response,'discount_type.html')

    def test_discount_detail(self):
        response = self.client.get(self.discount_detail_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'dis_list.html')

    def test_delete_discount(self):
        response = self.client.get(self.delete_discount_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'dis_detail.html')

