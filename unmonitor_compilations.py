import requests
import json
import os

# Set the base URL for your Lidarr instance and the API key
LIDARR_URL = "http://localhost:8686"  # Change this if your Lidarr instance is hosted elsewhere
API_KEY = "api key goes here"  # Replace this with your actual Lidarr API key

artist_id = os.environ.get("lidarr_artist_id", 1)

if artist_id:
    try:
        artist_details = requests.get(f"{LIDARR_URL}/api/v1/artist/{artist_id}?apikey={API_KEY}").json()
        artist_name = artist_details.get("artistName")

        albums = requests.get(f"{LIDARR_URL}/api/v1/album?artistId={artist_id}&apikey={API_KEY}").json()
        
        ids_to_unmonitor = []
        for album in albums:
            if album.get("albumType") in ("Album", "EP") and any(secondary_type in album.get("secondaryTypes") for secondary_type in ["Compilation", "Live", "Remix"]) and album.get("monitored"):
                album_title = album.get("title")
                album_id = album.get("id")
                
                ids_to_unmonitor.append(album_id)
                
        try:
            if ids_to_unmonitor:
                # Prepare data to unmonitor
                payload = {"albumIds": ids_to_unmonitor, "monitored": False}
                headers = {"content-type": "application/json"}
                response = requests.put(f"{LIDARR_URL}/api/v1/album/monitor?apikey={API_KEY}", headers=headers, data=json.dumps(payload).encode("utf-8"))
                response.raise_for_status()  # Raise an error if the status code is not 200
                print(f"{artist_name}'s albums with ID {ids_to_unmonitor} has been unmonitored.")
            else:
                print(f"{artist_name}'s compilation albums are already unmonitored.")
        except requests.exceptions.RequestException as e:
            print(f"Error unmonitoring {artist_name}'s albums with ID {ids_to_unmonitor}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error for artist ID {artist_id}: {e}")
else:
    print(f"Failed to retrieve album IDs for {artist_id}")