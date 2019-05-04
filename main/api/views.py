from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.db.models import Q
from main.api.serializers import WebSiteInfoSerializer, NewsSerializer, NewsDetailsSerializer, NewsWebsiteSerializer
from main.models import WebsiteInfo, News, NewsWebsite
from main.views import single_crawl_without_scheduling_celery


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
        if self.request.GET.get("action_type") in ["DB", "CS", "CW"]:

            result = single_crawl_without_scheduling_celery(search_term, website_list,
                                                            self.request.GET.get("action_type"))
            if not result:
                return []
        filtered_queryset = super(NewsViewSet, self).filter_queryset(queryset)
        return filtered_queryset.filter(Q(item_website__in=website_list))
