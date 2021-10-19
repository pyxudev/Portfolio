# -*- coding: utf-8 -*-
import scrapy
import sys
from ..items import SpeedScoreItem, WoorankItem, TestMySiteItem, IpItem
import re
import json
from scrapy.http import HtmlResponse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError,TimeoutError, TCPTimedOutError
import time




class SpeedScoreSpider(scrapy.Spider):
	name = 'speed_score'
	allowed_domains = ['developers.google.com','www.googleapis.com']

	start_urls = ['https://developers.google.com/speed/pagespeed/insights/']

	domain = None
	

	def __init__(self, *args, **kwargs):
		super(SpeedScoreSpider, self).__init__(*args, **kwargs) 
		self.domain = kwargs.get('domain', None)
		

	def parse(self, response):
		
		print(response.url)
		print(self.domain)

		if self.domain is not None:
			yield scrapy.FormRequest(
										url=response.url, 
										callback=self.parse_page, 
										method='GET', 
										formdata={'url': 'http://'+ self.domain , 'tab': 'mobile' }, 
										meta = {'url' : 'http://'+ self.domain}
									)

	def parse_page(self, response):
		
		key = 'AIzaSyAwlPiPJIkTejgqqH01v9DmtPoPeOPXDUQ'
		url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
		'''https://www.googleapis.com/pagespeedonline/v5/runPagespeed?key=AIzaSyAwlPiPJIkTejgqqH01v
		9DmtPoPeOPXDUQ&locale=en_US&url=http%3A%2F%2Fwww.makemytrip.com%2F&strategy=mobile'''
		
		yield scrapy.FormRequest(
										url=url, 
										callback=self.speed_score, 
										method='GET', 
										formdata={'key': key ,'locale':'en_US','url':response.meta['url'],'strategy': 'desktop'}, 
										headers={'Referer':response.url},
										errback = self.errback_httpbin
									)

		
		
		
	
	def speed_score(self, response):
		
		data_dict = json.loads(response.body.decode("utf-8"))
		score = data_dict['lighthouseResult']['categories']['performance']['score']

		page_speed_score = 0

		if score is not None:

			page_speed_score = score * 100 
		
		item = SpeedScoreItem()
		item['domain'] = self.domain
		item['spider'] = 'speed_score'
		item['page_speed_score'] = page_speed_score

		print(item)

		yield item

	

	def errback_httpbin(self, failure):
		
		self.logger.error(repr(failure))
		
		if failure.check(HttpError):
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)
		elif failure.check(DNSLookupError):
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)
		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)

	def filter_text(self, text):
		
		if text is None:
			text = '-'
		text = text.replace(u'\\u3000', u' ')
		text = text.replace(u'\\xa0', u' ')
		text = text.replace(u'\\n', u' ')
		text = text.replace(u'\\t', u' ')
		text = ' '.join(text.split())
		if text == '':
			text = '-'	
		return text

class TestmysiteSpider(scrapy.Spider):
	name = 'testmysite'
	allowed_domains = ['testmysite.io','api.netlify.com']
	domain = None
	
	def __init__(self, *args, **kwargs):
		super(TestmysiteSpider, self).__init__(*args, **kwargs) 
		self.domain = kwargs.get('domain', '')

	def start_requests(self):
		
		yield scrapy.FormRequest(
			
										url= 'https://api.netlify.com/api/v1/speed_tests',
										callback=self.parse_test, 
										method='POST', 
										formdata={'url': self.domain},
										errback = self.errback_httpbin,									
								)

	def parse_test(self,response):

		# print(response.url)
		# print(response.body)
		data_dict = json.loads(response.body.decode("utf-8"))
		new_url = response.url + '/' +data_dict['id']
		time.sleep(10)
		yield scrapy.Request(

										url= new_url,
										callback=self.testmysite,
										method='GET',
										errback=self.errback_httpbin
			)

	def testmysite(self,response):
		# print(response.url)
		data_dict = json.loads(response.body.decode("utf-8"))
		first_byte = []
		complete_load = []
		is_https = []
		is_http_2 = []
		connect = []
		status = []
		for value in data_dict['results'].values():
			first_byte.append(value['first_byte'])
			connect.append(value['connect'])
			status.append(value['status'])
			complete_load.append(value['complete_load'])
			is_https.append(value['is_https'])
			is_http_2.append(value['is_http_2'])

		first_byte_value = (sum(first_byte) / len(first_byte))/1000000
		connect_value = (sum(connect) / len(connect))/1000000
		complete_load_value = (sum(complete_load) / len(complete_load))/1000000
		is_https_value = (sum(is_https) / len(is_https))*100
		is_http_2_value = (sum(is_http_2) / len(is_http_2))*100
		status_value = (sum(status) / len(status))*100

		item = TestMySiteItem()
		item['domain'] = self.domain
		item['spider'] = 'testmysite'
		item['first_byte_value'] = first_byte_value
		item['complete_load_value'] = complete_load_value
		item['is_https_value'] = is_https_value
		item['is_http_2_value'] = is_http_2_value
		item['status_value'] = status_value
		item['connect_value'] = connect_value

		print(item)

		yield item

	def errback_httpbin(self, failure):
		
		self.logger.error(repr(failure))
		
		if failure.check(HttpError):
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)
		elif failure.check(DNSLookupError):
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)
		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)

	def filter_text(self, text):
		
		if text is None:
			text = '-'
		text = text.replace(u'\\u3000', u' ')
		text = text.replace(u'\\xa0', u' ')
		text = text.replace(u'\\n', u' ')
		text = text.replace(u'\\t', u' ')
		text = ' '.join(text.split())
		if text == '':
			text = '-'	
		return text

class WoorankSpider(scrapy.Spider):
	name = 'woorank'
	allowed_domains = ['www.woorank.com']
	domain = None
	
	def __init__(self, *args, **kwargs):
		super(WoorankSpider, self).__init__(*args, **kwargs) 
		self.domain = kwargs.get('domain', '')
		

	def start_requests(self):
		
		yield scrapy.FormRequest(
			
										url= 'https://www.woorank.com/en/www/'+self.domain,
										callback=self.metrics_page, 
										method='GET', 
										errback = self.errback_httpbin,
			)


	def metrics_page(self,response):
		
		overall_score = response.css('div.nr-review-summary-header span.jss76.jss77::text').extract_first()
		inpage_links = response.css('div.nr-review-links_details-crit div.jss157.jss158 span::text').extract_first()
		ip = response.css('div.nr-review-ip_information-crit div.jss157.jss158 p::text').extract_first()
		doctype = response.css('div.nr-review-doctype-crit div.jss157.jss158 span::text').extract_first()
		encoding = response.css('div.nr-review-encoding-crit div.jss157.jss158 span::text').extract_first()
		custom_404 = response.css('div.nr-review-custom_404-crit div.jss157.jss158 p::text').extract_first()
		language = response.css('div#criterium-language div.nr-review-language-crit div.jss157.jss158 p i::text').extract_first()
		url_parameters = response.css('div.nr-review-clean_url-crit div.jss157.jss158 span::text').extract_first()
		discovered_pages = response.css('div.nr-review-indexed_pages-crit div.jss157.jss158 div::text').extract_first()	
		traffic_estimation = response.css('div.nr-review-alexa-crit div.jss157.jss158 span::text').extract_first()
		traffic_rank = response.css('div.nr-review-trafic_ranking-crit div.jss157.jss158 strong::text').extract_first()
		
		item = WoorankItem()
		item['domain'] = self.domain
		item['spider'] = 'woorank'
		item['overall_score'] = self.filter_text(overall_score)
		item['inpage_links'] = self.filter_text(inpage_links)
		item['ip'] = self.filter_text(ip)
		item['doctype'] = self.filter_text(doctype)
		item['encoding'] = self.filter_text(encoding)
		item['custom_404'] = self.filter_text(custom_404)
		item['language'] = self.filter_text(language)
		item['url_parameters'] = self.filter_text(url_parameters)
		item['discovered_pages'] = self.filter_text(discovered_pages)
		item['traffic_estimation'] = self.filter_text(traffic_estimation)
		item['traffic_rank'] = self.filter_text(traffic_rank)

		print(item)

		yield item

	def errback_httpbin(self, failure):
		
		self.logger.error(repr(failure))
		
		if failure.check(HttpError):
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)
		elif failure.check(DNSLookupError):
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)
		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)

	def filter_text(self, text):
		
		if text is None:
			text = '-'
		text = text.replace(u'\\u3000', u' ')
		text = text.replace(u'\\xa0', u' ')
		text = text.replace(u'\\n', u' ')
		text = text.replace(u'\\t', u' ')
		text = ' '.join(text.split())
		if text == '':
			text = '-'	
		return text


		


class IpSpider(scrapy.Spider):
	name = 'ip'
	allowed_domains = ['iplocation.com']
	domain = None
	ip = None
	
	def __init__(self, *args, **kwargs):
		super(IpSpider, self).__init__(*args, **kwargs) 
		self.domain = kwargs.get('domain', None)
		self.ip = kwargs.get('ip', None)
		
	def start_requests(self):
		
		yield scrapy.FormRequest(
									url= 'https://iplocation.com/',
									callback=self.ipchecker,
									method='POST',
									errback=self.errback_httpbin,
									formdata={'ip':self.ip}
									)
	
	def ipchecker(self,response):
		
		item = IpItem()
		
		data_dict = json.loads(response.body.decode("utf-8"))
		item['city'] = self.filter_text(data_dict['city'])
		item['isp'] = self.filter_text(data_dict['isp'])
		item['country_name'] = self.filter_text(data_dict['country_name'])
		item['company'] = self.filter_text(data_dict['company'])
		item['time_zone'] = self.filter_text(data_dict['time_zone'])
		item['region_name'] = self.filter_text(data_dict['city'])
		item['domain'] = self.filter_text(self.domain)
		
		yield item

	def errback_httpbin(self, failure):
		
		self.logger.error(repr(failure))
		
		if failure.check(HttpError):
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)
		elif failure.check(DNSLookupError):
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)
		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)

	def filter_text(self, text):
		
		if text is None:
			text = '-'
		text = text.replace(u'\\u3000', u' ')
		text = text.replace(u'\\xa0', u' ')
		text = text.replace(u'\\xC5', u' ')
		text = text.replace(u'\\x8C', u' ')
		text = text.replace(u'\\n', u' ')
		text = text.replace(u'\\t', u' ')
		text = ' '.join(text.split())
		if text == '':
			text = '-'	
		return text