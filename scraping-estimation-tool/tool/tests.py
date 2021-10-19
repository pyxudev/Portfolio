from django.test import TestCase

# Create your tests here.
from .models import DomainInfo

item = {'broken_links': '-',
	 'city': None,
	 'company': 'Facebook',
	 'complete_load_value': 169.2588462,
	 'connect_value': 0.0745095,
	 'country_name': 'Ireland',
	 'custom_404': 'Great, your website has a custom 404 error page.',
	 'depth': 6,
	 'discovered_pages': '6,302,229,253',
	 'doctype': 'HTML5',
	 'domain': 'facebook.com',
	 'download_latency': 2.5117979049682617,
	 'download_slot': 'api.netlify.com',
	 'download_timeout': 180.0,
	 'encoding': 'Great, language/character encoding is specified: utf8',
	 'first_byte_value': 151.6424885,
	 'inpage_links': 'We found a total of 39 link(s) including 0 link(s) to files',
	 'ip': '31.13.66.35',
	 'is_http_2_value': 100.0,
	 'is_https_value': 100.0,
	 'isp': 'Facebook Ireland Ltd',
	 'language': 'English',
	 'overall_score': '77',
	 'page_speed_score': 91.0,
	 'proxy': 'http://127.0.0.1:8118',
	 'region_name': None,
	 'robots': 'The path to your robots.txt file is disallowed.',
	 'sitemap': 'We found a sitemap at:',
	 'status_value': 100.0,
	 'time_zone': 'Europe/Dublin',
	 'traffic_estimation': 'Very High',
	 'traffic_rank': '4',
	 'trust_indicator': '87%',
	 'url_parameters': "Warning! We've detected parameters in a significant number "
	                   'of URLs.'}

domain = DomainInfo(domain = item['domain'], first_byte_time = item['first_byte_value'], complete_page_load_time = item['complete_load_value'], 
				https_score = item['is_https_value'], https_2_score = item['is_http_2_value'], 
				page_status_score = item['status_value'], website_overall_score = item['overall_score'], 
				in_page_links = item['inpage_links'], ip =  item['ip'], doc_type =  item['doctype'], 
				encoding =  item['encoding'], custom_error_page =  item['custom_404'], 
				language =  item['language'], robots_txt_info =  item['robots'], sitemap_info =  item['sitemap'], 
				url_parameters =  item['url_parameters'], broken_links_count =  item['broken_links'], 
				discovered_pages = item['discovered_pages'], trust_indicator_percent = item['trust_indicator'], 
				traffic_estimation = item['traffic_estimation'], traffic_rank = item['traffic_rank'], 
				page_speed_score = item['page_speed_score'], city = item['city'], isp = item['isp'], country = item['country_name'], 
				internet_company = item['company'], timezone = item['time_zone'], 
				region_name = item['region_name'])

domain.save()