import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import lxml.html
from lxml.html import soupparser
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

 

def compute_total_files(url):

	session = requests.Session()

	session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"


	html = session.get(url).content


	soup = BeautifulSoup(html, "html.parser")

	script_files = []

	for script in soup.find_all("script"):
		if script.attrs.get("src"):
			
			script_url = urljoin(url, script.attrs.get("src"))
			script_files.append(script_url)

	print("Total script files in the page:", len(script_files))

	total_files = len(script_files)

	return total_files

def compute_difficulty(tag_list):

	js_difficulty = 2

	for tag in tag_list:
		soup = BeautifulSoup(tag,features="lxml")

		link_list = []
		event_list = []

		js_diff = 2

		for a in soup.find_all('a', href=True):
			link = a['href']
			link_list.append(link)
		for a in soup.find_all('a', onclick=True):
			link = a['onclick']
			event_list.append(link)
		if len(link_list) > 0:
			js_diff = 3
		if len(event_list) > 0 and len(link_list) > 0:
			js_diff = 5
		if len(event_list) > 0:
			js_diff = 4
		
		if js_difficulty < js_diff:
			js_difficulty = js_diff

	return js_difficulty


def js_data(url,xpath_list):

	
	total_js_files = compute_total_files(url)
	 
	page = requests.get(url, stream=True)
	# print(page.text)
	# soup = BeautifulSoup(page.text)
	sel = Selector(root=soupparser.fromstring(page.text))

	js_difficulty = 1

	for xpath_selector in xpath_list:

		tag_list = sel.xpath(xpath_selector).extract()
		js_diff = compute_difficulty(tag_list)
		if js_diff > js_difficulty:
			js_difficulty = js_diff

	js_data_dict = dict()
	js_data_dict['total_js_files'] = total_js_files
	js_data_dict['js_difficulty'] = js_difficulty

	return js_data_dict



	



# xpath_data = {
			
# 			'1':{
			
# 			'url':'https://www.amazon.com/events',
# 			'link':{
			
# 				'type':'link','xpath':'xpath_of_the_element'
# 			},
# 			'end_page':0
# 		},

# 			'2':{

# 			'url':'https://www.amazon.com/japan',
# 			'link':{
			
# 				'type':'link','xpath':'xpath_of_the_element'
# 			},
# 			'end_page':0
# 		},

# 			'3':{

# 				'url':'https://www.amazon.com/tokyo',
# 				'link':{
				
					
# 			},
# 			'end_page':1
# 		}
# 	}



	


	# print(soup)
	
	# response = requests.get(url, stream=True)
	# response.raw.decode_content = True
	# print(response.text)
	
	# tree = lxml.html.parse(response.raw)
	# links = tree.xpath(xpath_selector)
	# print(len(links))
	# links_count = len(links)
	# page_count = 10
	# level_count = get_count(links_count,page_count)
	# if end_page is True:
	# 	approximate_links_count(level_count)
	# else:
	# 	page_caller(link)
	# tree.xpath(xpathselector)
	# print(links[0].attrib['href'])

# def get_count(links_count,page_count):

# 	total_level_count = links_count * page_count
# 	total_count = earlier_count * total_level_count

# def page_caller(link):
# 	pass



# def approximate_links_count(level_count):
# 	pass



# link_data = {'url':'https://www.amazon.com/',
# 			'links':{
			
# 				'1':{'type':'link','link_flag':1,'href':'javascript:validate();','function':'validate','event_flag':0,'event':'-'},
# 				'2':{'type':'link','link_flag':0,'href':'https://www.w3schools.com','function':'-','event_flag':1,'event':'function_name'}
# 			}
# 		}

# total_links = len(link_data['links'])

# link_events = []

# link_functions = []

# for val in link_data['links'].values():
# 	if val.get('event_flag') == 1:
# 		link_events.append(val.get('event'))

# for val in link_data['links'].values():
# 	if val.get('link_flag') == 1:
# 		link_functions.append(val.get('function'))

# print(link_events)
# print(link_functions)

# response = requests.get(link_data.get('url'))
# response.encoding = 'utf-8'
# page = response.text

# events_in_page = True

# functions_in_page = True

# for event in link_events:
# 	value = page.find(event)
# 	if value > 0 :
# 		continue
# 	else:
# 		events_in_page = False
# 		break

# for function in link_functions:
# 	value = page.find(function)
# 	if value > 0 :
# 		continue
# 	else:
# 		functions_in_page = False
# 		break

# print('Total Links :' , total_links )

# js_level = 0

# if total_links == 0:
# 	js_level = 0
# else:
# 	if total_links > 0 and len(link_events) > 0 and len(link_functions) > 0 and events_in_page is False and functions_in_page is False:
# 		js_level = 5
# 	elif total_links > 0 and len(link_events) > 0 and len(link_functions) == 0 and events_in_page is False:
# 		js_level = 5
# 	elif total_links > 0 and len(link_events) == 0 and len(link_functions) > 0 and functions_in_page is False:
# 		js_level = 5
# 	elif total_links > 0 and len(link_events) > 0 and len(link_functions) > 0 and events_in_page is True and functions_in_page is False:
# 		js_level = 4
# 	elif total_links > 0 and len(link_events) > 0 and len(link_functions) > 0 and events_in_page is False and functions_in_page is True:
# 		js_level = 4
# 	elif total_links > 0 and len(link_events) > 0 and len(link_functions) > 0 and events_in_page is True and functions_in_page is True:
# 		js_level = 3
# 	elif total_links > 0 and len(link_events) == 0 and len(link_functions) > 0 and functions_in_page is True:
# 		js_level = 2
# 	elif total_links > 0 and len(link_events) > 0 and len(link_functions) == 0 and events_in_page is True:
# 		js_level = 2
# 	elif total_links > 0 :
# 		js_level = 1
# 	else:
# 		print('condition missed')

# print('JS Level :',js_level)