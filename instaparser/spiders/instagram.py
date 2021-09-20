import scrapy, re, json
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = 'Onliskill_udm' #TODO - вписать свой логин
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1629825416:ASpQAMvl1EAdo0NdRZNcM1/pjlU9rRg4n4cjCM00SDGSV5pDN6XbC93ZbYN67HUOHkXZnGGe2gIWPU2qtQY0HAkIjR5U5syu+lv8qtqeI7cyy2ua6WmBV6AngVo1apn3eJ6O3UAFVgb+q5HtHsQ=' #TODO - вписать свой пароль (в зашифрованном виде)
    user_parse = ['ai_machine_learning', 'livethevanlife']
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd' #TODO - вписать query_hash из заголовков запроса в devtools
    graphql_url = 'https://www.instagram.com/graphql/query/?' #TODO - query_hash из заголовка запроса в devtools со знаком ? в конце строки


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
        #if j_data['authenticated']:
        for user in self.user_parse:
            yield response.follow(
                f'/{user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': user} # при сборе минимум с двух пользователей
            )


    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'id': user_id,
            'first': 12
        }
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )


    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data= response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables)
                },
                headers={'User-Agent': 'Instagram 155.0.0.37.107'}
            )

        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstaparserItem(
                username=username,
                user_id=user_id,
                photo=post.get('node').get('display_url'),
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                post_data=post.get('node')
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

