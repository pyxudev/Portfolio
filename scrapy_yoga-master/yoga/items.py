import scrapy

class YogaItem(scrapy.Item):
	Name	= scrapy.Field()
	Address = scrapy.Field()
	Number 	= scrapy.Field()
	URL		= scrapy.Field()
	Ken		= scrapy.Field()