from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem
from django.utils.translation import ugettext_lazy as _


class WebsiteInfo(models.Model):
    GENDER_CHOICES = (
        ('ar', _('Arabic')),
        ('en', _('English')),
    )
    key = models.CharField(max_length=30)
    website_type = models.CharField(max_length=2, blank=True, null=True, choices=GENDER_CHOICES)
    search_domain = models.CharField(max_length=200)
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(max_length=256,upload_to='website_pics')

    def __str__(self):
        return self.key


class NewsWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    news_website = models.ForeignKey(NewsWebsite)
    description = models.TextField(blank=True)
    image = models.URLField()
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     from bs4 import BeautifulSoup
    #     import json
    #     table_data = [[cell.text for cell in row("td")]
    #                   for row in BeautifulSoup(self.description)("tr")]
    #     self.djson = json.dumps(dict(table_data))
    #     # from crawling.Html2Json import html_to_json
    #     # self.djson = html_to_json(self.description)
    #     super(Product, self).save(*args, **kwargs)

    # def djson_formatted(self):
    #     from django.utils.safestring import mark_safe
    #
    #     data = json.loads(self.djson, encoding='utf-8')
    #
    #     return mark_safe(data)
    #
    #     djson_formatted.short_description = 'Details Formatted'


class NewsItem(DjangoItem):
    django_model = News


@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, News):
        if instance.checker_runtime:
            instance.checker_runtime.delete()


pre_delete.connect(pre_delete_handler)
