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
            return False, None
        else:
            return True, Match(response)


class Match:
    def __init__(self, response_json):
        self.game_mode = response_json['gameMode']
        self.game_time = response_json['gameLength']
        self.participants = [summoner['summonerName'] for summoner in response_json['participants']]

        # Information to display:
        # TODO champions
        # TODO mastery (keystone)
        # TODO summoner spells
        # TODO team composition
        # TODO game mmr (elo)
        # TODO time played today
        # TODO url to op.gg


if __name__ == '__main__':
    jingjie = Summoner('Kikis')
    print(jingjie.summoner_id)
    print([i['summonerName'] for i in jingjie.current_game()[1]['participants']])
