# encoding: utf-8

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View
from .forms import SignupForm, SigninForm, SignupFormOwner, SigninFormOwner
from .models import User, Owner
from django.template.context_processors import debug
from django.contrib.auth.context_processors import auth
from django.contrib import messages
# from django.contrib.messages.context_processors import messages
import requests


def index(request):
    return render(request, 'front/front_index.html')


class SigninView(View):
    def get(self, request):
        return render(request, 'front/front_signin.html')

    def post(self, request):
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username, password=password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                # return redirect(reverse('home'))
                return render(request, 'front/front_tips.html', context={'message': "登陆成功！"})
            else:
                print('用户名或者密码错误！')
                # messages.add_message(request,messages.INFO,'用户名或者密码错误！')
                messages.info(request, '用户名或者密码错误！')
                return redirect(reverse('front:signin'))
        else:
            # errors = form.errors.get_json_data()
            # print(errors)
            errors = form.get_error()
            for error in errors:
                messages.info(request, error)
            return redirect(reverse('front:signin'))


class SignupView(View):
    def get(self, request):
        print(type(request._messages))
        return render(request, 'front/front_signup.html')

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('front:signin'))
        else:
            print(form.errors.get_json_data())
            return redirect(reverse('front:signup'))


class SigninView_Owner(View):
    def get(self, request):
        return render(request, 'front/front_signin_owner.html')

    def post(self, request):
        form = SigninFormOwner(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = Owner.objects.filter(username=username, password=password).first()
            if user:
                request.session['owner_id'] = user.id
                # return redirect(reverse('home'))
                return render(request, 'front/front_tips.html', context={'message': "登陆成功！"})
            else:
                # print('用户名或者密码错误！')
                # messages.add_message(request,messages.INFO,'用户名或者密码错误！')
                messages.info(request, '用户名或者密码错误！')
                return redirect(reverse('front:signinowner'))  ##
        else:
            # errors = form.errors.get_json_data()
            # print(errors)
            errors = form.get_error()
            for error in errors:
                messages.info(request, error)
            return redirect(reverse('front:signinowner'))


class SignupView_Owner(View):
    def get(self, request):
        return render(request, 'front/front_signup_owner.html')

    def post(self, request):
        # print(request.POST)
        form = SignupFormOwner(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('front:signinowner'))  ##
        else:
            print(form.errors.get_json_data())
            return redirect(reverse('front:signupowner'))


# 验证是否登录的装饰器
def check_ur(func):
    def inner(*args, **kwargs):
        # 判断是否登录
        username = args[0].session.get("user_id", "")
        if username == "":
            username = args[0].session.get("owner_id", "")
        if username == "":
            # 保存当前的url到session中
            args[0].session["path"] = args[0].path
            # 重定向到登录页面
            return redirect(reverse("front:signin"))
        return func(*args, **kwargs)

    return inner


def check_user(func):
    def inner(*args, **kwargs):
        # 判断是否登录
        username = args[0].session.get("user_id", "")
        if username == "":
            # 保存当前的url到session中
            args[0].session["path"] = args[0].path
            # 重定向到登录页面
            return redirect(reverse("front:signin"))
        return func(*args, **kwargs)

    return inner


def check_owner(func):
    def inner(*args, **kwargs):
        # 判断是否登录
        username = args[0].session.get("owner_id", "")
        if username == "":
            # 保存当前的url到session中
            args[0].session["path"] = args[0].path
            # 重定向到登录页面
            return redirect(reverse("front:signinowner"))
        return func(*args, **kwargs)

    return inner


def logout(request):
    request.session.flush()
    return redirect(reverse('home'))


class User_detail(View):
    def get(self, request):
        context = {}
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        context['user'] = user
        return render(request, 'front/front_user_detail.html', context=context)

    def post(self, request):
        if 'submit' in request.POST:
            user_id = request.session.get('user_id')
            username = request.POST.get('username')
            telephone = request.POST.get('telephone')
            password = request.POST.get('password')
            gender = request.POST.get('gender')
            # messages.add_message(request, messages.INFO, '性别输入错误')
            introduction = request.POST.get('introduction')
            User.objects.filter(pk=user_id).update(username=username, telephone=telephone, gender=gender,
                                                   introduction=introduction)
            # return redirect(reverse('home'))
            return render(request, 'front/front_tips.html', context={'message': "用户信息修改成功！"})
        elif 'delete' in request.POST:
            user_id = request.session.get('user_id')
            if str(request.POST.get('user_id')) == str(user_id):
                User.objects.filter(pk=user_id).delete()
                request.session.flush()
                return render(request, 'front/front_tips.html', context={'message': "账户注销成功！"})
            else:
                return redirect(reverse('home'))


@check_user
def change_pwd(request):
    if request.method == 'GET':
        print("get")
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        return render(request, 'front/front_cpwd.html', context={'name': "{}".format(user.username)})
    else:
        print("post")
        user_id = request.session.get('user_id')
        pwd_old = request.POST.get('password_old')
        pwd = request.POST.get('password')
        pwd2 = request.POST.get('password_repeat')
        if pwd_old != User.objects.get(pk=user_id).password:
            return render(request, 'front/front_tips.html', context={'message': "用户原密码错误！"})
        if pwd == pwd2:
            User.objects.filter(pk=user_id).update(password=pwd)
            return render(request, 'front/front_tips.html', context={'message': "修改密码成功"})
        else:
            pass
            RuntimeError("可能出现恶意伪造修改密码！")


def test(request):
    # post_data = {'clientid': '3QMvuozrNInLU5O7PKIS','secretkey':'3175F20BCE5E31010246A4646E6BB93D9DBA926E2C5861CB'}
    # response = requests.get('https://api.sjtu.edu.cn/v1/me/profile', data=post_data)
    response = requests.get(
        'https://jaccount.sjtu.edu.cn/oauth2/authorize?response_type=code&scope=essential&client_id=3QMvuozrNInLU5O7PKIS&redirect_uri=https://www.baidu.com')
    content = response.content
    print(content)
    return HttpResponse(content)
