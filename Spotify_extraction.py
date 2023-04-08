import spotipy
import pandas as pd
import math
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
import sqlite3
import json


CLIENT_ID = "a29e1acdc35549448a61bf0948282b5d"
CLIENT_PRIVATE_KEY = "0f75a36819744589a057f0330a1b0a56"
redirect_uri ='https://www.google.com/'

scope = "user-top-read"

oauth_object = spotipy.SpotifyOAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_PRIVATE_KEY,
                                    redirect_uri=redirect_uri,
                                    scope=scope)

token_dict = oauth_object.get_access_token()
token = token_dict['access_token']

spotify_object = spotipy.Spotify(auth=token)

top_tracks = spotify_object.current_user_top_tracks(limit=50)
top_tracks_df = pd.json_normalize(top_tracks['items'])

column_list = ['id','name','album.name','artists','popularity','album.total_tracks','album.release_date']

top_tracks_df = top_tracks_df[column_list]

top_tracks_df['artists'] = top_tracks_df.artists.str[0].str['name']

column_names = {
    'id':'id',
    'artists':'artists',
    'name':'track_name',
    'popularity':'popularity',
    'album.name':'album',
    'album.total_tracks':'total_tracks_in_album',
    'album.release_date':'album_release'
}

top_tracks_df = top_tracks_df.rename(columns=column_names)
top_tracks_df['album_release'] = pd.to_datetime(top_tracks_df['album_release'],format='mixed')

top_tracks_df.to_csv("top_tracks_df.csv")