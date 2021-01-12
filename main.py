import requests
import config
from bs4 import BeautifulSoup
import spotipy
from pprint import pprint

from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_REDIRECT_URI = 'http://example.com'


date = input("Which year you would like to travel to? Type the date in the format YYYY-MM-DD: ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

music_list = soup.find_all(name="span", class_="chart-element__information__song")

songs = [music.get_text() for music in music_list]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-modify-private",
    cache_path="token.txt"
  )
)

song_uris = []
user_id = sp.current_user()['id']
year = date.split("-")[0]
for song in songs:
   result = sp.search(q=f"track:{song} year:{year}", type="track")
   try:
       uri = result["tracks"]["items"][0]['uri']
       song_uris.append(uri)
   except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


user_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=True, collaborative=False, description=f"Top 100 Billboard songs of {date}")

add_songs = sp.user_playlist_add_tracks(user=user_id, playlist_id=user_playlist["id"], tracks=song_uris)

print(add_songs)







