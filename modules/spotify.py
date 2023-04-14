from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_playlist(token, mood):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={mood}&type=playlist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    if len(json_result) == 0:
        print("No Playlist Found")
        return None
    else:
        return json_result[0]
  
token = get_token()
playlist_search_result = search_for_playlist(token, "SAD")
print(playlist_search_result)
