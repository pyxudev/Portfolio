# -*- coding: utf-8 -*-



import scrapy

class SpeedScoreItem(scrapy.Item):
    
    page_speed_score = scrapy.Field()
    spider = scrapy.Field()
    domain = scrapy.Field()

class TestMySiteItem(scrapy.Item):

    spider = scrapy.Field()
    domain = scrapy.Field()
    first_byte_value = scrapy.Field()
    complete_load_value = scrapy.Field()
    is_https_value = scrapy.Field()
    is_http_2_value = scrapy.Field()
    status_value = scrapy.Field()
    connect_value = scrapy.Field()

class WoorankItem(scrapy.Item):
    
    spider = scrapy.Field()
    domain = scrapy.Field()
    overall_score = scrapy.Field()
    inpage_links = scrapy.Field()
    ip = scrapy.Field()
    doctype = scrapy.Field()
    encoding = scrapy.Field()
    custom_404 = scrapy.Field()
    language = scrapy.Field()
    url_parameters = scrapy.Field()
    discovered_pages = scrapy.Field()
    traffic_estimation = scrapy.Field()
    traffic_rank = scrapy.Field()

class IpItem(scrapy.Item):

    spider = scrapy.Field()
    domain = scrapy.Field()
    city = scrapy.Field()
    isp = scrapy.Field()
    country_name = scrapy.Field()
    company = scrapy.Field()
    time_zone = scrapy.Field()
    region_name = scrapy.Field()
    
