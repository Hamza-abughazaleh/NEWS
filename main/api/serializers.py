from News import settings
from rest_framework import serializers

from main.models import WebsiteInfo, News, NewsWebsite


class WebSiteInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebsiteInfo
        fields = ('pk', 'key', 'website_type')


class NewsWebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsWebsite
        fields = ('pk', 'name', 'url')


class NewsSerializer(serializers.ModelSerializer):
    news_details = serializers.HyperlinkedIdentityField(view_name='news-detail', lookup_field='pk')
    created_date = serializers.DateTimeField(format='%b %d,%Y,%I:%M %p.')

    class Meta:
        model = News
        fields = ('pk', 'news_details', 'title', 'image', 'created_date', 'item_website', 'news_website')


class NewsDetailsSerializer(serializers.ModelSerializer):
    news_website_details = serializers.HyperlinkedRelatedField(view_name='newswebsite-detail', source='news_website',
                                                               read_only=True)
    created_date = serializers.DateTimeField(format='%b %d,%Y,%I:%M %p.')

    class Meta:
        model = News
        fields = ('pk', 'title', 'description', 'image', 'url', 'news_website_details', 'created_date')
