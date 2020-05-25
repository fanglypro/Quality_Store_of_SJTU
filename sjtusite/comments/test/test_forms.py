from django.test import TestCase
from comments.forms import CommentForm
from shop.models import Shop,ShopType

class TsetForms(TestCase):

    def test_comment_form_notvalid(self):
        form = CommentForm (data = {})

        self.assertFalse( form.is_valid() )

    def test_comment_form_valid(self):
        shopType1 = ShopType.objects.create(
            type_name = '吃的'
        )

        
        shop1 = Shop.objects.create(
            name = "一餐",
            content = "yammy",
            shop_type = shopType1,
        )

        form = CommentForm (data = {
            'name' : 'liangxiaoyou', 
            'text' : 'yammy',
            'shop' : 'defalt',
        })

        self.assertTrue( form.is_valid() )