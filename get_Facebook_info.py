import json
import facebook


def main():
    token = 'Enter your token'
    graph = facebook.GraphAPI(token)
    fields = ['name, email, gender']
    profile  = graph.get_object('me', fields = fields)

    with open('facebook_dat.json', 'w', encoding='UTF-8') as file:
        json.dump(profile, file, indent=4)

if __name__ == '__main__':
    main()

