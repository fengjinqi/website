from datetime import datetime

from django.contrib.sessions.models import Session
from django.core.cache import cache

#from apps.forum.views import get_online_count
from apps.support.models import QQ
from apps.forum.models import Forum
from django import template
from django.utils.timezone import now, timedelta
from apps.user.models import User

register = template.Library()
@register.inclusion_tag('pc/aside/forum_side.html')
def get_fourm():
    qq = QQ.objects.all()
    fourm = Forum.objects.filter(category__name='求职招聘')[:10]
    sessions = Session.objects.filter(expire_date__gte=datetime.now()).count()
    #print(get_online_count())

    user = User.objects.count()
    cur_date = now().date() + timedelta(days=0)
    days = Forum.objects.filter(add_time__gte=cur_date).count()
    count = Forum.objects.count()
    Hottest = Forum.objects.order_by('-click_nums')[:10]
    return {'fourm':fourm,'qq':qq,'user':user,'sessions':sessions,'days':days,'count':count,'Hottest':Hottest}

