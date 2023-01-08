import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from models import write_to_db


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")

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
    return driver


driver = create_driver()
url = 'https://www.avito.ru/ekaterinburg/noutbuki?cd=1&q=%D0%B8%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B9+%D0%BD%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA+rtx+3080'
driver.get(url)
driver.implicitly_wait(10)
all_ads = driver.find_elements(By.CLASS_NAME, 'iva-item-content-rejJg')
for ad in all_ads:
    product_page_url = ad.find_element(By.CLASS_NAME, 'iva-item-titleStep-pdebR').find_element(By.TAG_NAME,
                                                                                               'a').get_attribute(
        'href')
    page_driver = create_driver()
    page_driver.get(product_page_url)
    page_driver.implicitly_wait(10)
    time.sleep(10)
    data = []
    current_url = page_driver.current_url
    data.append(current_url)
    try:
        title = page_driver.find_element(By.CLASS_NAME, 'style-title-info-main-_sKj0').text.strip()
        data.append(title)
    except:
        pass
    try:
        price = page_driver.find_element(By.CSS_SELECTOR, 'span.style-item-price-text-_w822:nth-child(1)').text.strip()
        data.append(price)
    except:
        pass
    try:
        description = page_driver.find_element(By.CLASS_NAME, 'style-item-description-html-qCwUL').text.strip()
        data.append(description)
    except:
        pass
    try:
        city = page_driver.find_element(By.CSS_SELECTOR, '.style-item-address__string-wt61A').text.strip()
        data.append(city)
    except:
        pass
    write_to_db(*data)
    print(data)
    page_driver.close()

# ###################### делать проверку на основной странице, если ссылка уже есть в базе, то не проверять ее
# больше(что бы не долбить сайт)
if __name__ == '__main__':
    pass
