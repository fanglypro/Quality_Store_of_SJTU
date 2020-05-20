from django.shortcuts import render
from shop.views import shop_search
from shop.forms import  SearchForm
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.models import Shop, ShopType

def home(request):
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
    
    return render(request, 'home.html', context)