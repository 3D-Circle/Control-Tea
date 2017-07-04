import requests
import os
import json


is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    API_KEY = os.environ.get('WEATHER_API_KEY')
else:
    with open('api_keys.json') as f:
        API_KEY = json.load(f)['weather']


class DarkSky:
    def __init__(self, key=None):
        self.api_key = key if key is not None else API_KEY

    def get_current_conditions(self, lat, lon):
        url = 'https://api.darksky.net/forecast/{}/{},{}'.format(self.api_key, lat, lon)
        data = requests.get(url).json()
        print(url, data)
        return {
            'icon': data['currently']['icon']
        }


if __name__ == '__main__':
    o = DarkSky()
    o.get_current_conditions(48.8566, 2.3522)
