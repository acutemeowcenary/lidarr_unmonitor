Files in the full library folder will scrub your entire library. I used them on mine originally. Just update the api and url.

Files not in a folder are to be added to the arr-extended scripts. These are specifically for Lidarr. They will run from localhost, just update the api.

Drop the main unmonitor.bash and either/or both the unmonitor.py in the folder /config/extended with the other arr-extended scripts. Might have to make the bash script executable with chmod +x

In the lidarr connect page, manually add them under the custom script option, checkmark only on import, upgrade and rename. Locate the file and add it.

The unmonitor_compilations automatically unmonitors any compilation, remix, live album.

The unmonitor_singles passes the artist_id to be able to find the newest album released by that artist and unmonitor all singles and eps that show up in that album and or previous ones.

Meant to help get rid of dupes in your library from complilation ablums and singles anytime it finds new music.

Plan to add a feature where it'll then delete any unmonitored albums.

Don't use if you want to keep multiple versions of files. I really only one albums, eps and singles that are remixes and such.
