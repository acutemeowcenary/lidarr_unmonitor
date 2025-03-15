import requests
import json
import difflib
import os

# Set the base URL for your Lidarr instance and the API key
LIDARR_URL = "http://localhost:8686"  # Change this if your Lidarr instance is hosted elsewhere
API_KEY = "api key goes here"  # Replace this with your actual Lidarr API key

artist_id = os.environ.get("lidarr_artist_id")
album_id = os.environ.get("lidarr_album_id")

# Function to get the newest album release date for an artist
def compare_singles_to_album(album_id, artist_id):
    if album_id:
        artist_details = requests.get(f"{LIDARR_URL}/api/v1/artist/{artist_id}?apikey={API_KEY}").json()
        artist_name = artist_details.get("artistName")
        
        album = requests.get(f"{LIDARR_URL}/api/v1/album/{album_id}&apikey={API_KEY}").json()
        
        if album.get("albumType") == "Single"
            print("Album was a single.")
            
        if album.get("albumType") == "Album"
            singles = requests.get(f"{LIDARR_URL}/api/v1/album?artistId={artist_id}&apikey={API_KEY}").json()
        
            # Filter for albums with albumType "Single" and compare them to all "Albums"\
            ids_to_unmonitor = []
            for single in singles:
                if single.get("albumType") == "Single"
                    simularity_found = False
                    
                    single_release_title = single.get("title")
                    single_release_id = single.get("id")
                    
                    single_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={single_release_id}&apikey={API_KEY}").json()
                    single_names = [tracks.get("title").lower() for tracks in single_tracks]
                    
                    album_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={album_id}&apikey={API_KEY}").json()
                    track_names = [tracks.get("title").lower() for tracks in album_tracks]

                    for track2 in track_names:
                        similarity_ratio = difflib.SequenceMatcher(None, single_release_title, track2).ratio()
                        if similarity_ratio >= 0.8:
                            simularity_found = True
                            if single_release_id not in ids_to_unmonitor:
                                ids_to_unmonitor.append(single_release_id)
                            
                    for track1 in single_names:
                        for track2 in track_names:
                            similarity_ratio = difflib.SequenceMatcher(None, track1, track2).ratio()
                            if similarity_ratio >= 0.8:
                                simularity_found = True
                                if single_release_id not in ids_to_unmonitor:
                                    ids_to_unmonitor.append(single_release_id)
                                    
                if single.get("albumType") == "EP"
                    simularity_found = False
                    
                    single_release_title = single.get("title")
                    single_release_id = single.get("id")
                    
                    single_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={single_release_id}&apikey={API_KEY}").json()
                    single_names = [tracks.get("title").lower() for tracks in single_tracks]
                    
                    album_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={album_id}&apikey={API_KEY}").json()
                    track_names = [tracks.get("title").lower() for tracks in album_tracks]

                    for track2 in track_names:
                        similarity_ratio = difflib.SequenceMatcher(None, single_release_title, track2).ratio()
                        if similarity_ratio >= 0.8:
                            simularity_found = True
                            if single_release_id not in ids_to_unmonitor:
                                ids_to_unmonitor.append(single_release_id)
            try:
                if ids_to_unmonitor:
                    # Prepare data to unmonitor
                    payload = {"albumIds": ids_to_unmonitor, "monitored": False}
                    headers = {"content-type": "application/json"}
                    response = requests.put(f"{LIDARR_URL}/api/v1/album/monitor?apikey={API_KEY}", headers=headers, data=json.dumps(payload).encode("utf-8"))
                    response.raise_for_status()  # Raise an error if the status code is not 200
                    print(f"{artist_name}'s singles with ID {ids_to_unmonitor} has been unmonitored.")
                else:
                    print(f"{artist_name}'s singles are already unmonitored.")
            except requests.exceptions.RequestException as e:
                print(f"Error unmonitoring {artist_name}'s singles with ID {ids_to_unmonitor}: {e}")
            
        if album.get("albumType") == "EP"
            singles = requests.get(f"{LIDARR_URL}/api/v1/album?artistId={artist_id}&apikey={API_KEY}").json()
        
            # Filter for albums with albumType "Single" and compare them to all "Albums"\
            ids_to_unmonitor = []
            for single in singles:
                if single.get("albumType") == "Single"
                    simularity_found = False
                    
                    single_release_title = single.get("title")
                    single_release_id = single.get("id")
                    
                    single_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={single_release_id}&apikey={API_KEY}").json()
                    single_names = [tracks.get("title").lower() for tracks in single_tracks]
                    
                    album_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={album_id}&apikey={API_KEY}").json()
                    track_names = [tracks.get("title").lower() for tracks in album_tracks]

                    for track2 in track_names:
                        similarity_ratio = difflib.SequenceMatcher(None, single_release_title, track2).ratio()
                        if similarity_ratio >= 0.8:
                            simularity_found = True
                            if single_release_id not in ids_to_unmonitor:
                                ids_to_unmonitor.append(single_release_id)
                            
                    for track1 in single_names:
                        for track2 in track_names:
                            similarity_ratio = difflib.SequenceMatcher(None, track1, track2).ratio()
                            if similarity_ratio >= 0.8:
                                simularity_found = True
                                if single_release_id not in ids_to_unmonitor:
                                    ids_to_unmonitor.append(single_release_id)
                                    
            try:
                if ids_to_unmonitor:
                    # Prepare data to unmonitor
                    payload = {"albumIds": ids_to_unmonitor, "monitored": False}
                    headers = {"content-type": "application/json"}
                    response = requests.put(f"{LIDARR_URL}/api/v1/album/monitor?apikey={API_KEY}", headers=headers, data=json.dumps(payload).encode("utf-8"))
                    response.raise_for_status()  # Raise an error if the status code is not 200
                    print(f"{artist_name}'s singles with ID {ids_to_unmonitor} has been unmonitored.")
                else:
                    print(f"{artist_name}'s singles are already unmonitored.")
            except requests.exceptions.RequestException as e:
                print(f"Error unmonitoring {artist_name}'s singles with ID {ids_to_unmonitor}: {e}")
            
        else: 
            print("Album was not any of the three.")
    else:
        print("No album data to compare singles against.")
        
if artist_id:
    compare_singles_to_album(album_id, artist_id)
    print("Process completed.")
else:
    print(f"Failed to retrieve singles IDs for {artist_id}")
