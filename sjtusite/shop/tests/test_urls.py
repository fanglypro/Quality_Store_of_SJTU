from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop.views import shop_list, shop_detail, shop_with_type, shop_search

# don't need database
class TestUrls(SimpleTestCase): 
    def test_list_url_is_resolved(self):
        url = reverse('shop:shop_list')
        self.assertEquals(resolve(url).func, shop_list)

    def test_detail_is_resolved(self):
        url = reverse('shop:shop_detail', args=[1])
        self.assertEquals(resolve(url).func, shop_detail)
        
    def test_type_is_resolved(self):
        url = reverse('shop:shop_with_type', args=[1])
        self.assertEquals(resolve(url).func, shop_with_type)
