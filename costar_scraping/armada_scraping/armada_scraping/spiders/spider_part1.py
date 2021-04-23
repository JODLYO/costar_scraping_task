import scrapy
import time
from ..items import ArmadaScrapingItem


class ForSaleSpyder(scrapy.Spider):
    name = 'ForSale'
    url = 'https://www.armadarealestate.com/inventory.aspx?propertyId=248786-sale'
    start_urls = [url]

    def __init__(self):
        self.current_url = 'https://www.armadarealestate.com/inventory.aspx?propertyId=248786-sale'
        self.transaction_type = 'For Sale'  # will change for lease properties
        self.sale_stage = 'available'  # not sure when this is not the case
        self.lang = ''

    def get_lang(self):
        self.lang = self.lang[self.lang.find('lang'):]
        self.lang = self.lang[self.lang.find('\"') + 1:]
        self.lang = self.lang[:self.lang.find('\"')]

    def parse(self, response):
        token = response.xpath('//*[@id="dnn_ctr500_HtmlModule_lblContent"]/script[last()]').get()
        token = self.clean_token(token)
        plugin_start = 'https://buildout.com/plugins/'
        arm_r_e = 'www.armadarealestate.com/'
        inv = 'inventory/'
        prop_id_sl = self.current_url[self.current_url.find('=') + 1:]
        other_url = '?pluginId=0&amp;iframe=true&amp;embedded=true&amp;cacheSearch=true&amp;propertyId='
        url = plugin_start + token + '/' + arm_r_e + inv + prop_id_sl + other_url + prop_id_sl
        self.lang = response.xpath('/html[1]').extract()[0][:100]
        self.get_lang()
        yield scrapy.Request(url, callback=self.parse_iframe)

    def parse_iframe(self, response):
        items = ArmadaScrapingItem()
        scraped_at = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        address_list = response.xpath('//*[@class="header-text"]/div/text()').extract()
        building_name = address_list[0]
        address = ', '.join(address_list)
        description = response.xpath('/ html / head / meta[last()]').extract()
        lat_long = response.xpath('//*[@id="mapContainer"]').extract()[0]
        lat, long = self.get_lat_long(lat_long)
        price_type_size = response.xpath('//*[@id="overview"]//table[@class="table striped"]//tr//text()').extract()
        price, type, size = self.get_price_type_size(price_type_size)
        contacts = response.xpath('//*[@id="overview"]//table[@class="js-broker"]//tr//text()').extract()
        contacts_dict = self.get_contacts_dict(contacts)
        brochure_link = response.xpath('//*[@id="overview"]//div[@class="bottom-buffer-md"]//a/@href').extract()

        items['scraped_at'] = scraped_at
        items['address'] = address
        items['building_name'] = building_name
        items['description'] = description
        items['latitude'] = lat
        items['longitude'] = long
        items['url'] = self.current_url
        items['transaction_type'] = self.transaction_type
        items['size'] = size
        items['contacts'] = contacts_dict
        items['sale_or_rent'] = price
        items['brochure_link'] = brochure_link
        items['language'] = self.lang
        yield items

    def get_contacts_dict(self, contacts):
        return {'name': contacts[0],
                'telephone': contacts[3:],
                'email': contacts[2]}

    def get_lat_long(self, lat_long):
        lat = lat_long[lat_long.find('data-latitude'):]
        lat = lat[lat.find('\"') + 1:]
        lat = lat[:lat.find('\"')]
        long = lat_long[lat_long.find('data-longitude'):]
        long = long[long.find('\"') + 1:]
        long = long[:long.find('\"')]
        return lat, long

    def get_price_type_size(self, price_type_size):
        price = price_type_size[1]
        type = price_type_size[3]
        size = price_type_size[5]
        return price, type, size

    def clean_token(self, token):
        token = token[token.find('token:'):]
        token = token[token.find('\"') + 1:]
        token = token[:token.find('\"')]
        return token
