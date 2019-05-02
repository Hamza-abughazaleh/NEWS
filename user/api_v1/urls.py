from __future__ import unicode_literals

from rest_framework import routers

from user.api_v1 import api

router = routers.DefaultRouter()
router.register(r'user', api.UserViewSet)

app_name = 'user'
urlpatterns = router.urls
