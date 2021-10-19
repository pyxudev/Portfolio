import csv
import sqlite3
from .items import WoorankItem, TestMySiteItem, SpeedScoreItem, IpItem
import os,sys,inspect
import mysql.connector



class EstimationToolPipeline(object):
	
	def open_spider(self, spider):
		self.db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="Helloworld@12345",
			database="set_database",
			use_unicode=True, 
			charset="utf8"
		)
		
		self.cursor = self.db.cursor()

	def close_spider(self, spider):
		self.cursor.close()
		self.db.close()

	def process_item(self, item, spider):
		

		if isinstance(item, SpeedScoreItem):

			query = """INSERT INTO tool_domaininfo (domain, page_speed_score) VALUES (%s, %s) ON DUPLICATE KEY UPDATE page_speed_score=%s"""
			try:
				self.cursor.execute(query, tuple([item['domain'],item['page_speed_score'],item['page_speed_score']]))
				self.db.commit()
				print("MySQL Success: Data inserted!!")
			except mysql.connector.Error as e:
				print("MySQL Error: ", e, query)
			
			
		elif isinstance(item, TestMySiteItem):

			query = """INSERT INTO tool_domaininfo (domain, first_byte_time, complete_page_load_time, https_score, https_2_score, 
				page_status_score,connection_time) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE first_byte_time=%s,
				complete_page_load_time=%s, https_score=%s, https_2_score=%s, 
				page_status_score=%s, connection_time=%s"""
			try:
				self.cursor.execute(query, tuple([item['domain'],item['first_byte_value'],item['complete_load_value'], 
					item['is_https_value'],item['is_http_2_value'], item['status_value'],item['connect_value'], 
					item['first_byte_value'],item['complete_load_value'], 
					item['is_https_value'],item['is_http_2_value'], item['status_value'],item['connect_value']]))
				self.db.commit()
				print("MySQL Success: Data inserted!!")
			except mysql.connector.Error as e:
				print("MySQL Error: ", e, query)

		elif isinstance(item, WoorankItem):

			query = """INSERT INTO tool_domaininfo (domain, website_overall_score, in_page_links, ip, doc_type, encoding, custom_error_page, 
				language, url_parameters, discovered_pages, traffic_estimation, traffic_rank) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
				ON DUPLICATE KEY UPDATE website_overall_score=%s, in_page_links=%s, ip=%s, doc_type=%s, encoding=%s, custom_error_page=%s, 
				language=%s, url_parameters=%s, discovered_pages=%s, traffic_estimation=%s, traffic_rank=%s"""
			try:
				self.cursor.execute(query, tuple([item['domain'],item['overall_score'], 
					item['inpage_links'],item['ip'],item['doctype'], item['encoding'],item['custom_404'], 
					item['language'], item['url_parameters'],item['discovered_pages'], item['traffic_estimation'],
					item['traffic_rank'],item['overall_score'],item['inpage_links'],item['ip'],item['doctype'],
					item['encoding'],item['custom_404'],item['language'], item['url_parameters'], 
					item['discovered_pages'], item['traffic_estimation'],item['traffic_rank']]))
				self.db.commit()
				print("MySQL Success: Data inserted!!")
			except mysql.connector.Error as e:
				print("MySQL Error: ", e, query)

		elif isinstance(item, IpItem):

			query = """INSERT INTO tool_domaininfo (domain, city, isp, country, internet_company, timezone,region_name)
			 	VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE city=%s, isp=%s, country=%s, 
			 	internet_company=%s, timezone=%s, region_name=%s"""
			try:
				self.cursor.execute(query, tuple([item['domain'],item['city'],item['isp'],item['country_name'], 
					item['company'],item['time_zone'], item['region_name'],item['city'],item['isp'],item['country_name'], 
					item['company'],item['time_zone'], item['region_name']]))
				self.db.commit()
				print("MySQL Success: Data inserted!!")
			except mysql.connector.Error as e:
				print("MySQL Error: ", e, query)



		return item
		



		


