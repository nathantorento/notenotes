from dotenv import load_dotenv
import os
import requests
import base64
from requests import post, get
import json
import pandas as pd

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Function to get token from Spotify API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)

    return json_result["access_token"]

# Create function to populate sample database using Spotify API
def populate_tracks(sample_albums):
    token = get_token()
    headers = {"Authorization": "Bearer " + token}
    for album in sample_albums:
        url = f"https://api.spotify.com/v1/search?q={album}&type=album&limit=1"
        result = get(url, headers=headers)
        album_search_json_result = json.loads(result.content)
        if not album_search_json_result['albums']['items']:
            continue
        album_id = album_search_json_result["albums"]["items"][0]["id"]

        tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        tracks_result = get(tracks_url, headers=headers)
        tracks = json.loads(tracks_result.content)["items"]

        for track in tracks:
            track_id = track["id"]
            title = track["name"]
            artist = track["artists"][0]["name"]

            # Fetch tempo from audio features endpoint
            audio_features_url = f"https://api.spotify.com/v1/audio-features/{
                track_id}"
            audio_features_result = get(audio_features_url, headers=headers)
            tempo = json.loads(audio_features_result.content)["tempo"]

            track_data = {
                'track_id': track_id, 'title': title,
                'album': album, 'artist': artist, 'tempo': tempo
            }
            sample_database.loc[len(sample_database)] = track_data
    return sample_database

# List of albums to populate sample database
sample_albums = [
    "eternal sunshine", "thank u next",
    "Something To Give Each Other", "Bloom",
    "DISCO (Deluxe)", "Tension (Deluxe)",
    "Scarlet", "Planet Her",
    "Never Enough", "Freudian"
]

# Populate the sample database
sample_database = pd.DataFrame(
    columns=['track_id', 'title', 'album', 'artist', 'tempo'])
sample_database = populate_tracks(sample_albums)

# Save the DataFrame to a CSV file
sample_database.to_csv('sample_database.csv', index=False)
