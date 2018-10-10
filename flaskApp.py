# import libraries
from flask import Flask, request
from flask_cors import CORS, cross_origin
from sortHeroes import sortHeroes
import config

# create app
app = Flask(__name__)

# route sortHeroes
@app.route('/sortFunc')
@cross_origin()
def sortFunc():
	playerName = request.args.get('name', None)
	if not playerName:
		return "Player name not provided."
	config.CONFIG['PLAYER_USERNAME_STR'] = playerName

	numGames = request.args.get('numGames', None)
	if not numGames:
		return "Number of games not provided."
	config.CONFIG['DISPLAY_X_LAST_GAMES'] = int(numGames)

	heroSelected = request.args.getlist('hero', None)
	if not heroSelected:
		return "No heroes provided."
	config.CONFIG['SPECIFIC_HERO_NAMES'] = heroSelected

	return sortHeroes()

if __name__ == "__main__":
    app.run(debug=True)