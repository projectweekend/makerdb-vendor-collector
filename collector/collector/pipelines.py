from urlparse import urljoin
from scrapy.exceptions import DropItem
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException


class ItemPipeline(object):

    def process_item(self, item, spider):
        if item['vendor_name'] and type(item['vendor_name']) == str:
            item['vendor_name'] = item['vendor_name'].strip()
        else:
            raise DropItem('Missing vendor_name')

        if item['vendor_item_id'] and type(item['vendor_item_id']) == list:
            parts = item['vendor_item_id'][0].split(':')
            try:
                item['vendor_item_id'] = parts[1].strip()
            except IndexError:
                raise DropItem('Invalid vendor_item_id')
        else:
            raise DropItem('Missing vendor_item_id')

        if item['vendor_site'] and type(item['vendor_site']) == str:
            item['vendor_site'] = item['vendor_site'].strip()
        else:
            raise DropItem('Missing vendor_site')

        if item['item_name'] and type(item['item_name']) == list:
            item['item_name'] = item['item_name'][0].strip()
        else:
            raise DropItem('Missing item_name')

        if item['item_url'] and type(item['item_url']) == str:
            item['item_url'] = item['item_url'].strip()
        else:
            raise DropItem('Missing item_url')

        if item['item_image_url'] and type(item['item_image_url']) == list:
            item_image_url = item['item_image_url'][0].strip()
            item['item_image_url'] = urljoin(item['vendor_site'], item_image_url)
        else:
            raise DropItem('Missing item_image_url')

        return item


class DatabasePipeline(object):

    vendor_items = Table('makerdb_vendor_items')

    def process_item(self, item, spider):
        try:
            self.vendor_items.put_item(data=item)
        except ConditionalCheckFailedException:
            raise DropItem('Duplicate item')
