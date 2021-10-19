import json
import math
import datetime
import mysql.connector
from .items import DevItem
from .items import GoogleItem
from itemadapter import ItemAdapter

class GooglePipeline:
	def open_spider(self, spider):
		self.db        = mysql.connector.connect(
			host       = "host",
			user       = "user",
			password   = "password",
			database   = "dbname",
		)
		self.cursor    = self.db.cursor()
	
	def close_spider(self, spider):
		self.cursor.close()
		self.db.close()

	def process_item(self, item, spider):
		if isinstance(item, GoogleItem):
			created_at     = datetime.datetime.now()
			user_url       = item['User_url']
			task_type      = item['Type']
			cols           = item['Cols']
			rows           = item['Rows']
			score          = item['Score']
			deadline       = item['Deadline']
			gap_date       = item['Gap_date']
			uuid           = item['Uuid']
			cols           = int(cols)
			rows           = int(rows)
			gap_date       = math.floor(float(gap_date))
			result         = 0
			if gap_date    < 10:
				gap_date   = 5
			elif gap_date >= 25:
				gap_date   = 25

			w              = 0.9*math.log10(cols)+0.1*(math.log10(rows)/math.sqrt(gap_date/30))
			if score      >= 25:
				if w      <= 4.0:
					result = 100000
				elif w     > 4.0 and w <= 5.5:
					result = 200000
				elif w     > 5.5 and w <= 10.0:
					result = 300000
				elif w     > 10.0:
					result = 1000000
			elif score     < 25:
				if w      <= 4.0:
					result = 200000
				elif w     > 4.0 and w <= 5.5:
					result = 400000
				elif w     > 5.5 and w <= 10.0:
					result = 800000
				elif w     > 10.0:
					result = 1000000
					
			if task_type   == "一回きりの収集":
				query      = "INSERT INTO speed_score(created_at, user_url, task_type, cols, rows, score, deadline, result, uuid) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			elif task_type == "継続的に収集":
				query      = "INSERT INTO speed_score_periodical(created_at, user_url, task_type, cols, rows, score, deadline, result, uuid) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			
			try:
				self.cursor.execute(query, tuple([created_at, user_url, task_type, cols, rows, score, deadline, result, uuid]))
				self.db.commit()
			except mysql.connector.Error as e:
				print("MySQL Error: ", e, query)			
				

		elif isinstance(item, DevItem):
			created_at     = datetime.datetime.now()
			user_url       = item['User_url']
			name           = item['Task_name']
			cols           = item['Cols']
			rows           = item['Rows']
			score          = item['Score']
			deadline       = item['Deadline']
			uuid           = item['Uuid']
			cols           = int(cols)
			rows           = int(rows)
			deadline       = int(deadline)
			result         = 0

			w              = 0.9*math.log10(cols)+0.1*(math.log10(rows)/math.sqrt(deadline/30))
			if score      >= 25:
				if w      <= 4.0:
					result = 100000
				elif w     > 4.0 and w <= 5.5:
					result = 200000
				elif w     > 5.5 and w <= 10.0:
					result = 300000
				elif w     > 10.0:
					result = 1000000
			elif score     < 25:
				if w      <= 4.0:
					result = 200000
				elif w     > 4.0 and w <= 5.5:
					result = 400000
				elif w     > 5.5 and w <= 10.0:
					result = 800000
				elif w     > 10.0:
					result = 1000000

			print(uuid)
			
			query      = "INSERT INTO dev_speed(created_at, user_url, cols, rows, score, deadline, result, uuid, name) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

			try:
				self.cursor.execute(query, tuple([created_at, user_url, cols, rows, score, deadline, result, uuid, name]))
				self.db.commit()
			except mysql.connector.Error as e:
				print("MySQL Error: ", e, query)