import streamlit as st
import streamlit.components.v1 as components

# Define a dictionary to map Warner artists to their Spotify track URLs
artist_spotify_urls = {
    "Artist 1": "https://open.spotify.com/embed/track/59BweHnnNQc5Y55WO30JuK?utm_source=generator",
    "Artist 2": "https://open.spotify.com/embed/track/1zZywn6Pfn04xgXtjmuy6G?utm_source=generator",
    "Artist 3": "https://open.spotify.com/embed/track/6JjDE8K8qxJdOdzM0jZLlL?utm_source=generator",
    # Add more artists and their track URLs here
}

# Streamlit UI
st.title(':notes: Warner Music Group Collaboration Tool')

# Select a Warner Music Group artist with placeholder
selected_warner_artist = st.selectbox(
    'Select an artist from Warner Music Group',
    options=['Select an artist'] + list(artist_spotify_urls.keys()),  # Use artist names as options
    index=0  # Default selection
)

# Ensure an artist is selected before proceeding
if selected_warner_artist == 'Select an artist':
    st.warning("Please select an artist before proceeding.")
else:
    # Retrieve the Spotify track URL for the selected artist
    track_url = artist_spotify_urls.get(selected_warner_artist)

    if track_url:
        # Embed the Spotify player
        st.write(f"Now playing: **{selected_warner_artist}**")
        components.iframe(track_url)  # Embed the Spotify player
    else:
        st.write(f"Sorry, no track URL found for {selected_warner_artist}.")
