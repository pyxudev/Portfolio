from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests


session = HTMLSession()

def get_all_forms(url):
	
	res = session.get(url)
	soup = BeautifulSoup(res.html.html, "html.parser")
	return soup.find_all("form")

def get_form_details(form):
	
	details = {}
	
	action = form.attrs.get("action",'').lower()
	onsubmit = form.attrs.get("onsubmit",'').lower()
	onclick = form.attrs.get("onclick",'').lower()
	oninvalid = form.attrs.get("oninvalid",'').lower()
	oninput = form.attrs.get("oninput",'').lower()
	onchange = form.attrs.get("onchange",'').lower()
	
	method = form.attrs.get("method", "get").lower()
	
	inputs = []
	for input_tag in form.find_all("input"):
		
		input_type = input_tag.attrs.get("type", "text")
		
		input_name = input_tag.attrs.get("name")
		
		input_value =input_tag.attrs.get("value", "")
		
		inputs.append({"type": input_type, "name": input_name, "value": input_value})
	
	details["action"] = action
	details["method"] = method
	details["inputs"] = inputs
	details['onsubmit'] = onsubmit
	details['onclick'] = onclick
	details['oninvalid'] = oninvalid
	details['oninput'] = oninput
	details['onchange'] = onchange
	return details

url = "https://www.alibaba.com/"

def compute_difficulty(details):
	difficulty = 1
	if details['action'] is not '':
		difficulty = 2
	if details['method'] is not 'get':
		difficulty = 3
	if details['onsubmit'] is not '':
		difficulty = 4
	elif details['onclick'] is not '':
		difficulty = 4
	elif details['oninvalid'] is not '':
		difficulty = 4
	elif details['oninput'] is not '':
		difficulty = 4
	elif details['onchange'] is not '':
		difficulty = 4
	else:
		difficulty = 3

	return difficulty

def form_data(url):

	forms = get_all_forms(url)
	total_forms = len(forms)
	form_difficulty = 0
	
	print('Total Forms',total_forms)
	for i, form in enumerate(forms, start=1):
		form_details = get_form_details(form)
		form_diff = compute_difficulty(form_details)
		if form_diff > form_difficulty:
			form_difficulty = form_diff
		print("="*50, f"form #{i}", "="*50)
		print(form_details)
	print('Form difficulty',form_difficulty)

	form_data_dict = dict()

	form_data_dict['total_forms'] = total_forms
	form_data_dict['form_difficulty'] = form_difficulty

	return form_data_dict










# form_data = {'url':'https://www.amazon.com/',
# 			'forms':{
			
# 				'1':{'type':'form','action':'/errors/validatecaptcha','method':'get','event_flag':0,'event':'-','input_count':3},
# 				'2':{'type':'form','action':'/errors/validatecaptcha','method':'post','event_flag':1,'event':'function_name','input_count':5}
# 			}
# 		}

# total_forms = len(form_data['forms'])

# form_events = []
# form_inputs = []

# for val in form_data['forms'].values():
# 	if val.get('event_flag') == 1:
# 		form_events.append(val.get('event'))
# 	form_inputs.append(val.get('input_count',0))

# print(form_events)
# print(form_inputs)

# response = requests.get(form_data.get('url'))
# response.encoding = 'utf-8'
# page = response.text

# events_in_page = True
# form_input_count = 0

# for event in form_events:
# 	value = page.find(event)
# 	if value > 0 :
# 		continue
# 	else:
# 		events_in_page = False
# 		break

# for input_count in form_inputs:
# 	if input_count <= 3 :
# 		form_input_count = input_count
# 		continue
# 	else:
# 		form_input_count = input_count
# 		break

# print(form_input_count)

# print('Total Forms :' , total_forms )

# form_data_level = 0

# if total_forms == 0:
# 	form_data_level = 0
# else:
# 	if total_forms > 0 and len(form_events) > 0 and events_in_page is False and form_input_count > 3:
# 		form_data_level = 5
# 	elif total_forms > 0 and len(form_events) > 0 and events_in_page is False and form_input_count < 3:
# 		form_data_level = 4
# 	elif total_forms > 0 and len(form_events) > 0 and events_in_page is True and form_input_count > 3:
# 		form_data_level = 3
# 	elif total_forms > 0 and len(form_events) > 0 and events_in_page is True and form_input_count < 3:
# 		form_data_level = 2
# 	elif total_forms > 0 and len(form_events) == 0:
# 		form_data_level = 1
# 	else:
# 		print('condition missed')

# print('Form Data Level :',form_data_level)

