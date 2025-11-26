# Spoti-rain
Fetches user listening data and creates albums, song lists, listening history and analyzes the data for some cool graphs. More features coming soon.


## Instructions
`pip install -r requirements.txt`



## get_recently_played output format
- "song_id": track["id"],
- "name": track["name"],
- "artists": artist_dict, -> {artist_name : id}
- "album": track["album"]["name"],
- "album_id": track["album"]["id"],
- "album_link" : track["album"]["external_urls"]["spotify"],
- "played_at": item["played_at"],
- "duration_ms": track["duration_ms"],
- "spotify_url"