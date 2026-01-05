from sqlalchemy.orm import sessionmaker
from db import engine, Song, Artist, Album, ListeningHistory, Session
from datetime import datetime



def save_song(entry,session):
    print('Saving songs...')
    
    with session.no_autoflush:
        song = session.query(Song).filter_by(song_id=entry["song_id"]).first()
    
    artists_dict = entry["artists"]

    artists = list(artists_dict.keys())

    if not song:
        song = Song(
            song_id=entry["song_id"],
            name=entry["name"],
            artist_names= ", ".join(a for a in artists),
            album_name=entry["album"],
            duration_ms=entry.get("duration_ms", None),
            spotify_url=entry["spotify_url"]
        )
        session.add(song)
        session.flush()
    print('Recent Songs added to database...')


def save_artists(entry, session):
    print('#####Saving artists data...#####')
    artists_dict = entry["artists"]

    for artist_data in artists_dict.items():
        print(artist_data)
        artist_name = artist_data[0]
        artist_id = artist_data[1]

        with session.no_autoflush:
            artist = session.query(Artist).filter_by(name=artist_name).first()

        if not artist:
            artist = Artist(
                artist_id=artist_id,
                name=artist_name,
                songs_list=entry["name"],
                albums_list=entry["album"]
            )

            session.add(artist)
            session.flush()
        else:
            # add song to CSV list if new
            songs = artist.songs_list.split(",") if artist.songs_list else []
            if entry["name"] not in songs:
                songs.append(entry["name"])
                artist.songs_list = ",".join(songs)
                print(f'Song `{entry["name"]}` added to the `{artist_name}\'s` list')
            
            albums = artist.albums_list.split(",") if artist.albums_list else []
            if entry["album"] not in albums:
                albums.append(entry["album"])
                artist.albums_list = ",".join(albums)
    
    print('Artists data stored....')



def save_album(entry, session):
    print('#######Saving Album data...#######')
    album_name = entry["album"]
    artists_dict = entry["artists"]
    album_type = entry["album_type"]
    album_id = entry["album_id"]
    album_link = entry["album_link"]
    
    artists = list(artists_dict.keys())

    with session.no_autoflush:
        album = session.query(Album).filter_by(album_id=album_id).first()

    if not album:
        album = Album(
            album_id=album_id,
            name=album_name,
            album_type=album_type,
            album_link = album_link,
            artist_names=", ".join(a for a in artists),
            songs_list=entry["name"]
        )
        session.add(album)
        session.flush()

    else:
        songs = album.songs_list.split(",") if album.songs_list else []
        print(songs)
        if entry["name"] not in songs:
            songs.append(entry["name"])
            album.songs_list = ",".join(songs)
            print(f"Added new song '{entry['name']}' to album '{album_name}'")
        else:
            print(f"Song '{entry['name']}' already exists in album '{album_name}'")


    print('Album added to database...')


from datetime import datetime

def parse_spotify_timestamp(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # fallback for timestamps without microseconds
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    

def save_history_entries(history_items):
    print('Starting `Save History`')
    session = Session()

    for entry in history_items:
        played_at_dt = parse_spotify_timestamp(entry["played_at"])

        # Check if history already exists
        with session.no_autoflush:
            exists = session.query(ListeningHistory).filter_by(
                song_id=entry["song_id"],
                played_at=played_at_dt
            ).first()

        if exists:
            continue  # avoid duplicates

        # Insert song + artist + album
        save_song(entry,session)
        save_artists(entry,session)
        save_album(entry,session)

        artists_dict = entry["artists"]
        artists = list(artists_dict.keys())


        # Insert history
        hist = ListeningHistory(
            song_id=entry["song_id"],
            name = entry["name"],
            artist_names = ", ".join(a for a in artists),
            spotify_url = entry["spotify_url"],
            played_at=played_at_dt,
            device=None,
            timestamp_added=datetime.now()
        )
        session.add(hist)
        session.flush()
    print('Saving History DONE...')

    session.commit()
    session.close()
