from datetime import datetime, time
from django.utils.translation import get_language
from django.db.models import Q
from main.models import News


def get_news_distinct():
    date = get_time(datetime.now())
    news = News.objects.filter(Q(news_website__language=get_language()) and Q(created_date__gte=date)).order_by(
        'news_website', "-created_date").distinct('news_website')
    return news


def get_time(value):
    min_time = time.min
    final_time = datetime.combine(value, min_time)
    return final_time
