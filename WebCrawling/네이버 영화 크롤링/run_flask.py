from flask import Flask, jsonify
from flask_cors import CORS
from navermoviecrawler import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route("/getmovies", methods=["GET"])
def getnews():
    return jsonify(getMovies())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
