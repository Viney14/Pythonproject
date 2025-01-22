import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np

# Spotify API credentials (replace with your own client_id and client_secret)
CLIENT_ID = 'your_spotify_client_id'
CLIENT_SECRET = 'your_spotify_client_secret'

# Function to get Spotify access token
def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    response = requests.post(
        url,
        data=data,
        headers={
            "Authorization": f"Basic {requests.utils.quote(CLIENT_ID)}:{requests.utils.quote(CLIENT_SECRET)}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    return response.json().get("access_token")

# Function to get the latest track for an artist
def get_latest_track(artist_name):
    token = get_spotify_token()
    if not token:
        return None
    search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        results = response.json().get("tracks", {}).get("items", [])
        if results:
            return results[0].get("uri"), results[0].get("name")
    return None, None

# Existing Warner Music Group dataset
df = pd.read_csv("final_tracks.csv")
df.drop(columns=['instrumentalness', "tempo"], inplace=True)
warner_artists = df[df['record_label'] == 'Warner Music Group'].sort_values(by='popularity', ascending=False)
artist_names = warner_artists['artist_name'].unique()

# Streamlit UI
st.title(':notes: Warner Music Group Collaboration Tool')

# Select a Warner Music Group artist
selected_warner_artist = st.selectbox(
    'Select an artist from Warner Music Group',
    options=['Select an artist'] + list(artist_names),
    index=0
)

if selected_warner_artist != 'Select an artist':
    # Retrieve the last track details
    warner_artist_data = df[df['artist_name'] == selected_warner_artist]
    last_track = warner_artist_data.sort_values(by='release_date', ascending=False).iloc[0]

    st.subheader(f"Information for {selected_warner_artist}:")
    st.write(f"**Track name:** {last_track['track_name']}")
    st.write(f"**Release Date:** {last_track['release_date']}")
    st.write(f"**Popularity:** {last_track['popularity']}")
    st.write(f"**Followers:** {last_track['followers']}")

    # Get the Spotify track URI
    track_uri, track_name = get_latest_track(selected_warner_artist)
    if track_uri:
        st.subheader(f"Play '{track_name}' on Spotify:")
        iframe_src = f"https://open.spotify.com/embed/track/{track_uri.split(':')[-1]}?utm_source=generator"
        components.iframe(iframe_src, height=80, width=300)
    else:
        st.warning("Could not find the track on Spotify.")

        curl -X GET "https://api.spotify.com/v1/search?q=artist_name&type=track&limit=1" -H "Authorization: Bearer <ACCESS_TOKEN>"

