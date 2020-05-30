from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Shop, ShopType
import json

class TestView(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('shop:shop_list')
        self.detail_url = reverse('shop:shop_detail', args=[1])
        self.type_url = reverse('shop:shop_with_type', args=[1])
        print(self.detail_url)
        print(self.type_url)
        self.shop_type1 = ShopType.objects.create(
            type_name = '吃的'
        )
        self.shop1 = Shop.objects.create(
            name = "一餐",
            content = "简介",
            shop_type = self.shop_type1,
        )
        
    def test_shop_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop_list.html')

    def test_shop_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop_detail.html')