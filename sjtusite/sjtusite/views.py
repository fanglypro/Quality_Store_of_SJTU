from django.shortcuts import render
from shop.views import shop_search
from shop.forms import  SearchForm
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.models import Shop, ShopType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.db.models import Sum
import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

def get_seven_days_hot_shops():  #最近七天最热店铺
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    shops = Shop.objects.filter(read_details__date__lt=today, read_details__date__gte=date).values('id', 'name').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return shops[:7]

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
    
    shop_content_type = ContentType.objects.get_for_model(Shop)
    dates, read_nums = get_seven_days_read_data(shop_content_type)

    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(shop_content_type)
    # context['yesterday_hot_data'] = get_yesterday_hot_data(shop_content_type)
    # context['seven_days_hot_shops'] = get_seven_days_hot_shops()
    return render(request, 'home.html', context)