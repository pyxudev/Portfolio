import json
import random
import time
import requests
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .forms import JavascriptForm
from .models import DomainInfo, DifficultyInfo
from .js_level import *
from .form_data_level import *
import mysql.connector

def save_to_db(domain, js_data_items , form_data_items):
	db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="Helloworld@12345",
			database="set_database",
			use_unicode=True, 
			charset="utf8"
		)
		
	cursor = db.cursor()

	query = """INSERT INTO tool_difficultyinfo (domain, total_js_files, js_difficulty, total_forms, form_difficulty) 
				VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE total_js_files=%s, js_difficulty=%s,
				 total_forms=%s, form_difficulty=%s"""
	try:
		cursor.execute(query, tuple([domain,js_data_items['total_js_files'],js_data_items['js_difficulty'],
			form_data_items['total_forms'],form_data_items['form_difficulty'],js_data_items['total_js_files'],
			js_data_items['js_difficulty'],form_data_items['total_forms'],form_data_items['form_difficulty']]))
		db.commit()
		print("MySQL Success: Data inserted!!")
	except mysql.connector.Error as e:
		print("MySQL Error: ", e, query)
	cursor.close()
	db.close()


def index(request): 
	return render(request, 'index.html')

def entry(request):
	return render(request, 'entry.html')

def input(request): 
	if request.method == 'POST':
		form = JavascriptForm(request.POST)
		if form.is_valid():
			domain = form.cleaned_data['domain']
			url = form.cleaned_data['url_label']
			xpath_str = form.cleaned_data['xpath_box']
			xpath_list = xpath_str.split(',')
			print(xpath_list)
			form_data_items = form_data(url)
			js_data_items = js_data(url,xpath_list)

			print(form_data_items)
			print(js_data_items)
			save_to_db(domain, js_data_items, form_data_items)
			
			js_dict = {url: xpath_list}
			return HttpResponseRedirect('/input/')

	else:
		form = JavascriptForm()

	return render(request, 'input.html', {'form': form})

def domain(request):
	fields = ['domain']
	domains  = DomainInfo.objects.all().values(*fields)
	context = {'domain_list': domains}
	return render(request, 'domain.html', context)

def webscan(request, domain):
	domain_info  = DomainInfo.objects.filter(domain=domain).values()
	difficulty_info = DifficultyInfo.objects.filter(domain=domain).values()
	context = {'domain_info': domain_info[0],'difficulty_info':difficulty_info[0]}
	return render(request, 'webscan_page.html', context)

def view_web(request):
	if request.method == 'POST':
		
		link = request.POST.get("link")
		domain = request.POST.get("domain")

		db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="Helloworld@12345",
			database="set_database",
			use_unicode=True, 
			charset="utf8"
		)
		
		cursor = db.cursor()

		query = """INSERT INTO tool_domaininfo (domain) VALUES (%s) ON DUPLICATE KEY UPDATE domain=%s"""
		try:
			cursor.execute(query, tuple([domain,domain]))
			db.commit()
			print("MySQL Success: Data inserted!!")
		except mysql.connector.Error as e:
			print("MySQL Error: ", e, query)

		query = """INSERT INTO tool_difficultyinfo (domain) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE domain=%s"""
		try:
			cursor.execute(query, tuple([domain,domain]))
			db.commit()
			print("MySQL Success: Data inserted!!")
		except mysql.connector.Error as e:
			print("MySQL Error: ", e, query)
	
		cursor.close()
		db.close()

		data1 = {
		  'project': 'estimation_tool_scrapy',
		  'spider': 'speed_score',
		  'domain': domain
		}
		data2 = {
		  'project': 'estimation_tool_scrapy',
		  'spider': 'testmysite',
		  'domain': domain
		}
		data3 = {
		  'project': 'estimation_tool_scrapy',
		  'spider': 'woorank',
		  'domain': domain
		}
		

		response1 = requests.post('http://localhost:6800/schedule.json', data=data1)
		response2 = requests.post('http://localhost:6800/schedule.json', data=data2)
		response3 = requests.post('http://localhost:6800/schedule.json', data=data3)

		time.sleep(120)

		domain_info  = DomainInfo.objects.filter(domain=domain).values()

		ip=domain_info[0]['ip']

		data4 = {
		  'project': 'estimation_tool_scrapy',
		  'spider': 'ip',
		  'domain': domain,
		  'ip':ip
		}

		if ip is not None:
			response4 = requests.post('http://localhost:6800/schedule.json', data=data4)

		return HttpResponseRedirect('/entry/')
	else:
		return HttpResponse(status=200)