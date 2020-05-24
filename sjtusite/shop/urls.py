from django.urls import path
from . import views

# http://localhost:8000
# http://localhost:8000/type/1
# http://localhost:8000/type/shop/1
# http://localhost:8000/1/1
# 

# start with shop
app_name = 'shop'  # 新添，在html页面中URL路径中都要加上"shop:"
urlpatterns = [
    # http://localhost:8000/shop/1
    path('', views.shop_list, name='shop_list'),
    # path('<int:shop_pk>', views.shop_detail, name='shop_detail'),
    path('shops/<int:shop_pk>/', views.shop_detail, name='shop_detail'),
    path('type/<int:shop_type_pk>', views.shop_with_type, name='shop_with_type'),
    path('search/', views.shop_search, name='shop_search'),
    path('score', views.score_change, name='score_change')
]
