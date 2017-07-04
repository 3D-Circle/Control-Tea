import requests
import os


is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    API_KEY = os.environ.get('LOL_API_KEY')
else:
    with open('lol_api_key.txt') as f:
        API_KEY = f.read()

ROOT_LINK = 'https://euw1.api.riotgames.com'
HEADERS = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": f"{API_KEY}",
    "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4,es;q=0.2"
}


class Champion:
    def __init__(self, _id):
        self.id = _id
        self.name = self.get_name()
        self.icon = self.get_profile_icon()

    def get_name(self):
        query_url = f'/lol/static-data/v3/champions/{self.id}'
        r = requests.get(f'{ROOT_LINK}{query_url}', headers=HEADERS)
        return r.json()['name']

    def get_profile_icon(self):
        """Return the url to the profile icon of the champion
        example: Aatrox's icon can be found on http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/Aatrox.png"""
        return f"http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/{self.name}.png"


class Spell:
    def __init__(self, _id):
        self.id = _id
        self.icon = self.get_icon()

    def get_icon(self):
        query_url = f'/lol/static-data/v3/summoner-spells/{self.id}'
        r = requests.get(f'{ROOT_LINK}{query_url}', headers=HEADERS)
        return f'http://ddragon.leagueoflegends.com/cdn/7.13.1/img/spell/{r.json()["key"]}.png'


def find_keystone(masteries):
    """Processes a list of masteries and return the url to the keystone if there is any"""
    KEYSTONE_IDS = [6161, 6162, 6164, 6361, 6362, 6363, 6261, 6262, 6263]
    keystone = 'https://opgg-static.akamaized.net/images/site/placeholder_keystonemastery.png'
    for mastery in masteries:
        if mastery['masteryId'] in KEYSTONE_IDS:
            keystone = f'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/mastery/{mastery["masteryId"]}.png'
            break
    return keystone


class Summoner:
    def __init__(self, username=None):
        # TODO time played today
        self.username = username
        self.summoner_id = self.get_summoner_id()

    def get_summoner_id(self):
        summoner_info_url = '/lol/summoner/v3/summoners/by-name/'
        r = requests.get(f'{ROOT_LINK}{summoner_info_url}{self.username}', headers=HEADERS)
        return int(r.json()['id'])

    def current_game(self):
        current_game_url = '/lol/spectator/v3/active-games/by-summoner/'
        response = requests.get(f'{ROOT_LINK}{current_game_url}{self.summoner_id}', headers=HEADERS).json()
        if 'status' in response and int(response["status"]["status_code"]) != 200:
            return False
        else:
            return Match(response)


class Match:
    def __init__(self, response_json):
        self.json = response_json

    def get_team_info(self):
        """Return a list of players including their champions, keystones and summoner spells (via urls to the icons)"""
        team_blue, team_red = [], []
        # Information to display:
        # TODO game mmr (elo)
        for summoner in self.json['participants']:
            if summoner['teamId'] == 100:
                team_to_append = team_blue
            else:
                team_to_append = team_red
            team_to_append.append({
                'champion': Champion(summoner['championId']).icon,
                'spells': [Spell(summoner['spell1Id']).icon, Spell(summoner['spell2Id']).icon],
                'keystone': find_keystone(summoner['masteries']),
                'name': summoner['summonerName'],
                'url': f'https://euw.op.gg/summoner/userName={summoner["summonerName"]}'
            })
        return team_blue, team_red

    def process_info(self):
        return {
            'game_mode': self.json['gameMode'],
            'start_time': self.json['gameStartTime'],
            'teams': self.get_team_info()
        }

