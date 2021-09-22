import scrapy, re, json
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    #TODO - вписать свой логин
    insta_login = 'Onliskill_udm'

    #TODO - вписать свой пароль (в зашифрованном виде)
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1629825416:ASpQAMvl1EAdo0N'\
                 'dRZNcM1/pjlU9rRg4n4cjCM00SDGSV5pDN6XbC93ZbYN67HUOHkX'\
                 'ZnGGe2gIWPU2qtQY0HAkIjR5U5syu+lv8qtqeI7cyy2ua6WmBV6A'\
                 'ngVo1apn3eJ6O3UAFVgb+q5HtHsQ='

    users_parse = ['ai_machine_learning', 'livethevanlife']
    api_url = 'https://i.instagram.com/api/v1/friendships/'


    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.insta_login_link,
            method='POST',
            callback=self.user_login,
            formdata={
                'username': self.insta_login,
                'enc_password': self.insta_pass
            },
            headers = {'X-CSRFToken': csrf}
        )


    def user_login(self, response: HtmlResponse):
        j_data = response.json()
        for user in self.users_parse:
            yield response.follow(
                f'/{user}/',
                callback=self.user_data_parse,
                cb_kwargs={'username': user}
            )


    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'count': 12,
            'search_surface': 'follow_list_page'
        }
        url_followers = f'{self.api_url}{user_id}/followers/?{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )


    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['next_max_id'] = j_data.get('next_max_id')
            url_followers = f'{self.api_url}/{user_id}/followers/?{urlencode(variables)}'

            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={
                    'variables': deepcopy(variables)
                },
                headers={'User-Agent': 'Instagram 155.0.0.37.107'}
            )

        followers = j_data.get('users')
        for follower in followers:
            item = InstaparserItem(
                username=username,
                follower_name=follower.get('username'),
                follower_full_name=follower.get('full_name'),
                follower_id=follower.get('pk'),
                follower_photo=follower.get('profile_pic_url'),
                follower_data=follower.get('node')
            )
            yield item


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

