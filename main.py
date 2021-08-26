import json
import requests
from bs4 import BeautifulSoup as bs
from get_HH_vacansies import getHeadHunterVacansies

def hhVacansies():
    for i in range(0, 100):
        url = 'https://nn.hh.ru'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '\
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        headers = {'User-Agent': user_agent}
        profession = 'python'
        params = {
            'fromSearchLine': 'true',
            'st': 'searchVacancy',
            'text': profession,
            'customDomain': 1,
            'page': i,
            'items_on_page': 20
        }

        response = requests.get(url + '/search/vacancy', params=params, headers=headers)
        soup = bs(response.text, 'html.parser')
        vacansies = soup.find_all('div', {'class':'vacancy-serp-item'})

        hh_result = getHeadHunterVacansies(vacansies, url)
        with open('vacansies_info.json', 'a', encoding='UTF-8') as file:
            json.dump(hh_result, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    hhVacansies()

