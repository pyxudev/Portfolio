import time
import datetime
import slackweb
from datetime import timedelta
from datetime import date as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

slack = slackweb.Slack(url="***")
slack.notify(text="Tool Restarted")
options  = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument('log-level=3')
driver   = webdriver.Chrome(options=options, executable_path='~/chromedriver.exe')
sleep_time       = 10
presult          = []

while True:
	clock_now  = datetime.datetime.now()
	clock_hour = clock_now.hour
	clock_min  = clock_now.minute
	clock      = str(clock_now.hour)+":"+str(clock_now.minute)
	
	#1:00am - 2:00am maintenance
	if clock_hour   != 1:
		ins          = 0
		time_init    = time.time()
		time.sleep(sleep_time)
		time_pass    = time.time() - time_init
		res          = []

		if time_pass > sleep_time:
			now      = dt.today()

			driver.get("https://www.jgo-os.com/wr/dyse.php")
			time.sleep(10)

			link     = driver.find_element_by_css_selector("#reservation2 > div:nth-child(3) > a")
			
			while link  == False:
				time.sleep(3600)
				driver.get("https://www.jgo-os.com/wr/dy.php")
				time.sleep(5)
				link = driver.find_element_by_css_selector("#reservation2 > div:nth-child(3) > a")
				
				if link == True:
					link.click()
					time.sleep(3)
					break

			lgo_in = driver.find_elements_by_css_selector("#mainContents > div > div > p:nth-child(2) > a")
			if lgo_in  == True:
				lgo_in.click()
				time.sleep(10)

			course_list = driver.find_elements_by_css_selector('#tabJGO > table > tbody > tr:nth-child(1)')
			course_num  = len(course_list)

			for i in range(1, course_num):
				if i    < 6:
					selector_para = 2*i+1
				elif i  == 6:
					continue
				else:
					selector_para = 2*i

				str_1   = str(selector_para)

				for j in range(2, 30):
					str_2 = str(j)

					my_selector_1 = '#tabJGO > table:nth-child(' + str_1 + ') > tbody > tr:nth-child(1) > td:nth-child(' + str_2 + ')'
					waku  = driver.find_element_by_css_selector(my_selector_1)
					num   = waku.text

					if len(num) > 6:
						avlb_time = now + timedelta(days=j-1)
						avlb_time = str(avlb_time)
						avlb_time = avlb_time.replace('day', ' ')
						avlb_time = avlb_time.replace('days', ' ')
						avlb_time = avlb_time.replace('datetime.datetime', ' ')
						res.append(avlb_time)
			
			setres = set(res)
			res    = list(setres)

			if res  == presult:
				res = []
			elif len(res) < len(presult):
				for r in res:
					if r in presult:
						res.remove(r)
				if len(res) > 0:
					presult = res
			else:
				presult = res

			ins = len(res)
			
			if ins > 0:
				print_result     = clock + " " + str(res)
				slack.notify(text=print_result)

		print(clock)
		driver.close()
		time.sleep(5)
	driver.quit()
	time.sleep(5)
	#website changed in Jun 2021