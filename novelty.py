import json
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

client = MongoClient('localhost', 27017)
db = client['Mvideo_products']
collection = db.novelties

driver = webdriver.Chrome(
    executable_path = '/Users/codezerodawn/Documents/'\
                      '#STUDY/GeekBrains/data_get_methods/'\
                      'GB_data_get_methods/chromedriver')

driver.implicitly_wait(10)

driver.get('https://www.mvideo.ru/?cityId=CityCZ_974')
novelties_block = driver.find_element_by_xpath(
        "//h2[text()[contains(., 'Новинки')]]/../../..")

actions = ActionChains(driver)
actions.move_to_element(novelties_block)
actions.perform()


next_button = novelties_block.find_element_by_xpath(".//a[contains(@class, 'next-btn')]")
while 'disabled' not in next_button.get_attribute('class'):
    driver.execute_script("arguments[0].click();", next_button)

novelties_list = novelties_block.find_elements_by_class_name('gallery-list-item')
print(len(novelties_list))

novelties_data = []
for novelty in novelties_list:
    url = novelty.find_element_by_tag_name('a').get_attribute('href')
    title = novelty.find_element_by_tag_name('a').get_attribute('data-track-label')
    price = novelty.find_element_by_class_name('fl-product-tile-price__current').text
    price = price[:-2:].split()
    if len(price):
        price = int(''.join(price))
    else:
        price = 0
    novelties_info = {
        'url': url,
        'title': title,
        'price': price
    }
    novelties_data.append(novelties_info)
print('Обработка новинок окончена')

'''
with open('novelties_data.json', 'a', encoding='UTF-8') as file:
    json.dump(novelties_data, file, indent=4, ensure_ascii=False)
'''

i = len(novelties_data)
for el in novelties_data:
    collection.insert_one(el)
    i = i - 1
    print(f'Запись добавлена в базу данных. Осталось {i} новинок')

