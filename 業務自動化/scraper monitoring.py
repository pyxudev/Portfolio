from sshtunnel import SSHTunnelForwarder
import mysql.connector as mysql
import datetime

order = input("1=today, 2=another date\n")
if order == "1":
	today = datetime.date.today()
	yesterday = today - datetime.timedelta(days=1)
else:
	alt_date = input("enter yyyy-mm-dd\n")
	yesterday = datetime.date(int(alt_date[0:4]), int(alt_date[5:7]), int(alt_date[8:]))
	today = yesterday + datetime.timedelta(days=1)

project_name = ['eiga', 'filmarks', 'famitsu', 'nicovideo', 'googleplay', 'yahoo_eiga']
status_code = ['Success', 'Scraping Complete with Error', 'Error']

log_file = './sony2_report_' + str(yesterday) + '.txt'
file = open(log_file, 'w', encoding='UTF-8')
file.write("SGS sony2 report\n")
file.close()

DB_HOST='dbhost'
DB_PORT=3306
DB_NAME='dbname'
ROOT_USER='dbuser'
ROOT_PASSWORD='dbpw'

con = mysql.connect(
	host=DB_HOST,
	port=DB_PORT,
	database=DB_NAME,
	user=ROOT_USER,
	password=ROOT_PASSWORD,
	charset='utf8'
)

for project in project_name:
	for status in status_code:
		eig = ['name_1', 'name_2']
		fmk = ['name_1', 'name_2', 'name_3']
		fmt = ['name_1', 'name_2', 'name_3']
		nic = ['name_1', 'name_2', 'name_3', 'name_4']
		ggp = ['name_1', 'name_2']
		yhe = ['name_1', 'name_2', 'name_3', 'name_4']
		if project == 'spider_name1':
			temp = eig
		elif project == 'spider_name2':
			temp = fmk
		elif project == 'spider_name3':
			temp = fmt
		elif project == 'spider_name4':
			temp = nic
		elif project == 'spider_name5':
			temp = ggp
		elif project == 'spider_name6':
			temp = yhe

		query = "select count(*),spider from [table_name] where project='{project}' and status='{status}' and time_ended > '{yesterday}' and time_ended < '{today}' GROUP BY spider;\n".format(project=project, status=status, yesterday=yesterday, today=today)
		cursor = con.cursor()
		cursor.execute(query)
		data = cursor.fetchall()
		file = open(log_file, 'a', encoding='UTF-8')

		if len(data) < 1:
			result = [0]*len(temp)
		else:
			for d in data:
				d1 = d[1]
				d0 = d[0]
				if project == project_name[0]:
					eig = [d0 if value==d1 else value for value in eig]
					result = eig
				elif project == project_name[1]:
					fmk = [d0 if value==d1 else value for value in fmk]
					result = fmk
				elif project == project_name[2]:
					fmt = [d0 if value==d1 else value for value in fmt]
					result = fmt
				elif project == project_name[3]:
					nic = [d0 if value==d1 else value for value in nic]
					result = nic
				elif project == project_name[4]:
					ggp = [d0 if value==d1 else value for value in ggp]
					result = ggp
				elif project == project_name[5]:
					yhe = [d0 if value==d1 else value for value in yhe]
					result = yhe

		for res in result:
			if res in temp:
				res = 0
			file.write('{res}\n'.format(res=res))

	file.write('\n')

file.write('Update users\n')

query = "select count(*) from [user_table] where is_registered and last_updated > '{yesterday}' and last_updated < '{today}';\n".format(yesterday=yesterday, today=today)
cursor = con.cursor()
cursor.execute(query)
data = cursor.fetchall()
for d in data:
	file.write('{d0}\n'.format(d0=d[0]))

file.close()
print("done")
con.close()