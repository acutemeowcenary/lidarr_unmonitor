Files in the full library folder will scrub your entire library. I used them on mine and nothing got wiped. Just update the api and url.

Files not in a folder are to be added to the arr-extended scripts. These are specifically for Lidarr. They will run from localhost, just update the api.

Drop the main unmonitor.bash and either/or both the unmonitor.py in the folder /config/extended with the other arr-extended scripts. Might have to make the bash script executable with chmod +x

In the lidarr connect page, manually add them under the custom script option, checkmark only on import, upgrade and rename. Locate the file and add it.

The unmonitor_compilations.py passes the artist_id to be able to find the newest album released and automatically unmonitors any compilation, remix, live album by that artist.

The unmonitor_singles.py passes the artist_id to be able to find the newest album released by that artist and unmonitor all singles and eps that show up in that album and or previous ones.
It does this by matching any song in the singles album with any song in normal albums with an 80%. It then compares the main singles ablum name with any song in normal ablums with an 80%. If any one song matches (or the main name) matches a normal ablum, the whole single ablum is unmonitored.

To remove eps, it only checks the singles album name and compares that to all songs in normal ablums. This prevents it from removing too many eps.

Meant to help get rid of dupes in your library from complilation ablums and singles anytime it finds new music.

Plan to add a feature where it'll then delete any unmonitored single albums. It won't touch eps or normal ones.

Don't use if you want to keep multiple versions of files. I really only want albums, eps and singles that are not remixes and such. And that are not dupes.

May add something to remove acoustic and instrumental and such but for now, using smart playlists resolves that issue.
