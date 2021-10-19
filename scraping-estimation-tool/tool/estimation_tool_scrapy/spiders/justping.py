import scrapy
from ..items import SpeedScoreItem
import re
import json
import codecs
from scrapy.http import HtmlResponse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError,TimeoutError, TCPTimedOutError
import time

class JustpingSpider(scrapy.Spider):
	name = 'justping'
	allowed_domains = ['asm.ca.com','amazon.com','facebook.com','joshinweb.jp']
	start_urls = ['https://asm.ca.com/en/ping.php']
	values_dict = dict()
	start_page = 1
	tor_count = 0

	def parse(self, response):
		print(response.url)
		vsec = response.css("#page_sectoken::attr(value)").extract_first()
		vtt = response.css("#vtt::attr(value)").extract_first()
		print(vsec)
		print(vtt)
		yield scrapy.FormRequest(
			url=response.url, 
			callback=self.parse_page, 
			method='POST', 
			formdata={'varghost': 'www.facebook.com','vhost': '_','vaction': 'ping','ping': 'Start','vtt': vtt,'vsectoken': vsec},
		)
		

	def parse_page(self, response):
		print(response.url)
		# print(response.body.decode("utf-8"))
		# data_regex = re.compile(r'data:(.*),[\s\S]*?errors')
		data_regex = re.compile(r"uid=(.*)',")
		data_regex2 = re.compile(r", t: (.*) },")
		data_item = data_regex.findall(codecs.decode(response.body, encoding='utf-8', errors='ignore'))
		data_item2 = data_regex2.findall(codecs.decode(response.body, encoding='utf-8', errors='ignore'))

		print(data_item[0])
		print(data_item2[0])

		yield scrapy.FormRequest(
			url='https://asm.ca.com/en/api/pingproxy.php?uid='+data_item[0], 
			callback=self.parse_dict, 
			method='POST', 
			# formdata={'uid': str(data_item[0]) ,'host':'www.utaten.com','t':str(data_item2[0])},
			formdata={'host':'www.facebook.com','t':str(data_item2[0])},
			errback = self.errback_httpbin,
			meta = {'uid' : data_item[0]}
		)

	def parse_dict(self, response):

		print(response.url)

		data_dict = json.loads(response.body.decode("utf-8"))

		yield scrapy.Request(
			url='https://asm.ca.com/en/api/pingproxy.php?uid='+response.meta['uid']+'&host=www.facebook.com&v=1', 
			callback=self.parse_real,
			method='GET', 
			errback = self.errback_httpbin,
			meta = {'uid' : response.meta['uid']}
		)

	def parse_real(self,response):

		# print(response.url)

		data_dict = json.loads(response.body.decode("utf-8"))

	
		if len(self.values_dict) < 50 :
			self.values_dict.update(data_dict['r'])
			self.start_page = self.start_page + 1 
			yield scrapy.Request(
				url='https://asm.ca.com/en/api/pingproxy.php?uid='+response.meta['uid']+'&host=www.facebook.com&v='+str(self.start_page), 
				callback=self.parse_real,
				method='GET', 
				errback = self.errback_httpbin,
				meta = {'uid' : response.meta['uid']}
			)
		elif len(self.values_dict) >= 50 :

			print(len(self.values_dict))
			self.calculate(self.values_dict)

		else :
			print(response.body)

		yield scrapy.Request(
				url='https://asm.ca.com/en/ping.php', 
				callback=self.tor_block,
				method='GET', 
				errback = self.errback_httpbin,
				meta = {'url' : 'https://www.amazon.com/'},
				dont_filter=True
			)

	def tor_block(self,response):
		
		if self.tor_count < 5:
			self.tor_count = self.tor_count + 1
			for i in range(10):
				yield scrapy.Request(url=response.meta['url'],
								callback=self.tor_block,method='GET',errback=self.errback_httpbin,dont_filter=True,
								meta={"proxy": "http://127.0.0.1:8118",'url':response.meta['url']})



	def calculate(self,data):

		countries = {'bl':'India - Bangalore (inblr01)','j2':'Japan - Tokyo (jptok02)',
		'i4':'Italy - Milan (itmil01)','k2':'Denmark - Copenhagen (dkcph02)',
		'jo':'South Africa - Johannesburg (zajnb01)','d5':'Germany - Berlin (deber01)',
		'id':'Indonesia - Jakarta (idjkt02)','ki':'Israel - Kiryat-Matalon (ilktm02)',
		'z4':'South Africa - Cape Town (zacpt02)','du':'Ireland - Dublin (iedub03)',
		'u4':'Ukraine - Kharkov (uahrk02)','rm':'Russian Federation - Moscow (rumow02)',
		'gb':'United Kingdom - Edinburgh (gbedi01)','lt':'Lithuania - Vilnius (ltvno02)',
		'f5':'France - Paris (frpar04)','m2':'Australia - Melbourne (aumel04)',
		'o2':'Norway - Oslo (noosl03)','m3':'Canada - Montreal (camtr03)',
		'g3':'United Kingdom - London (gblon03)','h3':'China - Hong Kong (hkhkg03)',
		'ct':'Canada - Toronto (cator03)','cs':'United States - Charleston (uschs01)',
		's1':'United States - San Antonio (usstx01)','s4':'United States - Seattle (ussea04)',
		'l5':'United States - Ashburn (usabn08)','jw':'Singapore - Singapore (sgsin04)',
		'la':'United States - Los Angeles (uslax03)','im':'India - Mumbai (inbom03)',
		'sy':'Australia - Sydney (ausyd05)','zu':'Switzerland - Zurich (chzrh02)',
		'sp':'Brazil - Sao Paulo (brsao05)','c1':'United States - Council Bluffs (uscbl01)',
		'ee':'Netherlands - Eemshaven (nleem01)','df':'Germany - Frankfurt (defra05)',
		'ha':'Finland - Hammina, Finland (fiham01)','sb':'Belgium - St. Ghislain (bestg01)',
		's5':'United States - Santa Clara (usscz04)','sk':'Korea, Republic of - Seoul (krsel02)',
		'c5':'India - Chennai (inche01)','c6':'United Kingdom - Cardiff (gbcar01)',
		'c7':'United States - Cheyenne (usche01)','vc':'Canada - Vancouver (cavan04)',
		'bz':'Australia - Brisbane (aubne03)','vt':'Viet Nam - Ho Chi Minh City (vnsgn03)',
		'gc':'Greece - Athens (grath02)','ep':'Spain - Madrid (esmad03)','pr':'Portugal - Lisbon (ptlis03)',
		'ti':'Turkey - Istanbul (trist03)','ub':'United States - Ashburn (usabn09)',
		'll':'United States - Los Angeles (uslax04)','ci':'United States - Charleston (uschs02)'}

		min_rtt_list = []
		max_rtt_list = []
		avg_rtt_list = []
		# print(data)

		for key,val in data.items():

			min_rtt_list.append(float(val['result'].get('min',0)))
			max_rtt_list.append(float(val['result'].get('max',0)))
			avg_rtt_list.append(float(val['result'].get('avg',0)))

			print('country:' , countries.get(key,''))
			print('IP:',val['result'].get('ip',''))
			print('status:' , val['status'])
			print('message:' , val['result'].get('message',''))

		min_rtt = sum(min_rtt_list)/len(min_rtt_list)
		max_rtt = sum(max_rtt_list)/len(max_rtt_list)
		avg_rtt = sum(avg_rtt_list)/len(avg_rtt_list)


		print('Minimum RTT',min_rtt,'ms' )
		print('Maximum RTT',max_rtt,'ms')
		print('Average RTT',avg_rtt,'ms' )
		

	def errback_httpbin(self, failure):


		# log all failures
		self.logger.error(repr(failure))
		# in case you want to do something special for some errors,
		# you may need the failure's type:
		if failure.check(HttpError):
			# these exceptions come from HttpError spider middleware
			# you can get the non-200 response
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)
			self.tor_checking(failure,response.url)
		elif failure.check(DNSLookupError):
			# this is the original request
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)
			self.tor_checking(failure,request.url)
		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)
			self.tor_checking(failure,request.url)

	def tor_checking(self,failure,url):

		print('Tor Checking')
		print('Error Occured:',repr(failure))
		print('Error on:',url)