# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpcrawlerItem(scrapy.Item):
    # subCategory = scrapy.Field()
    category = scrapy.Field()
    priceRange = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    address = scrapy.Field()
    hours = scrapy.Field()
    attributes = scrapy.Field()
    reviews = scrapy.Field()
    score = scrapy.Field()
    link = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    page = scrapy.Field()
    rank = scrapy.Field()
