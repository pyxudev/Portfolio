import re
import sys
import json
import scrapy
from ..items import YogaItem
from scraper_api import ScraperAPIClient
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class YogaSpider(scrapy.Spider):
	name            = 'yoga'
	allowed_domains = ['www.yogaroom.jp', 'api.scraperapi.com']
	error_page = open('error_page.log', 'a')
	client = ScraperAPIClient('****')
	
	def start_requests(self):
		url_list = {
					'大阪' : 'https://www.yogaroom.jp/studio/kinki/osaka',
					'京都' : 'https://www.yogaroom.jp/studio/kinki/kyoto',
					'滋賀' : 'https://www.yogaroom.jp/studio/kinki/shiga',
					'兵庫' : 'https://www.yogaroom.jp/studio/kinki/hyogo',
					'奈良' : 'https://www.yogaroom.jp/studio/kinki/nara',
					'福岡' : 'https://www.yogaroom.jp/studio/kyushu/fukuoka',
					'和歌山' : 'https://www.yogaroom.jp/studio/kinki/wakayama'}

		for key, value in url_list.items():
			meta = {
					'prefecture': key}
			yield scrapy.Request(
				self.client.scrapyGet(
					url 	 = value),
					meta	 = meta,
					callback = self.get_details,
					errback=self.errback_httpbin)

	def get_details(self, response):
		url 		 		 = 'https://www.yogaroom.jp'
		result_list  		 = response.css('div.search-result div.content-studio a.studio::attr(href)').extract()

		for res in result_list:
			form_url 	 	 = url + res
			meta 			 = {
								'prefecture' : response.meta['prefecture'],
								'url'		 : form_url}
			yield scrapy.Request(
				self.client.scrapyGet(
					url 	 = form_url),
					callback = self.get_form,
					meta	 = meta,
					errback  = self.errback_httpbin)

	def get_form(self, response):
		item 				 = YogaItem()
		item['Name'] 		 = None 
		item['Address'] 	 = None
		item['Number'] 		 = None
		item['Ken']			 = None
		item['URL'] 		 = None

		addr 				 = None
		num 				 = None

		dl_list 			 = response.css('div.data dl')
		for dl in dl_list:
			dt 				 = self._filter_text(dl.css('dt::text').extract_first())
			if dt 			 == '住所':
				addr 		 = self._filter_text(dl.css('dd::text').extract())
			if dt 			 == '電話番号':
				num			 = self._filter_text(dl.css('dd::text').extract_first())

		item['Name'] 		 = self._filter_text(response.css('h2.page-title::text').extract_first())
		item['URL'] 	 	 = response.meta['url']
		item['Ken'] 		 = response.meta['prefecture']
		item['Address'] 	 = addr
		item['Number'] 		 = num

		yield item

	def  _filter_text(self, text):
		if isinstance(text, list):
			if len(text) > 0:	
				return self._filter_text((' ').join(text))
			return None
		else:
			if text  == None:
				return None
			else:
				text = text.replace(u'\\n', u'')
				text = text.replace(u'\\t', u'')
				text = text.replace(u'\\r', u'')
				text = text.replace(u'<br>', u'')
				text = text.replace(u'\u3000', u'')
				text = ' '.join(text.split())
			# return ''.join(text).strip()
		return text

	def errback_httpbin(self, failure):
		self.logger.error(repr(failure))

		if failure.check(HttpError):
			response = failure.value.response
			self.error_page.write(response.url + '\n')
			self.logger.error('HttpError on %s', response.url)

		elif failure.check(DNSLookupError):
			request = failure.request
			self.error_page.write(request.url + '\n')
			self.logger.error('DNSLookupError on %s', request.url)

		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.error_page.write(request.url + '\n')
			self.logger.error('TimeoutError on %s', request.url)