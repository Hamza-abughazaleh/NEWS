import datetime

from celery.task import task

from dynamic_scraper.utils.task_utils import TaskUtils
from dynamic_scraper.models import SchedulerRuntime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from main.models import NewsWebsite, WebsiteInfo


@task()
def run_spiders():
    t = TaskUtils()
    t.run_spiders(NewsWebsite, 'scraper', 'scraper_runtime', 'product_spider')


def prepare_data(search_term, websites_keys):
    website_keys_to_be_crawled = []
    for website_key in websites_keys:
        website_name_name = website_key + "_" + search_term.replace(" ", "_")
        if not NewsWebsite.objects.filter(name=website_name_name).exists():
            website_keys_to_be_crawled.append(website_key)
    return website_keys_to_be_crawled


def concatenate_website_domain(domain, search_term):
    return domain.replace("###", search_term.replace(" ", "+"))


@task()
def single_crawl_without_scheduling(search_term, websites_keys, scheduled=True):
    try:
        website_keys_to_be_crawled = prepare_data(search_term, websites_keys)
        if website_keys_to_be_crawled:
            process = CrawlerProcess(get_project_settings())
            website_products_objects_to_be_deleted = []
            for website_key in website_keys_to_be_crawled:
                website = WebsiteInfo.objects.get(key=website_key)
                website_url = concatenate_website_domain(website.search_domain, search_term)
                website_news_name = website_key + "_" + search_term.replace(" ", "_")
                websites_scraper = website.scraper
                websites_scraper_runtime = create_scraper_runtime()
                news_website = NewsWebsite.objects.create(name=website_news_name, url=website_url,
                                                          scraper=websites_scraper,
                                                          scraper_runtime=websites_scraper_runtime,
                                                          language=website.website_type)
                website_products_objects_to_be_deleted.append(news_website)
                process.crawl('news_spider', id=news_website.id, do_action='yes', )
            process.start()
            if not scheduled:
                for website_products in website_products_objects_to_be_deleted:
                    website_products.delete()
        return True, "crawled success"
    except Exception as e:
        return False, e


def create_scraper_runtime():
    scraper_runtime_type = 'S'
    if SchedulerRuntime.objects.filter(runtime_type=scraper_runtime_type).exists():
        scraper_object = SchedulerRuntime.objects.get(runtime_type=scraper_runtime_type)
    else:
        next_action_factor = 1.0
        next_action_time = datetime.datetime.now()
        scraper_object = SchedulerRuntime.objects.create(runtime_type=scraper_runtime_type,
                                                         next_action_time=next_action_time,
                                                         next_action_factor=next_action_factor)
    return scraper_object

# @task()
# def run_checkers():
#     t = TaskUtils()
#     t.run_checkers(Product, 'news_website__scraper', 'checker_runtime', 'product_checker')
