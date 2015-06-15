import scrapy


class CollectorItem(scrapy.Item):

    name = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    vendor_name = scrapy.Field()
    vendor_product_id = scrapy.Field()
