import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker
from db import engine, ListeningHistory, Song

Session = sessionmaker(bind=engine)

def top_artists():
    session = Session()

    q = session.query(ListeningHistory, Song).join(
        Song, ListeningHistory.song_id == Song.song_id
    ).all()

    data = []
    for h, s in q:
        for artist in s.artist_names.split(", "):
            data.append(artist)

    df = pd.DataFrame(data, columns=["artist"])
    top = df["artist"].value_counts().head(10)

    top.plot(kind="bar")
    plt.title("Top 10 Artists by Play Count")
    plt.ylabel("Plays")
    plt.show()

def top_songs():
    session = Session()
    q = session.query(ListeningHistory, Song).join(
        Song, ListeningHistory.song_id == Song.song_id
    ).all()

    df = pd.DataFrame([s.name for _, s in q], columns=["song"])
    top = df["song"].value_counts().head(10)

    top.plot(kind="bar", color="green")
    plt.title("Top 10 Songs")
    plt.ylabel("Plays")
    plt.show()



import seaborn as sns
import numpy as np

def listening_heatmap():
    session = Session()
    q = session.query(ListeningHistory).all()

    rows = []
    for h in q:
        dt = pd.to_datetime(h.played_at)
        rows.append([dt.dayofweek, dt.hour])

    df = pd.DataFrame(rows, columns=["day", "hour"])

    heatmap = df.groupby(["day","hour"]).size().unstack(fill_value=0)

    plt.figure(figsize=(12,6))
    sns.heatmap(heatmap, cmap="Blues")
    plt.title("Listening Heatmap (Day of Week × Hour)")
    plt.xlabel("Hour")
    plt.ylabel("Day (0=Mon)")
    plt.show()


def monthly_trend():
    session = Session()
    q = session.query(ListeningHistory).all()

    df = pd.DataFrame([h.played_at for h in q], columns=["played_at"])
    df["played_at"] = pd.to_datetime(df["played_at"])
    df["month"] = df["played_at"].dt.to_period("M")

    trend = df["month"].value_counts().sort_index()

    trend.plot(kind="line", marker="o")
    plt.title("Monthly Listening Trend")
    plt.ylabel("Total Plays")
    plt.show()

if __name__ == '__main__':
    while(True):
        choice = int(input(
        """
1. Top 10 Artists
2. Top 10 Songs
3. Heatmap
4. Monthly Trend
5. Exit
Choose: _"""
    ))
        if choice == 1:
            top_artists()
        elif choice == 2:
            top_songs()
        elif choice == 3:
            listening_heatmap()
        elif choice == 4:
            monthly_trend()
        elif choice == 5:
            Session.close()
            break

        else:
            print("Choose one of the above")
    