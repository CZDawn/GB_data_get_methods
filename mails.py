import json
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


client = MongoClient('localhost', 27017)
db = client['mails_db']
collection = db.mails


driver = webdriver.Chrome(
        executable_path='Enter the route to the chromedriver')

driver.implicitly_wait(10)


driver.get('https://mail.ru/')
elem = driver.find_element_by_class_name('email-input')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)
elem = driver.find_element_by_class_name('password-input')
elem.send_keys('NextPassword172???')
elem.send_keys(Keys.ENTER)


links = set()
while True:
    flag = len(links)
    mails_block = driver.find_element_by_class_name('dataset__items')
    mails = mails_block.find_elements_by_class_name('llc')
    for mail in mails:
        link = mail.get_attribute('href')
        if (link is not None) and ('e.mail' in link):
            links.add(link)
    if flag == len(links):
        break
    actions = ActionChains(driver)
    actions.move_to_element(mails[-1])
    actions.perform()
print(f'Сбор ссылок на письма окончен: собрано {len(links)} ссылок.')


mails_data = []
for link in links:
    driver.get(link)
    mail_from = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    mail_date = driver.find_element_by_class_name('letter__date').text
    mail_subject = driver.find_element_by_class_name('thread__subject').text
    mail_text = driver.find_element_by_class_name('letter__body').text
    mail_info = {
        'from': mail_from,
        'date': mail_date,
        'subject': mail_subject,
        'text': mail_text
    }
    mails_data.append(mail_info)
print('Обработка писем окончена')


# with open('mails_data.json', 'a', encoding='UTF-8') as file:
#    json.dump(mails_data, file, indent=4, ensure_ascii=False)

i = len(mails_data)
for el in mails_data:
    collection.insert_one(el)
    i = i - 1
    print(f'Запись добавлена в базу данных. Осталось {i} писем')

