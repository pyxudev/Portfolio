import mysql.connector
from .items import ItmediaItem

class ItmediaPipeline:    
    def open_spider(self, spider):
        self.db = mysql.connector.connect(
            user='root',
            passwd='passwrd',
            host='localhost',
            db='dbname',
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.db.cursor()
        print(self.cursor)

    def close_spider(self, spider):
        print('end')
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        title = item['title']
        link = item['link']   
        print(title)
        print(link)
        query = "INSERT INTO news_list (title, url) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, tuple([title, link]))
            self.db.commit()
            print("MySQL Success: Data inserted!!")
        except mysql.connector.Error as e:
            print("MySQL Error: ", e, query)
    
