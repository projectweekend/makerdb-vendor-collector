import scrapy
from collector.items import CollectorItem


SITE_ROOT = 'http://www.adafruit.com'


class AdafruitSpider(scrapy.Spider):

    name = 'adafruit'
    allowed_domains = ['adafruit.com']
    start_urls = [
        'http://www.adafruit.com/category/8',
        'http://www.adafruit.com/category/17',
        'http://www.adafruit.com/category/33',
        'http://www.adafruit.com/category/35',
        'http://www.adafruit.com/category/37',
        'http://www.adafruit.com/category/40',
        'http://www.adafruit.com/category/44',
        'http://www.adafruit.com/category/50',
        'http://www.adafruit.com/category/54',
        'http://www.adafruit.com/category/63',
        'http://www.adafruit.com/category/65',
        'http://www.adafruit.com/category/75',
        'http://www.adafruit.com/category/82',
        'http://www.adafruit.com/category/105',
        'http://www.adafruit.com/category/112',
        'http://www.adafruit.com/category/117',
        'http://www.adafruit.com/category/128',
        'http://www.adafruit.com/category/168',
        'http://www.adafruit.com/category/196',
        'http://www.adafruit.com/category/203',
        'http://www.adafruit.com/category/227',
        'http://www.adafruit.com/category/234',
        'http://www.adafruit.com/category/290',
        'http://www.adafruit.com/category/307',
        'http://www.adafruit.com/category/342'
    ]
    xpath_for = {
        'product_url': '//div[@class="row product-listing"]//h1/a/@href',
        'product_info': '//div[@class="row product-info"]',
        'name': '//div[@id="prod-right-side"]/h1/text()',
        'img_src': '//div[@id="prod-primary-img-container"]//img/@src',
        'vendor_product_id': '//div[@class="product_id"]/text()'
    }

    def parse(self, response):
        for item in response.selector.xpath(self.xpath_for['product_url']):
            url = response.urljoin(item.extract())
            yield scrapy.Request(url=url, callback=self.parse_product_info)

    def parse_product_info(self, response):
        try:
            info = response.selector.xpath(self.xpath_for['product_info'])[0]
        except IndexError:
            print('No product info for: {0}'.format(response.url))
        else:
            yield CollectorItem(
                name=info.xpath(self.xpath_for['name']).extract(),
                url=response.url,
                image_url=info.xpath(self.xpath_for['img_src']).extract(),
                vendor_name='Adafruit',
                vendor_product_id=info.xpath(self.xpath_for['vendor_product_id']).extract())
