import mysql.connector
import requests
import json

db = mysql.connector.connect(
	user='user',
	passwd='password',
	host='host',
	db='db',
	auth_plugin='mysql_native_password'
)
cursor = db.cursor()

connpassAPI = "https://connpass.com/api/v1/event?order=2&count=20";
contents = requests.get(connpassAPI).json()
event = contents['events']

for i in range(0, 20):
	title = event[i]['title']
	link  = event[i]['event_url']

	query = "INSERT INTO event_list (title, url) \
	SELECT * FROM (SELECT '" + title + "', '" + link + "') AS tmp \
	WHERE NOT EXISTS \
	(SELECT * FROM event_list WHERE url = '" + link + "') LIMIT 1;"

	try:
		cursor.execute(query)
		db.commit()
		print("MySQL Success: Data inserted!!")
	except mysql.connector.Error as e:
		print("MySQL Error: ", e, query)
		

cursor.close()
db.close()
