from django.db import models
from django.core.validators import MinLengthValidator


class User(models.Model):
    username = models.CharField(max_length=100, validators=[MinLengthValidator(4)])
    password = models.CharField(max_length=16, validators=[MinLengthValidator(6)])
    telephone = models.CharField(max_length=11)
    verification = models.BooleanField(default=False)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default='M')
    introduction = models.TextField(null=True)

    def __str__(self):
        return "front %s " % self.username

    class Meta:
        app_label = "front"


class Owner(models.Model):
    username = models.CharField(max_length=100, validators=[MinLengthValidator(4)])
    password = models.CharField(max_length=16, validators=[MinLengthValidator(6)])
    verification = models.BooleanField(default=False)
    telephone = models.CharField(max_length=11)
    # 数据库中的shop信息由管理员添加
    shopname = models.CharField(max_length=100, validators=[MinLengthValidator(1)], unique=True)
    credit = models.SmallIntegerField(default=100)

    def __str__(self):
        return "front %s " % self.username

    class Meta:
        app_label = "front"
