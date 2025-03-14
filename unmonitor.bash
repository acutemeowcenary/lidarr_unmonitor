#!/bin/bash
lidarr_artist_id="$lidarr_artist_id"
python /config/extended/unmonitor_compilations.py "$lidarr_artist_id"
python /config/extended/unmonitor_singles.py "$lidarr_artist_id"