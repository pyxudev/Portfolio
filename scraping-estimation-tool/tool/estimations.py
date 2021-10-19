
def difficulty_score(js_level,form_data_level,extaction_level,ping_level,tor_blocking_level,page_status_level):

	diff_score = (max(js_level , form_data_level , extraction_level)*2)
	rechability_score = (max(ping_level,tor_blocking_level,page_status_level)*2)

	score = [diff_score,rechability_score]
	
	return score


js_level = 3

form_data_level = 3

extraction_level = 4

ping_level = 2

tor_blocking_level = 3

page_status_score = 80

page_status_level = max(1,(100-page_status_score)/10)

score_list = difficulty_score(js_level,form_data_level,extraction_level,ping_level,tor_blocking_level,page_status_level)



print('Difficulty Score:',score_list[0],'/ 10')
print('Reachability Score:',score_list[1],'/ 10')
 
complete_page_load = 120 

approximate_urls = 2000000

max_rtt = 100

avg_rtt = 65

max_scraping_time = (complete_page_load + max_rtt) * approximate_urls

avg_scraping_time = (complete_page_load + avg_rtt) * approximate_urls

print('Max Scraping Time :' ,(max_scraping_time/1000),'sec', '=' ,round((max_scraping_time/60000),2) ,'mins')

print('Avg Scraping Time :' ,(avg_scraping_time/1000),'sec', '=' ,round((avg_scraping_time/60000),2) ,'mins')

