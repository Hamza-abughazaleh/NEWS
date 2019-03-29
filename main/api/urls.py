from django.conf.urls import include, url
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from main.api import views

router = routers.DefaultRouter()
router.register(r'websitesInfo', views.WebSiteViewSet, base_name='websitesinfo')
router.register(r'websites', views.NewsWebSiteViewSet, base_name='newswebsite')
router.register(r'news', views.NewsViewSet)
router.register(r'user', views.UserViewSet, base_name='user')

urlpatterns = [
    # urls for Django Rest Framework API
    url('^', include(router.urls)),
    url(r'^login/$', csrf_exempt(views.LoginView.as_view()), name='api-login'),
    url(r'^logout/$', csrf_exempt(views.LogoutView.as_view()), name='api-logout'),
    url(r'^user/update/(?P<pk>\d+)/$', csrf_exempt(views.UserUpdateView.as_view()), name='update')
]
