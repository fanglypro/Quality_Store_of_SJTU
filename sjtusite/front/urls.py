from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    # path('', views.index, name='index'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin1/', views.SigninView_Owner.as_view(), name='signinowner'),
    path('signup1/', views.SignupView_Owner.as_view(), name='signupowner'),
    path('blog/', views.blog, name='blog'),
    path('video/', views.video, name='video'),
    path('logout/', views.logout, name='logout'),
    path('cpwd/', views.change_pwd, name='changepwd'),
    path('user/detail/', views.User_detail.as_view(), name='user_detail'),
]
