from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

engine = create_engine(
    "sqlite:///spotify_data.db",connect_args={"check_same_thread": False},
    poolclass=NullPool
)
with engine.connect() as conn:
    conn.execute(text("PRAGMA journal_mode=WAL;"))

Base = declarative_base()
Session = sessionmaker(bind=engine)

class Song(Base):
    __tablename__ = "songs"
    song_id = Column(String, primary_key=True)
    name = Column(String)
    artist_names = Column(Text)
    album_name = Column(String)
    duration_ms = Column(Integer)
    spotify_url = Column(String)

class ListeningHistory(Base):
    __tablename__ = "listening_history"
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(String)
    name = Column(String)
    artist_names = Column(Text)
    spotify_url = Column(String)
    played_at = Column(DateTime)
    device = Column(String, nullable=True)
    timestamp_added = Column(DateTime)

class Artist(Base):
    __tablename__ = "artists"
    artist_id = Column(String, primary_key=True)
    name = Column(String)
    songs_list = Column(Text)   # CSV list of song_ids or names
    albums_list = Column(Text)

class Album(Base):
    __tablename__ = "albums"
    album_id = Column(String, primary_key=True)
    album_link = Column(String)
    album_type = Column(String)
    name = Column(String)
    artist_names = Column(Text)
    songs_list = Column(Text)


class AudioFeatures(Base):
    __tablename__ = "audio_features"

    song_id = Column(String, primary_key=True)  # FK to songs
    danceability = Column(Float)
    energy = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    speechiness = Column(Float)
    liveness = Column(Float)


def init_db():
    Base.metadata.create_all(engine)
