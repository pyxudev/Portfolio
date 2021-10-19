import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options               = Options()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver                = webdriver.Chrome(options=options, executable_path="c:/chromedriver.exe")

driver.get("https://*****@*****/pig-data/wp-login.php")
time.sleep(2)

id_input              = driver.find_element_by_css_selector("#user_login")
pw_input              = driver.find_element_by_css_selector("#user_pass")
id_input.send_keys("****")
pw_input.send_keys("******")
login_btn             = driver.find_element_by_css_selector("#wp-submit")
login_btn.click()
time.sleep(2)

links                 = []
tags                  = []
cats                  = []

for i in range(1, 8):
	page_link         = "https://services.sms-datatech.co.jp/pig-data/wp-admin/edit.php?paged=" + str(i)
	driver.get(page_link)
	time.sleep(2)
	trs               = driver.find_elements_by_css_selector("#the-list > tr")

	for tr in trs:
		status        = tr.find_element_by_css_selector("td.date.column-date").text
		tag           = tr.find_element_by_css_selector("td.tags.column-tags").text
		cat           = tr.find_element_by_css_selector("td.categories.column-categories").text
		if "公開済み" in status:
			atag      = tr.find_element_by_css_selector("td.title.column-title.has-row-actions.column-primary.page-title > strong > a").get_attribute("href")
			links.append(atag)
			cats.append(cat)
			tags.append(tag)

	i                 = 0
	for link in links:
		driver.get(link)
		time.sleep(3)

		title         = driver.find_element_by_css_selector("#title")
		title_txt     = title.get_attribute("value")
		if "</br>" in title_txt:
			title_txt = title_txt.replace("</br>", "「改行」")
		if "事例" not in tags[i]:
			if "マーケティング" in cats[i]:
				title_txt = "[コラム]" + title_txt
			elif "リリース" in cats[i]:
				title_txt = "[ニュース]" + title_txt

		content       = driver.find_element_by_css_selector("#content")
		content_txt   = content.text

		save_path     = './blog/' + title_txt + '.txt'
		f             = open(save_path, 'w', encoding='UTF-8')
		f.write(content_txt)
		f.close()
		i             += 1

driver.close()
time.sleep(1)
driver.quit()
time.sleep(1)
