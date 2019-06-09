from __future__ import unicode_literals
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers

from user.api_v1 import api

router = routers.SimpleRouter()

urlpatterns = [
    # urls for Django Rest Framework API
    url(r'^profile/$', csrf_exempt(api.UserViewSet.as_view()), name='user-detail')

]
