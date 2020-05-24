from shop.models import *
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

#共两个属性，一个外码链接到店铺信息，一个优惠内容
class Discount(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='discounts')
    body = models.TextField()

    class Meta:
        ordering = ("shop",)

    def get_absolute_url(self):
        return reverse('discount:show_discount', args=[self.shop,])