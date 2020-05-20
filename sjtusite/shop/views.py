from django.shortcuts import render, get_object_or_404, redirect
from .models import Shop, ShopType
from django.contrib.postgres.search import SearchVector
from .forms import  SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def shop_list(request):
    context = {}
    #context['shops'] = Shop.objects.all()
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
    return render(request, 'shop/shop_list.html', context)


def shop_detail(request, shop_pk):
     context = {}
     context['shop'] = get_object_or_404(Shop, pk=shop_pk)
     return render(request, 'shop/shop_detail.html', context)



def shop_with_type(request, shop_type_pk):
    context = {}
    shop_type = get_object_or_404(ShopType, pk=shop_type_pk)
    context['shops'] = Shop.objects.filter(shop_type=shop_type)
    context['shop_type'] = shop_type
    context['shop_types'] = ShopType.objects.all()
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
    #-------------------------

    return render(request, 'shop/shops_with_type.html', context)


#新增全文搜索功能，搜索范围是标题和简介
def shop_search(request):
    context = {}
    if (request.method == "POST") :
        if (request.POST.get('keyword') ):
            #form = SearchForm()
            query = request.POST.get('keyword')
            results = []
            #if query in request.POST:
                #form = SearchForm(request.POST)
                #if form.is_valid():
                    #query = form.cleaned_data['query']
                    #search_vector = SearchVector('shop_name', 'detail')
                    #目前只能完成根据精确匹配项计算出来的分数筛选出的项，
                    #商店名的三元匹配已实现
            results= Shop.objects.annotate(
                                           similarity=TrigramSimilarity('name', query)*5+TrigramSimilarity('content', query),
                                          ).filter(similarity__gte=0.05).order_by('-similarity')
            context={'query': query, 
                    'results': results,
                    }
            return render(request, 'shop/search.html', context)
    
    return render(request,'shop/search.html', context)