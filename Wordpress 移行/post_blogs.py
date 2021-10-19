import csv
import time
import glob
import codecs
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

driver.get("https://****/wp-login.php")
time.sleep(2)

id_input              = driver.find_element_by_css_selector("#user_login")
pw_input              = driver.find_element_by_css_selector("#user_pass")
id_input.send_keys("***")
pw_input.send_keys("***")
login_btn             = driver.find_element_by_css_selector("#wp-submit")
login_btn.click()
time.sleep(2)

usecase               = "https://***/wp-admin/edit.php?post_type=usecase"
news                  = "https://***/wp-admin/edit.php?post_type=news_columns"
blogs                 = glob.glob("./blog/*.txt")
i                     = 0

for blog in blogs:
	done_csv          = codecs.open("./done.csv", "r")
	reader            = csv.reader(done_csv)
	titles            = []
	for row in reader:
		titles.append("".join(row))
	done_csv.close()

	if blog[7:] not in titles:
		if "[ニュース]" in blog or "[コラム]" in blog:
			driver.get(news)
		else:
			driver.get(usecase)	
		time.sleep(2)

		create_new     = driver.find_element_by_css_selector("#wpbody-content > div.wrap > a")
		create_new.click()
		time.sleep(2)

		if i           == 0:
			note       = driver.find_element_by_css_selector("body > div:nth-child(9) > div > div > div > div > div > div.components-modal__header > button > svg")
			note.click()
			time.sleep(1)
			menu       = driver.find_element_by_css_selector("#editor > div.edit-post-layout.is-mode-visual.is-sidebar-opened.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-interface-skeleton__header > div > div.edit-post-header__settings > div.components-dropdown.components-dropdown-menu.edit-post-more-menu")
			menu.click()
			time.sleep(1)

			editor      = driver.find_element_by_css_selector("#editor > div.popover-slot > div > div > div > div > div:nth-child(2) > div:nth-child(2) > button:nth-child(2)")
			editor.click()
			time.sleep(1)
			i         +=1	

		new_name       = blog.replace(".txt", "")
		if "「改行」" in blog:
			new_name   = new_name.replace("「改行」", "<br>")
		if "[ニュース]" in blog:
			new_name   = new_name[13:]
		elif "[コラム]" in blog:
			new_name   = new_name[12:]
			column     = driver.find_element_by_css_selector("#acf-field_60f52ed2738d7-column")
			column.click()
			time.sleep(1)
		else:
			new_name   = new_name[7:]

		name_space     = driver.find_element_by_css_selector("textarea.editor-post-title__input")
		name_space.send_keys(new_name)
		time.sleep(1)

		file           = open("./blog/" + blog[7:], "r", encoding="utf-8")
		text           = file.read()
		space          = driver.find_element_by_css_selector("textarea.editor-post-text-editor")
		space.send_keys(str(text))
		time.sleep(2)

		if "[ニュース]" in blog or "[コラム]" in blog:
			lead       = driver.find_element_by_css_selector("#acf-field_60f521702a239")
			lead.send_keys(" ")
			time.sleep(2)

		time.sleep(5)
		draft          = driver.find_element_by_css_selector("#editor > div.edit-post-layout.is-mode-text.is-sidebar-opened.has-metaboxes.interface-interface-skeleton > div > div.interface-interface-skeleton__header > div > div.edit-post-header__settings > button.components-button.editor-post-save-draft.is-tertiary")
		draft.click()
		time.sleep(5)
		
		reset          = driver.find_element_by_css_selector("#editor > div.edit-post-layout.is-mode-text.is-sidebar-opened.has-metaboxes.interface-interface-skeleton > div > div.interface-interface-skeleton__header > div > a")
		reset.click()
		time.sleep(2)

		done_csv       = codecs.open("./done.csv", "a")
		writer         = csv.writer(done_csv)
		done_list      = []
		done_list.append([blog[7:]])
		writer.writerows(done_list)
		done_csv.close()
		time.sleep(1)

print("done")
# driver.close()
# time.sleep(1)
# driver.quit()
# time.sleep(1)