import scrapy
from collector.items import CollectorItem


SITE_ROOT = 'http://www.adafruit.com'


class AdafruitSpider(scrapy.Spider):

    name = 'adafruit'
    allowed_domains = ['adafruit.com']
    start_urls = ['http://www.adafruit.com/category/17']
    xpath_for = {
        'name': '//div[@id="prod-right-side"]/h1/text()',
        'img_src': '//div[@id="prod-primary-img-container"]//img/@src',
        'vendor_product_id': '//div[@class="product_id"]/text()'
    }

    def parse(self, response):
        product_href = '//div[@class="row product-listing"]//h1/a/@href'
        for item in response.selector.xpath(product_href):
            url = response.urljoin(item.extract())
            yield scrapy.Request(url=url, callback=self.parse_product_info)

    def parse_product_info(self, response):
        try:
            info = response.selector.xpath('//div[@class="row product-info"]')[0]
        except IndexError:
            print('No product info for: {0}'.format(response.url))
        else:
            yield CollectorItem(
                name=info.xpath(self.xpath_for['name']).extract(),
                url=response.url,
                image_url=info.xpath(self.xpath_for['img_src']).extract(),
                vendor_name='Adafruit',
                vendor_product_id=info.xpath(self.xpath_for['vendor_product_id']).extract())
