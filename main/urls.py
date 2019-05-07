from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^search', views.SerchForm.as_view(), name="search_news"),
    url(r'^news/list/(?P<pk>\d+)$', views.NewsListView.as_view(), name="news_list"),
    url(r'^news/detail/(?P<pk>\d+)$', views.NewsDetailView.as_view(), name='news_detail')
]
