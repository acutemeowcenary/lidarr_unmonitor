Files in the full library folder will scrub your entire library. I used them on mine and spot checked. They seemed to have worked well. Just update the api and url. If you plan to use both, use the unmonitor_compilation.py first. The unmonitor_singles.py looks only at monitored albums, so doing it second will help it not match stuff you plan to unmonitor with the first script.

Files not in a folder are like the arr-extended scripts. These are specifically for Lidarr. They will run from localhost, just update the api.

Drop the main unmonitor.bash and either/or both of the unmonitor.py in the folder /config/extended with the arr-extended scripts. Might have to make the bash script executable with chmod +x

In the lidarr connect page, manually add them under the custom script option, checkmark only on import, upgrade and rename. Locate the file and add it.

The unmonitor_compilations.py passes the artist_id to be able to find the newest album released and automatically unmonitors any compilation, remix, live album by that artist.

The unmonitor_singles.py passes the artist_id to be able to find the newest album released by that artist and unmonitor all singles and eps that show up in that album and or previous ones. By default it only looks at albums you have monitored, so it doesn't remove singles from albums you don't have.

It does this by matching any song in the singles album with any song in normal albums with an 80%. It then compares the main singles ablum name with any song in normal ablums with an 80%. If any one song matches (or the main name) matches a normal ablum, the whole single ablum is unmonitored.

To remove eps, it only checks the singles album name and compares that to all songs in normal ablums. This prevents it from removing too many eps.

Meant to help get rid of dupes in your library from complilation ablums and singles anytime it finds new music.

Plan to add a feature where it'll then delete any unmonitored single albums. It won't touch eps or normal ones.

Don't use if you want to keep multiple versions of files. I really only want albums, eps and singles that are not remixes and such. And that are not dupes.

May add something to remove acoustic and instrumental and such but for now, using smart playlists resolves that issue.

I don't really plan to support these much. Just using them for personal use. Feel free to fix/change/steal them.
