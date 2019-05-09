from __future__ import unicode_literals
from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers

from user.api_v1 import api
from user.api_v1 import api

router = routers.DefaultRouter()
# router.register(r'user', api.UserViewSet)

app_name = 'user'
urlpatterns = router.urls

urlpatterns = [
    # urls for Django Rest Framework API
    # url('^', include(router.urls)),
    url(r'^profile/$', csrf_exempt(api.UserViewSet.as_view()), name='user-detail')

]
