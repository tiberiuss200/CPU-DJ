from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json
import random

class X:
    def __getitem__(self, i):
        return f"Value {i}"


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def main():
    token = get_token()
    result = search_for_playlist(token, "SAD")
    playlist_id = get_playlist_id(token, "SAD")
    songs = get_song(token, playlist_id)



        #to[0] = "Passed - QLabel Set Text"
    array1 = []
    array2 = []



    for index, item in enumerate(songs, start=0):
        try:
            name = item["track"]["name"]
            uri = item["track"]["uri"]
            index = index + 1
            # print(index, name)
            arrayName = [name]
            arrayUri = [uri]
            # print(mainWindow.array1)
            array1 = [index] + arrayName + arrayUri
            array2 = array2 + array1

        except TypeError or name == "":
            pass

    print("-------------------------------------------")

        #mainWindow.display[0] = "test text2"
    print(random.choice(array1))
        # index 2 of array2 = song number
        # index 0 of array2 = song title
        # index 1 of array2 = URI
    from modules.processing import uri_to_embed
    uri_to_embed(uri)




    return songs


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Accept": "application/json",
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    t_result = json.loads(result.content)
    token = t_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_playlist(token, mood):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={mood}&type=playlist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    playlist_result = json.loads(result.content)["playlists"]["items"]
    if len(playlist_result) == 0:
        print("No Playlist Found")
        return None
    else:
        return playlist_result

def get_playlist_id(token, mood):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={mood}&type=playlist&limit=1&offset=100"
    query_url = url + query
    result = get(query_url, headers=headers)
    id_result = json.loads(result.content)["playlists"]["items"][0]['id']
    if len(id_result) == 0:
        print("No Playlist Found")
        return None
    else:
        return id_result

def get_song(token, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        song_result = json.loads(result.content)["items"]
        return song_result



