import json, requests

USERNAME = 'Enter GitHub username'
URL = f'https://api.github.com/users/{USERNAME}/repos'

repos_data = {el['name']: el['url'] for el in requests.get(URL).json()}

with open(f'{USERNAME}_repos.json', 'w', encoding='UTF-8') as file:
    json.dump(repos_data, file, sort_keys=True, indent=4)

