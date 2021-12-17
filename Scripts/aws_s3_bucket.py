#coding: UTF-8
import feedparser
import json
from pathlib import Path
import boto3

data = feedparser.parse('https://dev.classmethod.jp/category/business/bigdata/feed/')

# print(data.keys())

list_feed = data['feed']['title']
list_author = []
for e in data['entries']:
	list_author.append(e['author'])
list_description = data['feed']['subtitle']

data ={
	'feed': list_feed,
	'dc:creator':list_author,
	'description':list_description
}

f = open('./data.json', 'w', encoding="utf=8_sig")
json.dump(data, f, indent=4, ensure_ascii=False)


BUCKET = '[bucket_name]'
KEY = '[access_key]'
s3 = boto3.client('s3')

#upload
s3.upload_file('./data.json', './')

#pre-signed-url
url = s3.generate_presigned_url(
	ClientMethod = 'put_object',
	Params = {'Bucket' : BUCKET, 'Key' : KEY},
	ExpiresIn = 3600,
	HttpMethod = 'PUT')

print(url)