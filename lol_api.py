import requests
import os
import json


is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    API_KEY = os.environ.get('LOL_API_KEY')
else:
    with open('api_keys.json') as f:
        API_KEY = json.load(f)['lol']


HEADERS = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": f"{API_KEY}",
    "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4,es;q=0.2"
}


class Summoner:
    def __init__(self, username=None, api_key=API_KEY):
        self.root_link = 'https://euw1.api.riotgames.com'
        self.key = api_key
        self.username = username
        self.summoner_id = self.get_summoner_id()

    def get_summoner_id(self):
        if self.username is None:
            return 0

        summoner_info_url = '/lol/summoner/v3/summoners/by-name/'
        r = requests.get(f'{self.root_link}{summoner_info_url}{self.username}', headers=HEADERS)
        return int(r.json()['id'])

    def current_game(self):
        current_game_url = '/lol/spectator/v3/active-games/by-summoner/'
        response = requests.get(f'{self.root_link}{current_game_url}{self.summoner_id}', headers=HEADERS).json()
        if 'status' in response and int(response["status"]["status_code"]) != 200:
            return False, None
        else:
            return True, response

if __name__ == '__main__':
    jingjie = Summoner('MrJingjie')
    print(jingjie.summoner_id)
    print([i['summonerName'] for i in jingjie.current_game()[1]['participants']])
