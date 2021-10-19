import scrapy
from ..items import GraveItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class MenheraSpider(scrapy.Spider):
	allowed_domains = ['www.']