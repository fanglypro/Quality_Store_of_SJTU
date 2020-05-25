from django.test import TestCase
from comments.models import Comment


class TsetModels(TestCase):
    
    def setUp(self):

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
    