from dotenv import load_dotenv
from requests import post, get
import state as state
import os
import base64
import json
import random

class X:
    def __getitem__(self, i):
        return f"Value {i}"

client_id = "016b59b007cf4494869123ecdb2f0687"
client_secret = "d97260bd8c6645848b0c571c7eff90a0"

def main():
    token = get_token()
    emotion = state.emotion
    songs = get_track_reccomendation(token, rock, 25, 50, 75)

    uris = []

    for index, item in enumerate(songs, start=0):
        try:
            uri = item["track"]["uri"]

            uris.append(uri)

        except TypeError or uri == "":
            pass

    print("-------------------------------------------")
    print("Emotion: " + emotion)
    #from modules.processing import uri_to_embed
    final_uri = random.choice(uris)
    uri_to_embed(final_uri)
    print(final_uri)
    print(song_result)
    return final_uri

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

def get_track_reccomendation(token, genre, energy, tempo, valence):
        url = f"https://api.spotify.com/v1/recommendations"
        headers = get_auth_header(token)
        query = f"?seed_genres={genre}&target_energy={energy}&target_tempo={tempo}&target_vaence={valence}"
        query_url = url + query
        result = get(query_url, headers=headers)
        song_result = json.loads(result.content)
        print(song_result)
        return song_result
# moved from processing because of the tasks I created bitching about this function -D
def uri_to_embed(uri): 
    """
    <html>
        <script src=\"https://open.spotify.com/embed-podcast/iframe-api/v1\" async></script>
        <script>
            window.onSpotifyIframeApiReady = (IFrameAPI) => {
                const element = document.getElementById('embed-iframe');
                const options = {
                    uri: '[[URI]]'
                };
                const callback = (EmbedController) => {};
                IFrameAPI.createController(element, options, callback);
            };
        </script>
        <body> 
            <div id="embed-iframe"></div>
        </body> 
    </html>
    """
    rough = uri_to_embed.__doc__
    toWrite = rough.replace("[[URI]]", str(uri))
    path = "embed.html"
    with open(path, 'w') as html:
        html.write(toWrite)
    
    return path

