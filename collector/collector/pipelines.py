from urlparse import urljoin, urlparse
from scrapy.exceptions import DropItem
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException


class ItemPipeline(object):

    def process_item(self, item, spider):
        if not item['vendor_name']:
            raise DropItem('Missing vendor_name')
        if not item['vendor_item_id']:
            raise DropItem('Missing vendor_item_id')
        if not item['vendor_site']:
            raise DropItem('Missing vendor_site')
        if not item['item_name']:
            raise DropItem('Missing item_name')
        if not item['item_url']:
            raise DropItem('Missing item_url')
        if not item['item_image_url']:
            raise DropItem('Missing item_image_url')
        else:
            parsed = urlparse(item['item_image_url'])
            if not parsed.netloc:
                item['item_image_url'] = urljoin(item['vendor_site'], item['item_image_url'])
        return item


class DatabasePipeline(object):

    vendor_items = Table('makerdb_vendor_items')

    def process_item(self, item, spider):
        try:
            self.vendor_items.put_item(data=item)
        except ConditionalCheckFailedException:
            raise DropItem('Duplicate item')
