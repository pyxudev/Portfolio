import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

print("Welcome!\nWordPress起動中...")
options   = Options()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver              = webdriver.Chrome(options=options, executable_path="~/chromedriver.exe")

#to pass the basic authentication
driver.get("https://[id]:[pw]@[website]/pig-data/wp-login.php")
time.sleep(2)

id_input            = driver.find_element_by_css_selector("#user_login")
pw_input            = driver.find_element_by_css_selector("#user_pass")
id_input.send_keys("[id]")
pw_input.send_keys("[pw]")
login_btn           = driver.find_element_by_css_selector("#wp-submit")
login_btn.click()
time.sleep(2)

pages               = []
links               = []
wrong               = '<HTML>'
right               = '<HTML>'
#edit on text file to avoid accident
txt_path            = './result.txt'
for i in range(1, 7):
	page_link       = "https://[website]/wp-admin/edit.php?orderby=modified&order=asc&paged=" + str(i)
	pages.append(page_link)

#to search the specific post
for page in pages:
	print(page)
	driver.get(page)
	time.sleep(2)

	trs             = driver.find_elements_by_css_selector("#the-list > tr")
	for tr in trs:
		atag        = tr.find_element_by_css_selector("td.title.column-title.has-row-actions.column-primary.page-title > strong > a").get_attribute("href")
		links.append(atag)
	time.sleep(2)

	for link in links:
		driver.get(link)
		time.sleep(2)

		content     = driver.find_element_by_css_selector("#content")	
		txt         = content.text

		#find the post and replace
		if wrong in txt:
			correct = txt.replace(wrong, right)
			content.clear()
			time.sleep(2)

			content.send_keys(correct)
			publish = driver.find_element_by_css_selector("#publish")
			publish.click()

			print(link + " 公開しました!")

			with open(txt_path, mode='a') as f:
				f.write(link+"\n")
				f.close()
			time.sleep(2)

print("done!")