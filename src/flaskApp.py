# import libraries
from flask import Flask, render_template
from sortHeroes import sortHeroes

# create app
app = Flask(__name__)

# # route home
# @app.route("/")
# def home():
# 	return render_template("index.js")

# route sortHeroes
@app.route("/sortFunc")
def sortFunc():
	return sortHeroes()

if __name__ == "__main__":
    app.run(debug=True)