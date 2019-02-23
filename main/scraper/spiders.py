from dynamic_scraper.spiders.django_spider import DjangoSpider
from main.models import NewsWebsite, News, NewsItem


class ArticleSpider(DjangoSpider):
    name = 'news_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(NewsWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = News
        self.scraped_obj_item_class = NewsItem
        super(ArticleSpider, self).__init__(self, *args, **kwargs)
