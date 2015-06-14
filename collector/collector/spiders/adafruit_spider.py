import scrapy
import logging


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
            parsed = {
                'name': self.parse_product_name(info),
                'url': response.url,
                'image_url': response.urljoin(self.parse_product_image_url(info)),
                'vendor_name': 'Adafruit',
                'vendor_product_id': self.parse_product_vendor_id(info)
            }
            logging.info(parsed)

    @staticmethod
    def parse_product_name(product_info):
        xpath = '//div[@id="prod-right-side"]/h1/text()'
        try:
            detail = product_info.xpath(xpath)[0]
        except IndexError:
            return None
        return detail.extract().strip()

    @staticmethod
    def parse_product_image_url(product_info):
        xpath = '//div[@id="prod-primary-img-container"]//img/@src'
        try:
            detail = product_info.xpath(xpath)[0]
        except IndexError:
            return None
        return detail.extract().strip()

    @staticmethod
    def parse_product_vendor_id(product_info):
        xpath = '//div[@class="product_id"]/text()'
        try:
            detail = product_info.xpath(xpath)[0]
            parts = detail.extract().split(':')
            return parts[1].strip()
        except IndexError:
            return None
