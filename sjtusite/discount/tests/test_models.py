# 引入Django.test提供的测试模块，这里选用的是TestCase类作为单元测试的模板。
from django.test import TestCase
from discount.models import Discount
from shop.models import Shop,ShopType


# 构造单元测试类，继承相应的模板。
class TestDiscount(TestCase):
    # 添加数据
    def setUp(self):
        self.shopt=ShopType.objects.create(type_name="吃的")
        self.shop1=Shop.objects.create(name="一餐",shop_type=self.shopt,content="营业")
        self.shop2=Shop.objects.create(name="二餐",shop_type=self.shopt,content="营业")
        self.dis1 = Discount.objects.create(shop=self.shop1,body="八折")
        self.dis2 = Discount.objects.create(shop=self.shop2,body="七折")

    # 测试优惠信息是否被添加
    def test_models_discount_body(self):
        self.assertEqual(self.dis1.body,"八折")
        self.assertEqual(self.dis2.body,"七折")

    # 测试优惠信息与店铺名是否对应
    def test_models_shop_names(self):
        self.assertEqual(self.dis1.shop.name,"一餐")
        self.assertEqual(self.dis2.shop.name,"二餐")





