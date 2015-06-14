# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CollectorItem(scrapy.Item):

    name = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    vendor_name = scrapy.Field()
    vendor_product_id = scrapy.Field()
