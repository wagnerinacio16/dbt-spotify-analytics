from constants import *
import base64


import requests
import urllib3
import json
from urllib.parse import urlencode, urlparse, parse_qs
import pandas as pd

urllib3.disable_warnings()

def get_spotify_token(client_id: str, client_secret: str) -> str:
    """
    Gera um token de acesso do Spotify usando client credentials.
    """
   
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data, verify=True)
    response.raise_for_status()  # Levanta erro se não for 200
    return response.json()["access_token"]


# def get_saved_tracks(access_token):
#     url = f"{BASE_URL}/me/tracks"

#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }

#     params = {
#         "limit": 50
#     }

#     tracks = []

#     while url:
#         response = requests.get(url, headers=headers, params=params, verify=True)
#         response.raise_for_status()

#         data = response.json()

#         for item in data["items"]:
#             track = item["track"]

#             tracks.append({
#                 "track_id": track["id"],
#                 "track_name": track["name"],
#                 "album_id": track["album"]["id"],
#                 "album_name": track["album"]["name"],
#                 "added_at": item["added_at"]
#             })

#         url = data["next"]
#         params = None

#     return tracks


def get_saved_tracks(access_token):
    url = f"{BASE_URL}/me/tracks"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {"limit": 50}

    while url:
        response = requests.get(url, headers=headers, params=params, verify=True)
        response.raise_for_status()

        data = response.json()

        for item in data["items"]:
            track = item["track"]

            print(track)  # mostra todos os campos
            return  # apenas o primeiro para inspeção

        url = data["next"]
        params = None
        
def get_all_tracks(access_token):
    url = f"{BASE_URL}/me/tracks"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    #params = {"limit": 50}
    all_items = []

    while url:
        response = requests.get(url, headers=headers, verify=True)
        response.raise_for_status()

        data = response.json()
        all_items.extend(data.get("items", []))

        url = data.get("next")
        params = None

    return all_items        

# def normalize_saved_tracks(saved_tracks_items):
#     saved_tracks_rows = []
#     track_rows = []
#     album_rows = []
#     artist_rows = []
#     track_artist_rows = []

#     for item in saved_tracks_items:
#         track = item.get("track")

#         if not track:
#             continue

#         track_id = track.get("id")
#         album = track.get("album", {})
#         album_id = album.get("id")

#         # saved_tracks
#         saved_tracks_rows.append({
#             "track_id": track_id,
#             "added_at": item.get("added_at")
#         })

#         # tracks
#         track_rows.append({
#             "track_id": track_id,
#             "track_name": track.get("name"),
#             "duration_ms": track.get("duration_ms"),
#             "explicit": track.get("explicit"),
#             "disc_number": track.get("disc_number"),
#             "track_number": track.get("track_number"),
#             "is_local": track.get("is_local"),
#             "is_playable": track.get("is_playable"),
#             "track_type": track.get("type"),
#             "track_uri": track.get("uri"),
#             "track_href": track.get("href"),
#             "track_url_spotify": (track.get("external_urls") or {}).get("spotify"),
#             "isrc": (track.get("external_ids") or {}).get("isrc"),
#             "album_id": album_id
#         })

#         # albums
#         images = album.get("images") or []
#         album_image_url = images[0].get("url") if images else None
#         album_image_height = images[0].get("height") if images else None
#         album_image_width = images[0].get("width") if images else None

#         album_rows.append({
#             "album_id": album_id,
#             "album_name": album.get("name"),
#             "album_type": album.get("album_type"),
#             "release_date": album.get("release_date"),
#             "release_date_precision": album.get("release_date_precision"),
#             "total_tracks": album.get("total_tracks"),
#             "is_playable": album.get("is_playable"),
#             "album_type_object": album.get("type"),
#             "album_uri": album.get("uri"),
#             "album_href": album.get("href"),
#             "album_url_spotify": (album.get("external_urls") or {}).get("spotify"),
#             "album_image_url": album_image_url,
#             "album_image_height": album_image_height,
#             "album_image_width": album_image_width
#         })

#         # artists + track_artists
#         for artist_order, artist in enumerate(track.get("artists", []), start=1):
#             artist_id = artist.get("id")

#             artist_rows.append({
#                 "artist_id": artist_id,
#                 "artist_name": artist.get("name"),
#                 "artist_type": artist.get("type"),
#                 "artist_uri": artist.get("uri"),
#                 "artist_href": artist.get("href"),
#                 "artist_url_spotify": (artist.get("external_urls") or {}).get("spotify")
#             })

#             track_artist_rows.append({
#                 "track_id": track_id,
#                 "artist_id": artist_id,
#                 "artist_order": artist_order
#             })

#     # transforma em DataFrames
#     df_saved_tracks = pd.DataFrame(saved_tracks_rows).drop_duplicates(subset=["track_id"])
#     df_tracks = pd.DataFrame(track_rows).drop_duplicates(subset=["track_id"])
#     df_albums = pd.DataFrame(album_rows).drop_duplicates(subset=["album_id"])
#     df_artists = pd.DataFrame(artist_rows).drop_duplicates(subset=["artist_id"])
#     df_track_artists = pd.DataFrame(track_artist_rows).drop_duplicates(subset=["track_id", "artist_id"])

#     return {
#         "saved_tracks": df_saved_tracks,
#         "tracks": df_tracks,
#         "albums": df_albums,
#         "artists": df_artists,
#         "track_artists": df_track_artists
#     }


def get_audio_features(access_token, track_ids):

    url = "https://api.spotify.com/v1/audio-features"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "ids": ",".join(track_ids)
    }

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()

    return r.json()["audio_features"]

def chunk_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def get_artists_genres(access_token, artist_ids):
    """
    Busca detalhes dos artistas na API do Spotify e retorna:
    - df_artists
    - df_artist_genres

    artist_ids: lista de ids de artistas
    """
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    artist_rows = []
    artist_genres_rows = []

    unique_artist_ids = list({artist_id for artist_id in artist_ids if artist_id})

    for batch in chunk_list(unique_artist_ids, 50):
        url = f"{BASE_URL}/artists"
        params = {
            "ids": ",".join(batch)
        }

        response = requests.get(url, headers=headers, params=params, verify=True)
        response.raise_for_status()

        data = response.json()

        for artist in data.get("artists", []):
            if not artist:
                continue

            artist_id = artist.get("id")

            artist_rows.append({
                "artist_id": artist_id,
                "artist_name": artist.get("name"),
                "artist_popularity": artist.get("popularity"),
                "artist_followers_total": (artist.get("followers") or {}).get("total"),
                "artist_href": artist.get("href"),
                "artist_uri": artist.get("uri"),
                "artist_type": artist.get("type"),
                "artist_url_spotify": (artist.get("external_urls") or {}).get("spotify")
            })

            for genre in artist.get("genres", []):
                artist_genres_rows.append({
                    "artist_id": artist_id,
                    "genre_name": genre
                })

    df_artists = pd.DataFrame(artist_rows).drop_duplicates(subset=["artist_id"])
    df_artist_genres = pd.DataFrame(artist_genres_rows).drop_duplicates(subset=["artist_id", "genre_name"])

    return df_artists, df_artist_genres


def search_spotify_track(token: str, query: str, limit: int = 1) -> dict:
    """
    Busca por uma música no Spotify usando o token de acesso.
    """
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": limit}

    response = requests.get(url, headers=headers, params=params, verify=REQUESTS_VERIFY)
    response.raise_for_status()
    return response.json()

def print_track_info(data: dict):
    """
    Imprime informações da primeira faixa encontrada na busca.
    """
    if data['tracks']['items']:
        track = data['tracks']['items'][0]
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        album_name = track['album']['name']
        duration_ms = track['duration_ms']
        release_date = track['album']['release_date']
        
        print(f"Artista: {artist_name}")
        print(f"Faixa: {track_name}")
        print(f"Álbum: {album_name}")
        print(f"Duração (ms): {duration_ms}")
        print(f"Data de lançamento: {release_date}")
    else:
        print("Nenhuma faixa encontrada.")
        
def get_user(access_token):

    url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers, verify=False)

    print("STATUS:", response.status_code)

    if response.status_code == 401:
        raise Exception("Token inválido ou expirado")

    response.raise_for_status()

    return response.json()   


def extract_code(callback_url):
    parsed = urlparse(callback_url)
    query = parse_qs(parsed.query)

    if "error" in query:
        raise Exception(f"Erro no callback: {query['error'][0]}")

    if "code" not in query:
        raise Exception("Code não encontrado")

    return query["code"][0]

def get_token(code):
    url = "https://accounts.spotify.com/api/token"

    auth = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64 = base64.b64encode(auth.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    r = requests.post(url, headers=headers, data=data, verify=False)

    print("TOKEN STATUS:", r.status_code)
    print("TOKEN BODY:", r.text)

    if r.status_code != 200:
        raise Exception(f"Erro ao gerar token: {r.text}")

    return r.json()

# # Exemplo de uso
# if __name__ == "__main__":
   
    
#     print(client_id)
#     print(client_secret)

#     if not client_id or not client_secret:
#         raise ValueError("Variáveis de ambiente SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET devem estar definidas.")

#     token = get_spotify_token(client_id, client_secret)
#     print("TOKEN GERADO:")
#     print(token)

#     # Teste da API
#     result = search_spotify_track(token, "Quando A Fonte Secar", limit=2)
#     print("\nTESTE DA API - Busca por 'Quando A Fonte Secar':")
#     print_track_info(result)
