import random
import json
import spotipy
import spotipy.util as util
import requests

# Load Spotify credentials from JSON file
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

# Curated track URIs (based on your albums)
TRACK_URIS = [
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
    """Create a personalized Spotify playlist."""
    playlist_name = "Virtual Art Exhibition Playlist"
    
    # Create the playlist
    playlist = sp.user_playlist_create(username, playlist_name, public=True)
    playlist_id = playlist["id"]

    print(f"Created playlist: {playlist_name} (ID: {playlist_id})")

    # Add tracks to the playlist
    try:
        sp.user_playlist_add_tracks(username, playlist_id, TRACK_URIS[:5])  # Add first 5 tracks
    except Exception as e:
        print(f"Error adding tracks: {e}")

    return f"https://open.spotify.com/playlist/{playlist_id}"

def get_artworks():
    """Fetch 10 random artworks from preferred categories."""
    ART_CATEGORIES = [
        "Textiles", "Prints and Drawings", "Applied Arts of Europe", "Modern Art",
        "Photography and Media", "Contemporary Art", "Arts of Asia", 
        "Painting and Sculpture of Europe", "Arts of the Ancient Mediterranean and Byzantium",
        "Arts of Africa", "Arts of the Americas"
    ]
    
    ART_API_URL = "https://api.artic.edu/api/v1/artworks"
    preferred_departments = ART_CATEGORIES

    artworks = []
    try:
        for category in preferred_departments:
            response = requests.get(
                f"{ART_API_URL}?fields=id,title,artist_display,image_id,department_title&q={category}&limit=10"
            )
            data = response.json()
            if "data" in data:
                artworks.extend(random.sample(data["data"], min(1, len(data["data"]))))
    except Exception as e:
        print(f"Error fetching artworks: {e}")

    # Format artworks for display
    formatted_artworks = []
    for artwork in artworks:
        formatted_artworks.append({
            "title": artwork.get("title", "Unknown Title"),
            "artist": artwork.get("artist_display", "Unknown Artist"),
            "image_url": f"https://www.artic.edu/iiif/2/{artwork['image_id']}/full/843,/0/default.jpg"
        })

    return formatted_artworks
