import scrapy


class TorSpider(scrapy.Spider):
	name = 'tor'
	allowed_domains = ['httpbin.org']
#	start_urls = ['https://httpbin.org/ip/']

	def start_requests(self):
		yield scrapy.Request(url = 'https://httpbin.org/ip', callback = self.get_ips)
		print("123")

	def get_ips(self, response):
		print(response.body)
