import re
import csv
from .items import YogaItem
from itemadapter import ItemAdapter

class YogaPipeline:
	def open_spider(self, spider):
		print("spider started")
		self.count = 1
		self.filename = open('yogaroom.csv', mode='w')
		self.csv_analysis = csv.writer(self.filename, quoting=csv.QUOTE_MINIMAL)
		self.csv_analysis.writerow(["所在地", "URL", "店舗名", "住所", "電話番号"])

	
	def close_spider(self, spider):
		print("spider closed")
		self.filename.close()

	def process_item(self, item, spider):
		print(item)
		if isinstance(item, YogaItem):
			self.csv_analysis.writerow([item['Ken'], item['URL'], item['Name'], item['Address'], item['Number']])