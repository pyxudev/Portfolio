import re
import sys
import math
import json
import scrapy
from ..items import DevItem
from ..items import GoogleItem
from scrapy.exceptions import UsageError

class SpeedSpider(scrapy.Spider):
	name                                 = 'speed_score'
	allowed_domains                      = ['developers.google.com','www.googleapis.com']
	start_urls                           = ['https://developers.google.com/speed/pagespeed/insights/']

	def __init__(self, *args, **kwargs):
		super(SpeedSpider, self).__init__(*args, **kwargs)

	def parse(self, response):
		url                              = response.url
		
		if hasattr(self, 'user_url'):
			user_url                     = self.user_url
			if user_url[0:4]            != 'http':
				user_url                 = 'https://' + user_url
			if hasattr(self, 'cols'):
				cols                     = self.cols
				if hasattr(self, 'rows'):
					rows                 = self.rows
					if hasattr(self, 'task_type'):
						task_type        = self.task_type
						if hasattr(self, 'deadline'):
							deadline     = self.deadline
							if hasattr(self, 'gap_date'):
								gap_date = self.gap_date
								if hasattr(self, 'uuid'):
									uuid = self.uuid

									yield scrapy.FormRequest(
										url      = url, 
										callback = self.get_estimate,
										method   = 'GET', 
										formdata = {
											'url': user_url, 
											'tab': 'mobile' },
										meta	 = {'user_url'     : user_url,
													'cols'         : cols,
													'rows'         : rows,
													'task_type'    : task_type,
													'deadline'     : deadline,
													'gap_date'     : gap_date,
													'uuid'         : uuid}
													)

								else:
									raise UsageError("Invalid --uuid value, use uuid=VALUE(str)")
							else:
								raise UsageError("Invalid --gap_date value, use gap_date=VALUE(str)")
						else:
							raise UsageError("Invalid --times value, use times=VALUE(str)")
					else:
						raise UsageError("Invalid --task_type value, use task_type=VALUE(str)")
				else:
					raise UsageError("Invalid --rows value, use rows=VALUE(str)")
			else:
				raise UsageError("Invalid --cols value, use cols=VALUE(str)")
		else:
			raise UsageError("Invalid --user_url value, use user_url=VALUE(str)")

	def get_estimate(self, response):
		url                  = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
		key                  = 'AIzaSyAwlPiPJIkTejgqqH01v9DmtPoPeOPXDUQ'
		user_url             = response.meta['user_url']
		cols                 = response.meta['cols']
		rows                 = response.meta['rows']
		task_type            = response.meta['task_type']
		deadline             = response.meta['deadline']
		gap_date             = response.meta['gap_date']
		uuid                 = response.meta['uuid']
	
		yield scrapy.FormRequest(
			url              = url, 
			formdata         = {
				'key'      : key, 
				'locale'   : 'en_US', 
				'url'      : user_url, 
				'strategy' : 'desktop'
			}, 
			method           = 'GET', 
			headers          = {
				'Referer'  : response.url,
			}, 
			callback         = self.get_score,
			meta             = {'user_url'      : user_url,
								'cols'          : cols,
								'rows'          : rows,
								'task_type'     : task_type,
								'deadline'      : deadline,
								'gap_date'      : gap_date,
								'uuid'          : uuid}
		)

	def get_score(self, response):
		data_dict            = json.loads(response.body.decode("utf-8"))
		score                = data_dict['lighthouseResult']['categories']['performance']['score']
		page_speed_score     = 0

		if score is not None:
			page_speed_score = score * 100
		
		item                 = GoogleItem()
		item['Score']        = page_speed_score
		item['User_url']     = response.meta['user_url']
		item['Cols']         = response.meta['cols']
		item['Rows']         = response.meta['rows']
		item['Type']         = response.meta['task_type']
		item['Deadline']     = response.meta['deadline']
		item['Gap_date']     = response.meta['gap_date']
		item['Uuid']         = response.meta['uuid']

		return item

class DevSpider(scrapy.Spider):
	name                                 = 'dev_score'
	allowed_domains                      = ['developers.google.com','www.googleapis.com']
	start_urls                           = ['https://developers.google.com/speed/pagespeed/insights/']

	def __init__(self, *args, **kwargs):
		super(DevSpider, self).__init__(*args, **kwargs)

	def parse(self, response):
		url                              = response.url
		
		if hasattr(self, 'user_url'):
			user_url                     = self.user_url
			if user_url[0:4]            != 'http':
				user_url                 = 'https://' + user_url
			if hasattr(self, 'task_name'):
				task_name                     = self.task_name
				if hasattr(self, 'cols'):
					cols                     = self.cols
					if hasattr(self, 'rows'):
						rows                 = self.rows
						if hasattr(self, 'deadline'):
							deadline         = self.deadline
							deadline         = math.floor(float(deadline))
							if hasattr(self, 'uuid'):
								uuid = self.uuid

								yield scrapy.FormRequest(
									url      = url, 
									callback = self.dev_estimate,
									method   = 'GET', 
									formdata = {
										'url': user_url, 
										'tab': 'mobile' },
									meta	 = {'user_url'     : user_url,
												'task_name'    : task_name,
												'cols'         : cols,
												'rows'         : rows,
												'deadline'     : deadline,
												'uuid'         : uuid}
												)
							else:
								raise UsageError("Invalid --uuid value, use uuid=VALUE(str)")
						else:
							raise UsageError("Invalid --deadline value, use deadline=VALUE(str)")
					else:
						raise UsageError("Invalid --rows value, use rows=VALUE(str)")
				else:
					raise UsageError("Invalid --cols value, use cols=VALUE(str)")
			else:
					raise UsageError("Invalid --task_name value, use task_name=VALUE(str)")
		else:
			raise UsageError("Invalid --user_url value, use user_url=VALUE(str)")

	def dev_estimate(self, response):
		url                  = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
		key                  = 'AIzaSyAwlPiPJIkTejgqqH01v9DmtPoPeOPXDUQ'
		user_url             = response.meta['user_url']
		task_name            = response.meta['task_name']
		cols                 = response.meta['cols']
		rows                 = response.meta['rows']
		deadline             = response.meta['deadline']
		uuid                 = response.meta['uuid']
	
		yield scrapy.FormRequest(
			url              = url, 
			formdata         = {
				'key'      : key, 
				'locale'   : 'en_US', 
				'url'      : user_url, 
				'strategy' : 'desktop'
			}, 
			method           = 'GET', 
			headers          = {
				'Referer'  : response.url,
			}, 
			callback         = self.dev_score,
			meta	 = {'user_url'     : user_url,
						'task_name'    : task_name,
						'cols'         : cols,
						'rows'         : rows,
						'deadline'     : deadline,
						'uuid'         : uuid}
						)

	def dev_score(self, response):
		data_dict            = json.loads(response.body.decode("utf-8"))
		score                = data_dict['lighthouseResult']['categories']['performance']['score']
		page_speed_score     = 0

		if score is not None:
			page_speed_score = score * 100
		
		item                 = DevItem()
		item['Score']        = page_speed_score
		item['User_url']     = response.meta['user_url']
		item['Task_name']    = response.meta['task_name']
		item['Cols']         = response.meta['cols']
		item['Rows']         = response.meta['rows']
		item['Deadline']     = response.meta['deadline']
		item['Uuid']         = response.meta['uuid']
		item['user_url']     = response.meta['user_url']


		return item