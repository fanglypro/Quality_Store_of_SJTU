from django.test import SimpleTestCase
from django.urls import reverse , resolve
from comments.views import comment

#以shop_pk = 1为例测试
class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse("comments:comment",args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, comment)