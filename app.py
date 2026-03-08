from flask import Flask, request, jsonify, send_from_directory, render_template
import os, json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, template_folder="templates", static_folder="static")

MOVIES_JSON = "movies.json"
BANNER_JSON = "banner.json"

# ---------------- HELPERS ----------------
def load_movies():
    if os.path.exists(MOVIES_JSON):
        with open(MOVIES_JSON,"r") as f:
            return json.load(f)
    return []

def save_movies(data):
    with open(MOVIES_JSON,"w") as f:
        json.dump(data,f,indent=2)

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return send_from_directory("static","index.html")

@app.route("/add_movie")
def add_movie_page():
    return render_template("add_movies.html")

@app.route("/save-movie",methods=["POST"])
def save_movie():
    data = request.get_json(force=True)
    movies = load_movies()
    new_id = max([m.get("id",0) for m in movies], default=0) + 1
    movies.append({
        "id": new_id,
        "title": data.get("title"),
        "category": data.get("category"),
        "poster": data.get("poster"),
        "preview": data.get("preview"),
        "movie": data.get("movie"),
        "is_banner": data.get("is_banner")
    })
    save_movies(movies)
    return jsonify({"status":"success","message":"Movie info saved"})

@app.route("/movies")
def movies():
    return jsonify(load_movies())

@app.route("/player_preview")
def preview():
    return send_from_directory("static","player_preview.html")

@app.route("/player")
def player():
    return send_from_directory("static","player.html")

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

if __name__=="__main__":
    app.run(debug=True,port=5001)
