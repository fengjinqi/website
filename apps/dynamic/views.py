
from django.shortcuts import render

# Create your views here.
from pure_pagination import Paginator,PageNotAnInteger

from apps.article.models import Recommend
from apps.dynamic.models import *
from apps.support.models import link, QQ, Banners


def Home(request):
    """
    首页
    :param request:
    :return:
    """
    recommend = Recommend.objects.filter(is_recommend=True)[:10]

    qq = QQ.objects.all()
    links = link.objects.all()

    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = request.GET.get('page')
    # Provide Paginator with the request object for complete querystring generation
    dynamicList = dynamic.objects.filter(is_delete=False)[:500]

    dynamicPage = Paginator(dynamicList, 10, request=request).page(page)

    banners = Banners.objects.first()
    return render(request, 'pc/index.html', {'dynamicPage':dynamicPage})
