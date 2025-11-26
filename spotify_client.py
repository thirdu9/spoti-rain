import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

scope = "user-read-currently-playing user-read-playback-state user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope=scope
))

def current_track():
    current = sp.current_playback()

    if current is None or current['is_playing'] is False:
        return None
    
    track = current['item']
    print(f'Now playing... `{track['name']}`')
    
    return {
        "song_id" : track["id"],
        "name" : track["name"],
        "artists": ", ".join([a['name'] for a in track['artists']]),
        "album" : track["album"]["name"],
        "album_type" : track["album"]["album_type"],
        "album_id" : track["album"]["id"],
        "album_link" : track["album"]["external_urls"]['spotify']
        }

# current = sp.current_playback()
# print(current['item']['album']["external_urls"])

def get_recently_played():
    print('Getting you listening histroy....')
    results = sp.current_user_recently_played(limit=50)
    history = []
    for item in results["items"]:
        track = item['track']
        artists = track['artists']
        artist_dict = {}
        for a in artists:
            artist_dict[a['name'.strip()]] = a['id']

        history.append({
            
        "song_id": track["id"],
        "name": track["name"],
        "artists": artist_dict,
        "album": track["album"]["name"],
        "album_id": track["album"]["id"],
        "album_type": track["album"]["type"],
        "album_link" : track["album"]["external_urls"]["spotify"],
        "played_at": item["played_at"],
        "duration_ms": track["duration_ms"],
        "spotify_url": track["external_urls"]["spotify"],
        '#####':'--------------'
    })
    print('Done....')
    return history

if __name__ == '__main__': 
    print(get_recently_played())
    # artists = sp.current_user_recently_played(limit=1)['items'][0]['track']['artists']

    # artist = {}
    # for a in artists:
    #     artist[a['name']] = a['id']

    # print(artist)

    # a= artist.keys()
    # print(list(a))