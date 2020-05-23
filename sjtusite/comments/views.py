from django.contrib import messages
from django.shortcuts import render
from shop.models import Shop
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_POST
# Create your views here.

from .forms import CommentForm

def check_user(func):
    def inner(*args, **kwargs):
        #判断是否登录
        username = args[0].session.get("user_id", "")
        if username == "":
            #保存当前的url到session中
            args[0].session["path"] = args[0].path
            #重定向到登录页面
            return redirect(reverse("front:signin"))
        return func(*args, **kwargs)

    return inner

@require_POST
@check_user
def comment(request, shop_pk):
    shop = get_object_or_404(Shop, pk=shop_pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.shop = shop
        comment.name = request.session.get('username')
        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')

        return redirect(shop)
    context = {
        'shop': shop,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')

    return render(request, 'comments/preview.html', context=context)

