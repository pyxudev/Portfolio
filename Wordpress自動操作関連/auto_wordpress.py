import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main(driver):

	print("行いたい操作を選択して下さい：")
	print("1.新しい固定ページを作成する\n2.新しい投稿を作成する\n3.新しいフォームを作成する\n4.既存のテキストを編集する\nexitでプログラムを終了させます")
	pange_list         = [home_link, blog_link, form_link]
	cat                = input()
	#to check correct value or not
	ck                 = 0

	if cat             == "exit":
		driver.close()
		time.sleep(1)
		driver.quit()
		time.sleep(1)
		ck             = 1

	else:
		for i in range(1, 5):
			if i       == 4:
				print("編集したいページのURLを入力してください：")
				link   = input()
				ck     = 1
				break
			elif cat   == i:
				link   = page_list[i-1]
				ck     = 1
				break
		if ck          == 1:
			driver.get(str(link))
			create(link, driver)
		else:
			main(driver)

def create(link, driver):
	time.sleep(2)
	create_new         = driver.find_element_by_css_selector("#wpbody-content > div.wrap > a")
	if create_new.text == "新規追加":
		create_new.click()
		time.sleep(1)
		h_1            = driver.find_element_by_css_selector("#wpbody-content > div.wrap > h1").text
		print(h_1)

		print("新規作成するタイトルを入力してください：")
		new_name       = input()
		name_space     = driver.find_element_by_css_selector("#title")
		name_space.send_keys(new_name)
		time.sleep(1)

		while True:
			print("この名前でよろしいですか？ y/n")
			confirm        = input()
			if confirm     == "y":
				break
			elif confirm   == "n":
				name_space.clear()
				print("インデックスに戻りますか？ y/n")
				go_back    = input()

				if go_back == "y":
					break

		print("コードスクリプトをインポートしてください、homeと入力するとインデックスに戻ります：")
		code        = input()
		time.sleep(1)
		
		if code     == "home":
			driver.get(home_link)
			main(driver)

		else:
			file    = open(code, "r", encoding="utf-8")
			text    = file.read()
			space   = driver.find_element_by_css_selector("#content")
			space.send_keys(str(text))
			time.sleep(2)
			publish = driver.find_element_by_css_selector("#publish")
			publish.click()
			print("公開しました!")
			edit(link, driver)

	else:
		print("エラーが発生しました、ご確認お願い致します")

def edit(link, driver):
	time.sleep(2)
	while True:
		print("コードスクリプトをインポートしてください、homeと入力するとインデックスに戻ります：")
		code     = input()
		time.sleep(1)

		if code  == "home":
			break

		else:
			driver.get(link)
			file  = open(code, "r", encoding="utf-8")
			text  = file.read()
			space = driver.find_element_by_css_selector("#content")
			space.clear()
			time.sleep(1)
			space.send_keys(str(text))
			time.sleep(2)
			push  = driver.find_element_by_css_selector("#publish")
			push.click()
			print("公開しました!")

	driver.get(home_link)
	main(driver)

print("Welcome!\nWordPress起動中...")
options   = Options()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver    = webdriver.Chrome(options=options, executable_path="~/chromedriver.exe")
# driver    = webdriver.Chrome(executable_path="c:/chromedriver.exe")
home_link = "https://****/wp-admin/index.php"
page_link = "https://****/wp-admin/edit.php?post_type=page"
blog_link = "https://****/wp-admin/edit.php"
form_link = "https://****/wp-admin/edit.php?post_type=mw-wp-form"

driver.get("https://jikai:Sdt.0831@services.sms-datatech.co.jp/pig-data/wp-login.php")
time.sleep(2)

id_input  = driver.find_element_by_css_selector("#user_login")
pw_input  = driver.find_element_by_css_selector("#user_pass")
id_input.send_keys("_id_")
pw_input.send_keys("_password_")
login_btn = driver.find_element_by_css_selector("#wp-submit")
login_btn.click()
time.sleep(2)
main(driver)