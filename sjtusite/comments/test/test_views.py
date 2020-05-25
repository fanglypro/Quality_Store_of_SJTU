from django.test import TestCase , Client
from comments.models import Comment
from django.urls import reverse , resolve
from shop.models import Shop,ShopType
from comments.forms import CommentForm

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.comment_url = reverse("comments:comment",args=["1"])
        shopType1 = ShopType.objects.create(
            type_name = '吃的'
        )
        shop1 = Shop.objects.create(
            name = "一餐",
            content = "yammy",
            shop_type = shopType1,
        )
        self.comment1 = Comment.objects.create(
                            name = "liangxiaoyou",
                            text = "yammy",
                            shop = shop1,
                        )
    
        self.form = CommentForm (data = {
            'name' : 'liangxiaoyou', 
            'text' : 'yammy',
            'shop' : 'defalt',
        })


    def test_post(self):

        response = self.client.post(self.form )
        self.assertEquals(response.status_code, 404)