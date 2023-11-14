from dotenv import *
from requests import post, get, Response

#for testing
if __name__ == "modules.spotify":
    import modules.state as state
else:
    import state as state

import os
import base64
import json
import random

class X:
    def __getitem__(self, i):
        return f"Value {i}"

client_id = "016b59b007cf4494869123ecdb2f0687"              #Client ID
client_secret = "113ddc7d11f940f990e85be0a186399f"          #Client Secret

def main():
    state.update_spotify_values()
    token = get_token()                                                             #Calls to setup the client ID and Secret
    songs = get_track_reccomendation(token, state.currentGenre, state.spotify_dict["energy"] / 10, state.spotify_dict["tempo"] / 10, state.spotify_dict["valence"] / 100)      #Gets the track name from the computer mood
    #uri = get_uri(token, state.currentGenre, state.spotify_dict["energy"], state.spotify_dict["valence"], state.spotify_dict["tempo"])                         #Gets the track URI from the computer mood
    print(songs)                                                                    #Prints out the song title
    #print(uri)                                                                      #Prints the song URI
    print("-------------------------------------------")                            #Bar to make output more readable
    uri_to_embed(songs)

    return 0

#Function get_token sets up the client ID and secret in order to communicate with the Spotify API
def get_token():
    auth_string = client_id + ":" + client_secret                                   #Appends the Client ID and Secret together divided by a :
    auth_bytes = auth_string.encode("utf-8")                                        #Encodes the ID and Secret in UTF-8
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"                                  #Sets the API endpoint
    headers = {
        "Accept": "application/json",
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    t_result = json.loads(result.content)
    token = t_result["access_token"]
    print(__name__)
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

#Function to use the API to get a song that corresponds to the computer's mood.
#Returns the song's name
def get_track_reccomendation(token, genre, energy, tempo, valence):
        url = f"https://api.spotify.com/v1/recommendations"                                                     #Sets the API endpoint
        headers = get_auth_header(token)
        print("Energy: " + str(energy) + ", Tempo: " + str(tempo) + ", Valence: " + str(valence))
        query = f"?seed_genres={genre}&target_energy={energy}&target_tempo={tempo}&target_valence={valence}"     #Sets up the query with an f string to search for the genre, energy, tempo, and valence provided
        query_url = url + query
        result = get(query_url, headers=headers)
        print_headers(result)
        #print("Retry After: " +  + "s") #check for a 429
        song_result = json.loads(result.content)["tracks"][0]["name"]
        if (state.debugMode):
            print(song_result)
        song_url = json.loads(result.content)["tracks"][0]["external_urls"]["spotify"]
        song_uri = json.loads(result.content)["tracks"][0]["uri"]
        return song_uri                                                                                      #Returning the song's name

def print_headers(result : Response):
    try:
       print("Retry After: " + result.headers["retry-after"] + "s") #429 handler
    except: 
       print("No retry-after field.")
    finally:
        if state.debugMode:
            print(result.headers)

#Function to use the API to get a song that corresponds to the computer's mood
#Returns the song's URI to embed
def get_uri(token, genre, energy, tempo, valence):
        url = f"https://api.spotify.com/v1/recommendations"
        headers = get_auth_header(token)
        query = f"?seed_genres={genre}&target_energy={energy}&target_tempo={tempo}&target_vaence={valence}"     #Sets up the query with an f string to search for the genre, energy, tempo, and valence provided
        query_url = url + query
        result = get(query_url, headers=headers)
        song_uri = json.loads(result.content)["tracks"][0]["uri"]
        return song_uri
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
        <body style="background-color:#33475b">
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

if __name__ == "__main__":
    main()