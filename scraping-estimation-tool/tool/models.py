from django.db import models

# Create your models here.

class DomainInfo(models.Model):
	
	domain = models.CharField(max_length=150, primary_key=True)

	first_byte_time = models.FloatField(null=True)
	complete_page_load_time = models.FloatField(null=True)
	https_score = models.FloatField(null=True)
	https_2_score = models.FloatField(null=True)
	page_status_score = models.FloatField(null=True)
	connection_time = models.FloatField(null=True)

	website_overall_score = models.PositiveIntegerField(default=0,null=True)
	in_page_links = models.TextField(null=True)
	ip =  models.TextField(null=True)
	doc_type =  models.TextField(null=True)
	encoding =  models.TextField(null=True)
	custom_error_page =  models.TextField(null=True)
	language =  models.TextField(null=True)
	url_parameters =  models.TextField(null=True)
	discovered_pages = models.TextField(null=True)
	traffic_estimation = models.TextField(null=True)
	traffic_rank = models.TextField(null=True)
	
	page_speed_score = models.FloatField(null=True)

	city = models.TextField(null=True)
	isp = models.TextField(null=True)
	country = models.TextField(null=True)
	internet_company = models.TextField(null=True)
	timezone = models.TextField(null=True)
	region_name = models.TextField(null=True) 

class DifficultyInfo(models.Model):

	domain = models.CharField(max_length=150, primary_key=True)

	total_js_files = models.PositiveIntegerField(default=0,null=True)
	js_difficulty = models.FloatField(default=0,null=True)
	total_forms = models.PositiveIntegerField(default=0,null=True)
	form_difficulty = models.FloatField(default=0,null=True)