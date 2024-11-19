import random
import json
import spotipy
import spotipy.util as util
import requests

cred = "spotify_keys.json"
with open(cred, "r") as key_file:
    api_tokens = json.load(key_file)

client_id = api_tokens['client_id']
client_secret = api_tokens['client_secret']
redirectURI = api_tokens['redirect']
username = api_tokens['username']

scope = 'playlist-modify-public playlist-modify-private user-library-read'
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirectURI)
sp = spotipy.Spotify(auth=token, retries=10)

track_uris = [
    "spotify:track:6cE2FLwrFQax3nU57J9F1F",  # Ryo Fukui - It Could Happen to You
    "spotify:track:4ymgmXnpuuOiJt9EtL3o8b",  # Ryo Fukui - Early Summer
    "spotify:track:0FcHBk3o2mksDRMEmhtUmU",  # Hiroshi Yoshimura - Crepuscule
    "spotify:track:2PXqAFHVRfTYkVYrFSx09z",  # Hiroshi Yoshimura - Horizon
    "spotify:track:2UXWhOdhRVFzfdadRBak1c",  # Hiroshi Suzuki - Cat
    "spotify:track:6x1vPr3TFTWKPqeQlwROdF",  # Hiroshi Suzuki - Walk Tall
    "spotify:track:6bLOvxk4Xswv9cYQFByZjJ",  # Masabumi Kikuchi - Dancing Mist
    "spotify:track:3fHsUAMKfOKHH6pGe4nPdS",  # Masabumi Kikuchi - Dreamscape
    "spotify:track:5YF3pJm9VFXi6exEnVPwxD",  # Toshiko Akiyoshi - When Johnny Comes Marching Home
    "spotify:track:1ctNTWsRbZdQzY7NJZbFvL",  # Toshiko Akiyoshi - Blues for Toshiko
]

def create_music_playlist():
    playlist_name = "virtual art exhibition playlist"
    playlist = sp.user_playlist_create(username, playlist_name, public=True)
    playlist_id = playlist["id"]
    print(f"created playlist: {playlist_name} (ID: {playlist_id})")

    sp.user_playlist_add_tracks(username, playlist_id, track_uris[:5]) 

    return f"https://open.spotify.com/playlist/{playlist_id}"

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
        response = requests.get(f"{art_api_url}?fields=id,title,artist_display,image_id,department_title&q={category}&limit=10")
        data = response.json()
        if "data" in data:
            artworks.extend(random.sample(data["data"], min(1, len(data["data"]))))
    
    formatted_artworks = []
    for artwork in artworks:
        formatted_artworks.append({
            "title": artwork.get("title", "unknown title"),
            "artist": artwork.get("artist_display", "unknown artist"),
            "image_url": f"https://www.artic.edu/iiif/2/{artwork['image_id']}/full/843,/0/default.jpg"
        })

    return formatted_artworks