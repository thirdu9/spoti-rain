from spotify_client import current_track, get_recently_played
from scheduler import start_scheduler
from db import init_db


init_db()
start_scheduler()