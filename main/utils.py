from datetime import datetime, time, timedelta
from django.utils.translation import get_language
from main.models import News


def get_news_distinct():
    date = get_time(datetime.now())
    first_news = News.objects.order_by('news_website', '-created_date').distinct('news_website')
    news = News.objects.filter(id__in=first_news, news_website__language=get_language(),
                               created_date__gte=date).order_by("-created_date")
    return news


def get_time(value):
    min_time = time.min
    final_time = datetime.combine(value - timedelta(days=3), min_time)
    return final_time
