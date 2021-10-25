from sshtunnel import SSHTunnelForwarder
import mysql.connector as mysql
import datetime

today = datetime.date.today()
DB_HOST='***'
DB_PORT=3306
DB_NAME='****'
ROOT_USER='***'
ROOT_PASSWORD='***'

con = mysql.connect(
	host=DB_HOST,
	port=DB_PORT,
	database=DB_NAME,
	user=ROOT_USER,
	password=ROOT_PASSWORD,
	charset='utf8'
)

query = "select title, url, summary, publisher from {DB_NAME}.news where created_at > '{today}';\n".format(DB_NAME=DB_NAME ,today=today)
cursor = con.cursor()
cursor.execute(query)
data = cursor.fetchall()
temp = f"email_content.txt"
file = open(temp, 'w')

for d in data:
	content = f"{d[0]}\n{d[1]}\n{d[2]}\n{d[3]}\n \n"
	file.write(content)

file.close()
con.close()
