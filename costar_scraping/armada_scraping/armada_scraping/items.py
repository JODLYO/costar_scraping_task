# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArmadaScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    scraped_at = scrapy.Field()
    address = scrapy.Field()
    building_name = scrapy.Field()
    description = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    url = scrapy.Field()
    transaction_type = scrapy.Field()
    size = scrapy.Field()
    contacts = scrapy.Field()
    sale_or_rent = scrapy.Field()
    brochure_link = scrapy.Field()
    language = scrapy.Field()

    pass
