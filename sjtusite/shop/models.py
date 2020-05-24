from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class ShopType(models.Model):
    type_name = models.CharField(max_length=10) # 吃的、喝的、玩的、学习、生活、打扮

    def __str__(self):
        return self.type_name

class Shop(models.Model):
    name = models.CharField(max_length=20)
    shop_type = models.ForeignKey(ShopType, on_delete=models.DO_NOTHING)
    content = models.TextField()
    grade = models.IntegerField(default=0)
    grade_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):#新增
        self.modified_time = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):#新增
        return reverse('shop:shop_detail', kwargs={'shop_pk': self.pk})  #comment.view中重定向到 post 的详情页，当 redirect 函数接收一个模型的实例时调用这个模型实例的 get_absolute_url 方法