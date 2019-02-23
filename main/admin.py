from __future__ import unicode_literals

from django.contrib import admin
from main.models import NewsWebsite, News ,WebsiteInfo


class NewsWebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_', 'scraper')
    list_display_links = ('name',)

    def url_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.url, title=instance.url)

    url_.allow_tags = True


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'news_website', 'url_',)
    list_display_links = ('title',)
    raw_id_fields = ('checker_runtime',)

    def url_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.url, title=instance.url)


    # readonly_fields = ('djson', 'djson_formatted')

    url_.allow_tags = True


admin.site.register(NewsWebsite, NewsWebsiteAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(WebsiteInfo)
