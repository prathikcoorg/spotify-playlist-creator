import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


Client_ID = "ae45fba94cc3486cb3f8447d006843b0"
Client_Secret = "6ab0516b5df24dec9fa0827fd2aa03f2"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url ="https://www.billboard.com/charts/hot-100/"+date

response = requests.get(url,headers=header)
songs = response.text
# print(songs)

soup = BeautifulSoup(songs,"html.parser")
song_name = soup.select("ul li h3")
songs_name = [song.getText().strip() for song in song_name]
for song in songs_name:
     if "Expand" in song or "menu" in song or 'Account' in song:
        break
     print(song)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.org/callback",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt",
        username="billboard to spotify", 
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for song in songs_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)






















































































# last_song_index = songs_name.index - 1  
# filtered_songs = songs_name[:last_song_index]
# for song in filtered_songs:
#     print(song)


# print(songs_name)
# for song in songs_name(len(songs_name)-1):
#     print(song)
# print(songs_name)
# for song in song_name:
#     songs_name = song.getText()
#     print(songs_name)
# print(song_name)

