from flask import Flask, render_template, request
import random
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

cred = "spotify_keys.json"
with open(cred, "r") as key_file:
    api_tokens = json.load(key_file)

client_id = api_tokens['client_id']
client_secret = api_tokens['client_secret']
redirect_uri = api_tokens['redirect']
username = api_tokens['username']

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public user-library-read'
token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope).get_access_token()

sp = spotipy.Spotify(auth=token)

# list of pre-defined embedded albums as I am not able to 
# access genre seeds/ recommended songs from spotify for strange reasons.

albums = [
    "https://open.spotify.com/embed/album/5Uny0mkKiVGDat7H6SNDyS",  # Ryo Fukui - Scenery
    "https://open.spotify.com/embed/album/07KJ48Y7pbXvz3Q4H44GZl",  # Hiroshi Yoshimura - GREEN
    "https://open.spotify.com/embed/album/2vgc3dNLfceYv2k1vxK2zA",  # Hiroshi Suzuki - Cat
    "https://open.spotify.com/embed/album/1XoE7ZirQ3gjxq8HIzTJU9",  # Masabumi Kikuchi - Poo-Sun
    "https://open.spotify.com/embed/album/3uFgYgCEvCSACjB8XHl3hb",  # Toshiko Akiyoshi - Toshiko Mariano Quartet
    "https://open.spotify.com/embed/album/6XJZInF8Eg8hLBGNKTeHEI",  # Hiroshi Yoshimura - Green
    "https://open.spotify.com/embed/album/2rwQ71x5mXHX162ce5ypy7",  # Takao Uematsu - Jazz Fusion
    "https://open.spotify.com/embed/album/5STN9WkizILrlz9TmpNJkI",  # Hiroshi Suzuki - Soundscape
    "https://open.spotify.com/embed/album/1qWA39v5KzquKUCWqRAoiH",  # Masabumi Kikuchi - Sky
    "https://open.spotify.com/embed/album/3q4PfaZLuRApEjGT7Mm2N1",  # Toshiko Akiyoshi - Jazz Ensemble
    "https://open.spotify.com/embed/album/6hZD91Fc5vjc0bOoPmHsiS",  # Hiroshi Yoshimura - Aesthetic
    "https://open.spotify.com/embed/album/7jqOrlO593Qw3Xqjg0y7Md",  # Masabumi Kikuchi - Stratus
    "https://open.spotify.com/embed/album/4O4EW9UiDEg3Ue7Vcq5U0E"   # Takao Uematsu - Shifting Sands
]

def get_artworks():

    art_categories = [
        "Textiles", "Prints and Drawings", "Applied Arts of Europe", "Modern Art",
        "Photography and Media", "Contemporary Art", "Arts of Asia", 
        "Painting and Sculpture of Europe", "Arts of the Ancient Mediterranean and Byzantium",
        "Arts of Africa", "Arts of the Americas"
    ]
    
    art_api_url = "https://api.artic.edu/api/v1/artworks"
    artworks = []

    for category in art_categories:
        response = requests.get(
            f"{art_api_url}?fields=id,title,artist_display,image_id,department_title&q={category}&limit=10"
        )
        data = response.json()
        if "data" in data:
            artworks.extend(random.sample(data["data"], 1))  

    formatted_artworks = []
    for artwork in artworks:
        formatted_artworks.append({
            "title": artwork.get("title", "Unknown Title"),
            "artist": artwork.get("artist_display", "Unknown Artist"),
            "image_url": f"https://www.artic.edu/iiif/2/{artwork['image_id']}/full/843,/0/default.jpg"
        })

    return formatted_artworks

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artworks = get_artworks()
        random_album = random.choice(albums)
        return render_template('index.html', artworks=artworks, album=random_album)

    return render_template('index.html', artworks=None, album=None)

if __name__ == "__main__":
    app.run(debug=True)
