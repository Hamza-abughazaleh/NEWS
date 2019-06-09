from django.conf.urls import include, url
from rest_framework import routers

from main.api import views

router = routers.DefaultRouter()
router.register(r'websitesInfo', views.WebSiteViewSet, base_name='websitesinfo')
router.register(r'websites', views.NewsWebSiteViewSet, base_name='newswebsite')
router.register(r'news', views.NewsViewSet)
router.register(r'last_news', views.LastNewsViewSet, base_name='last_news')

urlpatterns = [
    # urls for Django Rest Framework API
    url('^', include(router.urls)),
]
