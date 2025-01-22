import requests
import streamlit as st

# Function to search for a track on Spotify by title and artist
def search_spotify_track(song_title, artist_name):
    base_url = "https://api.spotify.com/v1/search"
    query = f"track:{song_title} artist:{artist_name}"
    
    # Prepare the query parameters
    params = {
        "q": query,
        "type": "track",
        "limit": 1  # Limit results to 1 (most relevant result)
    }
    
    # Make the GET request to the Spotify API
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])
        
        if tracks:
            track = tracks[0]  # Take the first (most relevant) track
            track_name = track.get('name', 'Unknown song')
            track_url = track.get('external_urls', {}).get('spotify', '#')
            return track_name, track_url
    return None, None

# Streamlit UI
st.title(':notes: Spotify Song Search')

# Select a Warner Music Group artist (example for testing)
selected_warner_artist = st.selectbox('Select an artist from Warner Music Group', ['Adele', 'Ed Sheeran', 'Bruno Mars'])

# Enter a song name (this can be dynamically chosen or hardcoded for testing)
song_name = "Shape of You"  # Replace with actual song name dynamically
artist_name = selected_warner_artist  # Replace with selected artist name dynamically

if selected_warner_artist:
    st.write(f"Fetching the latest track for {selected_warner_artist}...")
    song_title, song_url = search_spotify_track(song_name, artist_name)

    if song_title:
        st.subheader(f"Latest track: {song_title}")
        st.markdown(f"Listen to the song on [Spotify]({song_url})")
    else:
        st.write(f"No tracks found for {song_name} by {artist_name}.")
