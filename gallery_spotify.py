import spotipy
import spotipy.util as util
import json
import webbrowser
import pandas
import pandas as pd
import urllib.request
import random

cred = "spotify_keys.json"
with open(cred, "r") as key_file:
    api_tokens = json.load(key_file)

client_id = api_tokens['client_id']
client_secret = api_tokens['client_secret']
redirectURI = api_tokens['redirect']
username = api_tokens['username']

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public user-library-read'
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token, retries=10)
genre_seeds = sp.recommendation_genre_seeds()

url = "https://api.artic.edu/api/v1/artworks?fields=id,title,artist_display,date_display,classification_titles,department_title,image_id&limit=100"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
all_art_data= json.loads(response.read())
    
artworks_df = pd.json_normalize(all_art_data['data'])
artworks_with_images_df = artworks_df[artworks_df["image_id"].notna()]

unique_departments = artworks_with_images_df["department_title"].unique()
departments_of_interest = ["Modern Art", "Contemporary Art", "Textiles", "Photography and Media", "Prints and Drawings"]
filtered_departments_df = artworks_with_images_df[artworks_with_images_df["department_title"].isin(departments_of_interest)]
department_counts = artworks_with_images_df["department_title"].value_counts()

art_to_music_map = {
    # Group 1: Abstract and Experimental
    "Modern Art": ["ambient", "experimental", "trip-hop", "alt-rock", "idm"],
    "Contemporary Art": ["ambient", "experimental", "trip-hop", "alt-rock", "idm"],
    
    # Group 2: Textiles and Cultural Arts
    "Textiles": ["new-age", "ethereal", "drone", "ambient"],
    "Arts of the Americas": ["folk", "americana"],
    "Arts of Africa": ["afrobeat", "african", "ethereal"],
    
    # Group 3: Historical and Classical Arts
    "Painting and Sculpture of Europe": ["classical", "ethereal"],
    "Applied Arts of Europe": ["jazz", "blues", "classical"],
    "Arts of the Ancient Mediterranean and Byzantium": ["classical","medieval"],
    
    # Group 4: Photography and Media
    "Photography and Media": ["cinematic", "dark-ambient", "lo-fi", "soundscapes", "drone"],
    "Prints and Drawings": ["ethereal", "ambient", "downtempo", "soundscapes"],
    
    # Group 5: Asian Art and Fusion
    "Arts of Asia": ["cantopop", "k-pop", "j-pop"]

}
for art_category in art_to_music_map.keys():
    genre_seeds = art_to_music_map.get(art_category)

    random_genre_seeds = random.sample(genre_seeds, min(5, len(genre_seeds)))

    recommendations = sp.recommendations(seed_genres=random_genre_seeds, limit=5)

    for track in recommendations['tracks']:
        track_name = track['name']
        artist_name = track['artists'][0]['name']

def display_virtual_exhibition_with_music(artworks_with_images_df, art_to_music_map, num_samples=5):
    # Randomly sample artworks to display
    sampled_artworks = artworks_with_images_df.sample(n=num_samples)
    all_recommended_tracks = []  # List to collect all recommended track URIs

    for _, artwork in sampled_artworks.iterrows():
        # Display the artwork details
        print(f"\nTitle: {artwork['title']}")
        print(f"Artist: {artwork['artist_display']}")
        print(f"Department: {artwork['department_title']}")
                
        # Get the genres for the department
        department = artwork["department_title"]
        genre_seeds = art_to_music_map.get(department, [])
        
        # Generate music recommendations if genres are available
        if genre_seeds:
            print("Music Recommendations:")
            random_genre_seeds = random.sample(genre_seeds, min(3, len(genre_seeds)))  
            recommendations = sp.recommendations(seed_genres=random_genre_seeds, limit=3)  # Limit to 3 tracks
            for track in recommendations['tracks']:
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                track_uri = track['uri']
                all_recommended_tracks.append(track_uri)  # Collect track URI for playlist
                print(f" ♫ {track_name} by {artist_name}")
        else:
            print("No genre mapping found for this department.")
       
    
    # Return all collected track URIs
    return all_recommended_tracks

def create_exhibition_playlist(track_uris):
    if not track_uris:
        print("No tracks to add to the playlist.")
        return
    
    # Create a new Spotify playlist for the exhibition
    playlist_name = "Virtual Art Exhibition Playlist"
    description = "A curated playlist featuring music to complement each artwork in the exhibition."
    playlist = sp.user_playlist_create(user=username, name=playlist_name, public=True, description=description)
    playlist_id = playlist['id']
    
    # Add tracks to the playlist
    random_genre_seeds = random.sample(genre_seeds, min(3, len(genre_seeds))) 
    sp.playlist_add_items(playlist_id, track_uris)
    print(f"Playlist '{playlist_name}' created with {len(track_uris)} tracks.")
    
    # Display the playlist URL
    playlist_url = playlist['external_urls']['spotify']
    print(f"Playlist URL: {playlist_url}")

track_uris = display_virtual_exhibition_with_music(artworks_with_images_df, art_to_music_map)
create_exhibition_playlist(track_uris)    