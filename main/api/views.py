from django.contrib.auth import authenticate, login
from rest_framework import viewsets, filters, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.conf import settings

from main.api.serializers import WebSiteInfoSerializer, NewsSerializer, NewsDetailsSerializer, NewsWebsiteSerializer, \
    UserSerializer, UserDetailsSerializer, LoginSerializer
from main.models import WebsiteInfo, News, NewsWebsite
from main.views import single_crawl_without_scheduling_celery
from user.models import User


class WebSiteViewSet(viewsets.ModelViewSet):
    """from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
    API endpoint that allows users to be viewed or edited.
    """
    queryset = WebsiteInfo.objects.all()
    serializer_class = WebSiteInfoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('key', 'url',)


class NewsWebSiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = NewsWebsite.objects.all()
    serializer_class = NewsWebsiteSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'url',)


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description',)

    details_serializer_class = NewsDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['context'] = self.get_serializer_context()
        serializer = self.details_serializer_class(instance, context={'request': request})
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        if 'pk' in self.kwargs:
            filtered_queryset = super(NewsViewSet, self).filter_queryset(queryset)
            return filtered_queryset.filter(pk=self.kwargs['pk'])

        websiteInfo_id = self.request._request.GET.get("websiteinfo_id", "")
        if websiteInfo_id:
            website = WebsiteInfo.objects.get(id=websiteInfo_id)
            filtered_queryset = super(NewsViewSet, self).filter_queryset(queryset)
            return filtered_queryset.filter(news_website__name__contains=website.key)

        search_term = self.request._request.GET.get("search", "").strip()
        if not search_term:
            return []
        if not self.request._request.GET.getlist("websites"):
            website_info_qs = WebsiteInfo.objects.all()
        else:
            website_info_qs = WebsiteInfo.objects.filter(
                key__in=self.request._request.GET.getlist("websites"))
        if not website_info_qs:
            return []
        website_list = list(each_website.key for each_website in website_info_qs)
        if self.request.GET.get("action_type", "DB") in ["CS", "CW"]:

            result = single_crawl_without_scheduling_celery(search_term, website_list,
                                                            self.request.GET.get("action_type", "DB") == "CS")
            if not result:
                return []
        filtered_queryset = super(NewsViewSet, self).filter_queryset(queryset)
        return filtered_queryset.filter(item_website__in=website_list)


class UserViewSet(viewsets.ModelViewSet):
    """from rest_framework import status

    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'id',)

    details_serializer_class = UserDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['context'] = self.get_serializer_context()
        serializer = self.details_serializer_class(instance, context={'request': request})
        return Response(serializer.data)


class UserUpdateView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)


class LogoutView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        request = request._request
        request.session.clear()
        # request.session = None

        return Response("ok")


class LoginView(APIView):
    serializer_class = LoginSerializer
    ser = user = None

    def get(self, request, format=None):
        if settings.DEBUG:
            if request.user.is_authenticated():
                return Response(
                    {'detail': 'Session is in use, log out first'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise MethodNotAllowed('GET')

    def post(self, request, format=None):

        # refuse to login logged in users, to avoid attaching sessions to
        # multiple users at the same time.
        username = request.POST['username']
        password = request.POST['password']

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.user = self.user
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt)
    def delete(self, request, format=None):
        """
        Destroy the session.

        for anonymous users that means having their basket destroyed as well,
        because there is no way to reach it otherwise.
        """
        request = request._request

        request.session.clear()
        request.session.delete()
        request.session = None

        return Response("ok")
