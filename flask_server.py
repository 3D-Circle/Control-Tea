from flask import Flask, jsonify, request
from weather_api import DarkSky
import lol_api


app = Flask(__name__)


@app.route('/current_game', methods=['GET'])
def get_player_game():
    player = lol_api.Summoner(request.args['name'])
    current_game = player.current_game()
    if current_game:
        return jsonify({
            'status': 'online',
            'game': current_game.process_info()
        })
    else:
        return jsonify({'status': 'offline'})


@app.route('/weather', methods=['GET'])
def get_weather():
    weather = DarkSky()
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    resp = jsonify(weather.get_current_conditions(lat, lon))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run()
