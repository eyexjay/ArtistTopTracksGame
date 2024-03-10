from dotenv import load_dotenv
import os
import base64
from requests import post, get
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
    token =json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1" # want most popular so limit = 1

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists.")
        return None
    return json_result[0]

def get_songs_by_artist(token, artisit_id):
        url = f"https://api.spotify.com/v1/artists/{artisit_id}/top-tracks?country=US"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["tracks"]
        return json_result

# print("Enter an artist's name to get their top ten tracks in the US")
# artist_name = input()
# token = get_token()
# result = search_for_artist(token, artist_name)
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)

# for idx, song in enumerate(songs):
#      print(f"{idx + 1}. {song['name']}")


## Top Ten Track Guessing Game ###
     
def game():
    print("Enter an artist's name to guess their top ten tracks in the US")
    artist_name = input()
    token = get_token()
    result = search_for_artist(token, artist_name)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)

    print(f"You have 10 guesses {artist_name}'s top ten tracks.")
    correct = 0
    for i in range(10):
        print("Guess #", i + 1)
        guess =  input()

        found = False
        for song in songs:
             if guess.lower() == song["name"].lower():
                  correct +=1
                  found = True
                  print("That is correct!")
                  break
        if not found:
             print("That is not a top ten track")
    
    print(f"Game Over: You guessed {correct}/10 tracks correctly")
    print("The top ten tracks are:")
    for idx, song in enumerate(songs):
     print(f"{idx + 1}. {song['name']}")

    
game()
          
