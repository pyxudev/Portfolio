import scrapy

class GoogleItem(scrapy.Item):
	Score        = scrapy.Field()
	User_url     = scrapy.Field()
	Cols         = scrapy.Field()
	Rows         = scrapy.Field()
	Type         = scrapy.Field()
	Deadline     = scrapy.Field()
	Gap_date     = scrapy.Field()
	Uuid         = scrapy.Field()

class DevItem(scrapy.Item):
	Score        = scrapy.Field()
	User_url     = scrapy.Field()
	Cols         = scrapy.Field()
	Rows         = scrapy.Field()
	Deadline     = scrapy.Field()
	Uuid         = scrapy.Field()
	Task_name    = scrapy.Field()
