from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Discount
from .forms import DiscountForm
from shop.models import Shop,ShopType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def show_discount(request):
    context = {}
    context['shop_types'] =  ShopType.objects.all()
    context['discounts'] = Discount.objects.all()
    context['shop_types'] = ShopType.objects.all()

    #------------------------实现分页
    shop_list = Shop.objects.all()
    paginator = Paginator(shop_list, 6)  # 每页显示3篇文章
    page = request.GET.get('page') #页数请求

    context['shop_num']=len(shop_list)
    #为了实现向前翻页和向后翻页，新增一个模块，计算前一页和后一页的页数
    if page==None:
        context['page'] =1
    else:context['page']=int(page)

    if (context['page']>=2) :
        context['previous_page'] = context['page']-1
    else : context['previous_page'] = 1

    if context['page'] < paginator.num_pages:
        context['next_page']= context['page']+1
    else:  context['next_page'] = paginator.num_pages

    context['all_page'] = list (range(1,paginator.num_pages+1))#生成页数序列
    try:
        context['shops'] = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        context['shops'] = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        context['shops'] = paginator.page(paginator.num_pages)
    #-------------------------
    return render(request, 'dis_list.html',context)

def discount_type(request,shop_type_pk):
    context = {}
    shop_type = get_object_or_404(ShopType, pk=shop_type_pk)
    context['shops'] = Shop.objects.filter(shop_type=shop_type)
    context['shop_type'] = shop_type
    context['shop_types'] =  ShopType.objects.all()
    context['discounts']=Discount.objects.all()
    #------------------------实现分页
    context['shop_num']=len(context['shops'])
    paginator = Paginator(context['shops'] , 6)
    page = request.GET.get('page')
    context['all_page'] = list (range(1,paginator.num_pages+1))#生成页数序列

    #为了实现向前翻页和向后翻页，新增一个模块，计算前一页和后一页的页数
    if page==None:
        context['page'] =1
    else:context['page']=int(page)

    if (context['page']>=2) :
        context['previous_page'] = context['page']-1
    else : context['previous_page'] = 1

    if context['page'] < paginator.num_pages:
        context['next_page']= context['page']+1
    else:  context['next_page'] = paginator.num_pages

    try:
        context['shops'] = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        context['shops'] = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        context['shops'] = paginator.page(paginator.num_pages)
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

