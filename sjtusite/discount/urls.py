from django.contrib import admin
from django.urls import path, include
from . import views

app_name='discount'
#在所有原网页url的“/shop”之前加一个“/discount”
urlpatterns = [
    path('shop/',views.show_discount),
    path('shop/type/<int:shop_type_pk>', views.discount_type, name='discount_type'),
    path('shop/shops/<int:shop_pk>/', views.discount_detail, name='discount_detail'),
]
