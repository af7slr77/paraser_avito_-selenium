from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pickle
import json
import os



def create_driver():
	options = webdriver.ChromeOptions()
	options.add_argument("start-maximized")
	options.add_argument("--disable-popup-blocking")
	options.add_argument("--headless")
	user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
	options.add_argument(f"user-agent={user_agent}")
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	stealth(driver,
			languages=["en-US", "en"],
			vendor="Google Inc.",
			platform="Win32",
			webgl_vendor="Intel Inc.",
			renderer="Intel Iris OpenGL Engine",
			fix_hairline=True,
			)
	driver = webdriver.Chrome(options=options)
	return driver

def add_cookie(driver):
	for cookie in pickle.load(open(f"avito_cookies", 'rb')):
		driver.add_cookie(cookie)

def log_in_using_cookies(driver, url_post):
	driver.get(url_post)
	time.sleep(5)
	add_cookie(driver)
	time.sleep(5)
	driver.refresh()
	time.sleep(5)

def check_new_ad_in_json(url, file_path):
	with open(file_path, 'r', encoding='utf-8') as file:
		existing_file = json.load(file)
	for i in existing_file:
		if url in i.values():
			return True
	return False

def write_json(data, file_path='data.json'):
	# Проверяем существование файла
	if os.path.exists(file_path):
		# Если файл существует, сначала читаем его содержимое
		with open(file_path, 'r', encoding='utf-8') as file:
			existing_file = json.load(file)
			print(len(existing_file))
		# Добавляем только новые объявления
		for item in data:
			if not check_new_ad_in_json(item["url"], file_path):
				existing_file.append(item)
		
		# Перезаписываем файл с обновленными данными
		with open(file_path, 'w', encoding='utf-8') as json_file:
			json.dump(existing_file, json_file, indent=4, ensure_ascii=False)
	else:
		# Если файл не существует, записываем данные в новый файл
		with open(file_path, 'w', encoding='utf-8') as json_file:
			json.dump(data, json_file, indent=4, ensure_ascii=False)


def get_page_ads(url):
	data = []
	driver = create_driver()
	driver.get(url)
	# pickle.dump(driver.get_cookies(), open(f"avito_cookies", 'wb'))
	log_in_using_cookies(driver, url)
	driver.implicitly_wait(10)
	try:
		all_ads = driver.find_elements(By.CLASS_NAME, 'iva-item-content-rejJg')
	except Exception() as ex:
		return data
	for ad in all_ads:
		product_page_url = ad.find_element(
			By.CLASS_NAME, 'iva-item-titleStep-pdebR'
			).find_element(
				By.TAG_NAME,'a'
			).get_attribute('href')
		title = ad.find_element(
			By.CLASS_NAME, 'iva-item-titleStep-pdebR'
			).text.strip()
		price = ad.find_element(
			By.CLASS_NAME, 'iva-item-priceStep-uq2CQ'
			).text.strip()
		description = ad.find_element(
			By.CLASS_NAME, 'iva-item-descriptionStep-C0ty1'
			).text.strip()
		ad_data = {
			"url": product_page_url,
			"title": title,
			"price": price,
			"description": description,
		}
		data.append(ad_data)
	return data

def main():
	url = 'https://www.avito.ru/ekaterinburg?cd=1&q=xbox+series+x'
	page_ads = get_page_ads(url)
	print(len(page_ads))
	write_json(page_ads)

	# while get_page_ads() is not None:
	#     pass



	# page_driver = create_driver()
	# page_driver.get(product_page_url)
	# time.sleep(4)
	# page_driver.refresh()
	# page_driver.implicitly_wait(10)
	# time.sleep(5)
	# data = []
	# current_url = page_driver.current_url
	# data.append(current_url, description)
	# try:
	#     title = page_driver.find_element(By.CLASS_NAME, 'style-title-info-main-_sKj0').text.strip()
	#     data.append(title)
	# except:
	#     pass
	# try:
	#     price = page_driver.find_element(By.CSS_SELECTOR, 'span.style-item-price-text-_w822:nth-child(1)').text.strip()
	#     data.append(price)
	# except:
	#     pass
	# try:
	#     description = page_driver.find_element(By.CLASS_NAME, 'style-item-description-html-qCwUL').text.strip()
	#     data.append(description)
	# except:
	#     pass
	# try:
	#     city = page_driver.find_element(By.CSS_SELECTOR, '.style-item-address__string-wt61A').text.strip()
	#     data.append(city)
	# except:
	#     pass
	# print(data)
	# page_driver.close()

if __name__ == '__main__':
	main()
