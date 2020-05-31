from django.urls import path
from . import views


app_name = 'shop'  # 新添，在html页面中URL路径中都要加上"shop:"
urlpatterns = [
    path('', views.shop_list, name='shop_list'),
    path('shops/<int:shop_pk>/', views.shop_detail, name='shop_detail'),
    path('type/<int:shop_type_pk>', views.shop_with_type, name='shop_with_type'),
    path('search/', views.shop_search, name='shop_search'),
    path('score', views.score_change, name='score_change')
]
