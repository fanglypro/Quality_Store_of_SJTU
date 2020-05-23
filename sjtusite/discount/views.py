from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Discount
from .forms import DiscountForm
from shop.models import Shop,ShopType
# Create your views here.

def show_discount(request):
    context = {}
    context['shops'] = Shop.objects.all()
    context['shop_types'] =  ShopType.objects.all()
    context['discounts'] = Discount.objects.all()
    return render(request, 'dis_list.html',context)

def discount_type(request,shop_type_pk):
    context = {}
    shop_type = get_object_or_404(ShopType, pk=shop_type_pk)
    context['shops'] = Shop.objects.filter(shop_type=shop_type)
    context['shop_type'] = shop_type
    context['shop_types'] =  ShopType.objects.all()
    context['discounts']=Discount.objects.all()
    return render(request, 'discount_type.html', context)

def discount_detail(request,shop_pk):
    context = {}
    context['shop'] = get_object_or_404(Shop, pk=shop_pk)
    context['shop_types'] =  ShopType.objects.all()
    context['discounts'] = Discount.objects.all()

    new_discount = None

    # if request.method == "SHOP":
    #     discount_form = DiscountForm(data=request.SHOP)
    #     if  discount_form.is_valid():
    #         # 通过表单直接创建新数据对象，但是不要保存到数据库中
    #         new_discount =  discount_form.save(commit=False)
    #         # 设置外键为当前文章
    #         new_discount.post = post
    #         # 将评论数据对象写入数据库
    #         new_discount.save()
    # else:
    #     discount_form = DiscountForm()
    if request.method=='POST':
        if 'discount' in request.POST:
            id = request.POST.get('shopname')
            discount = request.POST.get('introduction')
            new = Discount(shop_id=id, body=discount)
            new.save()
    return render(request, 'dis_detail.html',context)

def check_owner(func):
    def inner(*args, **kwargs):
        #判断是否登录
        username = args[0].session.get("owner_id", "")
        if username == "":
            #保存当前的url到session中
            args[0].session["path"] = args[0].path
            #重定向到登录页面
            return redirect(reverse("front:signinowner"))
        return func(*args, **kwargs)

    return inner

@check_owner
def delete_discount(request, id):
    delete = Discount.objects.get(id=id)
    shop_id = delete.shop.id
    delete.delete()
    return redirect(reverse('discount:discount_detail', kwargs={'shop_pk':shop_id}))

