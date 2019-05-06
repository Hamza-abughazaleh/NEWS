import logging
from datetime import datetime

from django.db.utils import IntegrityError
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime

from main.parsing import parse_descreption_to_text, image_res


class DjangoWriterPipeline(object):

    def process_item(self, item, spider):
        if spider.conf['DO_ACTION']:  # Necessary since DDS v.0.9+
            try:
                item['news_website'] = spider.ref_object
                item['item_website'] = spider.ref_object.name.split("_")[0]
                item['created_date'] = datetime.now()
                if 'description' in item:
                    item['description'] = parse_descreption_to_text(item['description'])

                if 'image' in item:
                    item['image'] = image_res(spider.ref_object.name, item['image'])

                checker_rt = SchedulerRuntime(runtime_type='C')
                checker_rt.save()
                item['checker_runtime'] = checker_rt

                item.save()
                spider.action_successful = True
                dds_id_str = str(item._dds_item_page) + '-' + str(item._dds_item_id)
                spider.struct_log("{cs}Item {id} saved to Django DB.{ce}".format(
                    id=dds_id_str,
                    cs=spider.bcolors['OK'],
                    ce=spider.bcolors['ENDC']))

            except IntegrityError as e:
                spider.log(str(e), logging.ERROR)
                spider.log(str(item._errors), logging.ERROR)
                raise DropItem("Missing attribute.")
        else:
            if not item.is_valid():
                spider.log(str(item._errors), logging.ERROR)
                raise DropItem("Missing attribute.")

        return item
