from pprint import pprint
import requests


with open('lol_api_key') as f:
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
        r = requests.get(f'{ROOT_LINK}{query_url}')
        return r.json()['name'] if 'status' not in r.json() else 'Teemo'  # the default champion == troll

    def get_profile_icon(self):
        """Return the url to the profile icon of the champion
        example: Aatrox's icon can be found on http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/Aatrox.png"""
        return f"http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/{self.name}.png"


class Spell:
    def __init__(self, _id):
        self.id = _id

    def get_profile_icon(self):
        spell_ref = {
            0: 'Haste',  # Ghost
            0.1: 'Snowball',  # Mark
            0.2: 'Mana',  # Clarity,
            0.3: 'PoroThrow',  # Poro Toss
            0.4: 'PoroRecall',  # To the King!
            0.5: 'Barrier',
            1: 'Boost',
            2: 'Exhaust',
            4: 'Flash',
            7: 'Heal',
            11: 'Smite',
            12: 'Teleport',
            14: 'Dot'  # Ignite
        }[self.id]
        return f'http://ddragon.leagueoflegends.com/cdn/7.13.1/img/spell/Summoner{spell_ref}.png'


class Summoner:
    def __init__(self, username=None):
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

        self.game_mode = response_json['gameMode']
        self.start_time = response_json['gameStartTime']

    def get_team_info(self):
        """Return a list of players including their champions, keystones and summoner spells (via urls to the icons)"""
        KEYSTONE_IDS = [6161, 6162, 6164, 6361, 6362, 6363, 6261, 6262, 6263]
        # Information to display:
        # TODO mastery (keystone)
        # TODO summoner spells
        # TODO game mmr (elo)
        # TODO time played today
        return [
            {
                'team': 'blue' if summoner['teamId'] == 100 else 'red',
                'name': summoner['summonerName'],
                'url': f'https://euw.op.gg/summoner/userName={summoner["summonerName"]}',
                'champion': Champion(summoner['championId']).get_profile_icon(),
                'keystone': 1,
                'spells': [],
            }
            for summoner in self.json['participants']
        ]




if __name__ == '__main__':
    jingjie = Summoner('OG Darkside')
    pprint(jingjie.current_game().json)
