from flask import Flask, jsonify, request
import lol_api

app = Flask(__name__)


@app.route('/current_game', methods=['GET'])
def get_player_game():
    player = lol_api.Summoner(request.args['name'])
    is_playing, current_game = player.current_game()
    if is_playing:
        return jsonify({
            'status': 'online', 'game': current_game
        })
    else:
        return jsonify({'status': 'offline'})


if __name__ == '__main__':
    app.run()
