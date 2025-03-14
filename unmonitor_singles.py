import requests
import json
import difflib
import os
from datetime import datetime

# Set the base URL for your Lidarr instance and the API key
LIDARR_URL = "http://localhost:8686"  # Change this if your Lidarr instance is hosted elsewhere
API_KEY = "api key goes here"  # Replace this with your actual Lidarr API key

artist_id = os.environ.get("lidarr_artist_id", 1)

# Function to get the newest album release date for an artist
def get_newest_album(artist_id):
    try:
        artist_details = requests.get(f"{LIDARR_URL}/api/v1/artist/{artist_id}?apikey={API_KEY}").json()
        artist_name = artist_details.get("artistName")

        albums = requests.get(f"{LIDARR_URL}/api/v1/album?artistId={artist_id}&apikey={API_KEY}").json()

        newest_album = None
        for album in albums:
            if album.get("albumType") == "Album" and album.get("releaseDate") and album.get("monitored"):
                release_date_str = album.get("releaseDate")
                try:
                    release_date_obj = datetime.fromisoformat(release_date_str.rstrip("Z"))
                    if newest_album is None or release_date_obj > datetime.fromisoformat(newest_album["releaseDate"].rstrip("Z")):
                        newest_album = album
                except ValueError:
                    print(f"Warning: Invalid release date format '{release_date_str}' for album '{album.get('title')}'")
                    continue # Skip to the next album.

        if newest_album:
            album_title = newest_album.get("title")
            release_date_str = newest_album.get("releaseDate")
            try:
                release_date_obj = datetime.fromisoformat(release_date_str.rstrip("Z"))
                album_release_date = release_date_obj.date().isoformat()
            except ValueError:
                album_release_date = release_date_str

            print(f"Artist: {artist_name} | Album: {album_title} | Released: {album_release_date}")
            return albums, album_release_date, artist_name
        else:
            print(f"Artist: {artist_name} | No valid 'Album' type releases found")
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error for artist ID {artist_id}: {e}")
        return None, None
        
def compare_singles_to_album(albums, album_release_date, artist_name):
    if albums and album_release_date:
        
        album_list = [album for album in albums if album.get("albumType") in ("Album", "EP") and album.get("releaseDate") and album.get("monitored")]
        single_list = [album for album in albums if album.get("albumType") == "Single" and album.get("releaseDate") and album.get("monitored")]
        
        # Filter for albums with albumType "Single" and compare them to all "Albums"\
        ids_to_unmonitor = []
        for album in single_list:
            single_release_date_str = album.get("releaseDate")
            try:
                single_release_date_obj = datetime.fromisoformat(single_release_date_str.rstrip("Z"))
                single_release_date = single_release_date_obj.date().isoformat()
            except ValueError:
                single_release_date = single_release_date_str
            single_release_title = album.get("title")
            single_release_id = album.get("id")
            
            single_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={single_release_id}&apikey={API_KEY}").json()
            single_names = [tracks.get("title").lower() for tracks in single_tracks]
            
            simularity_found = False
            for album in album_list:
                album_title = album.get("title")
                album_id = album.get("id")

                album_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={album_id}&apikey={API_KEY}").json()
                track_names = [tracks.get("title").lower() for tracks in album_tracks]

                if single_release_date < album_release_date:
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
        print("No album data to compare singles against.")
        
def compare_eps_to_album(albums, album_release_date, artist_name):
    if albums and album_release_date:
        
        album_list = [album for album in albums if album.get("albumType") == "Album" and album.get("releaseDate") and album.get("monitored")]
        single_list = [album for album in albums if album.get("albumType") == "EP" and album.get("releaseDate") and album.get("monitored")]
        
        # Filter for albums with albumType "EP" and compare them to all "Albums"\
        ids_to_unmonitor = []
        for album in single_list:
            single_release_date_str = album.get("releaseDate")
            try:
                single_release_date_obj = datetime.fromisoformat(single_release_date_str.rstrip("Z"))
                single_release_date = single_release_date_obj.date().isoformat()
            except ValueError:
                single_release_date = single_release_date_str
            single_release_title = album.get("title")
            single_release_id = album.get("id")
            
            single_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={single_release_id}&apikey={API_KEY}").json()
            single_names = [tracks.get("title").lower() for tracks in single_tracks]
            
            simularity_found = False
            for album in album_list:
                album_title = album.get("title")
                album_id = album.get("id")

                album_tracks = requests.get(f"{LIDARR_URL}/api/v1/track?albumId={album_id}&apikey={API_KEY}").json()
                track_names = [tracks.get("title").lower() for tracks in album_tracks]

                if single_release_date < album_release_date:
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
                print(f"{artist_name}'s eps with ID {ids_to_unmonitor} has been unmonitored.")
            else:
                print(f"{artist_name}'s eps are already unmonitored.")
        except requests.exceptions.RequestException as e:
            print(f"Error unmonitoring {artist_name}'s eps with ID {ids_to_unmonitor}: {e}")
    else:
        print("No album data to compare eps against.")

if artist_id:
    albums, album_release_date, artist_name = get_newest_album(artist_id)
    compare_singles_to_album(albums, album_release_date, artist_name)
    compare_eps_to_album(albums, album_release_date, artist_name)
    print("Process completed.")
else:
    print(f"Failed to retrieve singles IDs for {artist_id}")