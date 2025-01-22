import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Warner Music Group Dashboard",
    page_icon=":musical_note:",
    layout="wide",
    initial_sidebar_state="expanded")

# load data
df = pd.read_csv("final_tracks.csv")
filtred = pd.read_csv("filtered_data.csv")
df.drop(columns=['instrumentalness', "tempo"], inplace=True)
# filter
warner_artists = df[df['record_label'] == 'Warner Music Group'].sort_values(by='popularity', ascending=False)
artist_names = warner_artists['artist_name'].unique()
# Get unique labels excluding Warner Music Group
other_labels = filtred[filtred['record_label'] != 'Warner Music Group']['record_label'].unique()

# Main UI
st.title(':notes: Warner Music Group Collaboration Tool')

# Sidebar
st.sidebar.title("Filters and Visualization")

# Popularity Filter with Slider
popularity_range = st.sidebar.slider(
    "Set Popularity Range:",
    min_value=75,
    max_value=100,
    value=(75, 85),
    step=1
)

filtered_warner_artists = warner_artists[
    (warner_artists['popularity'] >= popularity_range[0]) &
    (warner_artists['popularity'] <= popularity_range[1])
]

# Plotly Chart
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=filtered_warner_artists['popularity'],
        y=filtered_warner_artists['followers'],
        mode='markers',
        marker=dict(size=10, color='purple'),
        text=filtered_warner_artists['artist_name']
    )
)

fig.update_layout(
    title='Popularity vs Followers (Filtered)',
    xaxis=dict(title='Popularity', range=[75, 100], showgrid=True),
    yaxis=dict(title='Followers', showgrid=True)
)

# Show Chart in Sidebar
st.sidebar.plotly_chart(fig, use_container_width=True)

# Display filtered table in Sidebar
st.sidebar.markdown(f"#### Artists with popularity between {popularity_range[0]} and {popularity_range[1]}:")

# Remove duplicates based on 'artist_name', reset index to hide it
filtered_warner_artists_unique = warner_artists[['artist_name', 'record_label', 'popularity', 'followers', ]].drop_duplicates(subset=['artist_name']).reset_index(drop=True)
# Display the dataframe in sidebar with the specified columns and hidden index
st.sidebar.dataframe(filtered_warner_artists_unique, use_container_width=True, hide_index=True)




# Helper function to clean artist names
def clean_artist_name(artist_name):
    return "_".join(artist_name.strip().replace(" ", "_").split())
# Function to get artist image from Wikipedia API
def get_artist_image(artist_name):
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": artist_name,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 500
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "thumbnail" in page_data:
                return page_data["thumbnail"]["source"]
    return None

# Define a dictionary to map Warner artists to their Spotify track URLs
artist_spotify_urls = {
    "Bruno Mars": "https://open.spotify.com/embed/track/2plbrEY59IikOBgBGLjaoe",
    "Charli XCX": "https://open.spotify.com/embed/track/7CwWhMGWICOl2ICwbk3QTE",
    "Ava Max": "https://open.spotify.com/embed/track/1KixkQVDUHggZMU9dUobgm",
    "Taylor Swift": "https://open.spotify.com/embed/track/36t6frENUtCYKuZus6aYDO",
    "The Weeknd": "https://open.spotify.com/embed/track/1Es7AUAhQvapIcoh3qMKDL",
    "Eminem": "https://open.spotify.com/embed/track/4HMUrFl8y6rQCzEbaGEkcj",
    "Post Malone": "https://open.spotify.com/embed/track/6nLUacmejwxurxcknrSWFG",
    "Future": "https://open.spotify.com/embed/track/3xqD0CgWTjZ6RuvXaVyKEC",
    "Metro Boomin": "https://open.spotify.com/embed/track/7nQXU7lu0RhVOSmsa3teKj",
    "21 Savage": "https://open.spotify.com/embed/track/1qIwin7JMVuX70qN6wD8ww",
    "Bring Me The Horizon": "https://open.spotify.com/embed/track/3ySqZ8yGoh4Emi9HiPCCdP",
    "Blink 182": "https://open.spotify.com/embed/track/6sjtUtT0lWNTQ2Xy9GFVML",
    "Troye Sivan": "https://open.spotify.com/embed/track/7CwWhMGWICOl2ICwbk3QTE",
    "Jimin": "https://open.spotify.com/embed/track/7tI8dRuH2Yc6RuoTjxo4dU",
    "Lil Baby": "https://open.spotify.com/embed/track/4xbfYPpKIKtGU4iEK3WW2C",
    "Quavo": "https://open.spotify.com/embed/track/5CJ3DQPUmrtI2lqRjPk4K6",
    "Big Sean": "https://open.spotify.com/track/1ymWIr4E5x6xORlDO0bXlP",
    "Benson Boone": "https://open.spotify.com/embed/track/1QxxBUAx42J8pIFYJJR880",
    "Charlie Puth": "https://open.spotify.com/embed/track/1jEBSDN5vYViJQr78W7jr2",
    "David Guetta": "https://open.spotify.com/embed/track/0IAFmrpi9KF0PP3LONJonm",
    }


# 1. Select a Warner Music Group artist with placeholder (default message)
selected_warner_artist = st.selectbox(
    'Select an artist from Warner Music Group',
    options=['Select an artist'] + list(artist_names),  # Placeholder
    index=0  # Default selection
)
# Ensure an artist is selected before proceeding

# Retrieve the Spotify track URL for the selected artist
track_url = artist_spotify_urls.get(selected_warner_artist)

if selected_warner_artist == 'Select an artist':
    st.warning("Please select an artist before proceeding.")

else:
    # Generate Wikipedia URL
    base_url = "https://en.wikipedia.org/wiki/"
    artist_url = base_url + clean_artist_name(selected_warner_artist)
    # Check if the Wikipedia page exists
    response = requests.get(artist_url)
    if response.status_code == 200:
        st.markdown(f"### Wikipedia Page for {selected_warner_artist}")
        st.markdown(f"[Visit {selected_warner_artist}'s Wikipedia Page]({artist_url})")
        # Retrieve artist image
        image_url = get_artist_image(clean_artist_name(selected_warner_artist))
        # Retrieve all data for the selected Warner artist
        df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%Y', errors='coerce')
        warner_artist_data = df[df['artist_name'] == selected_warner_artist]
        last_track = warner_artist_data.sort_values(by='release_date', ascending=False).iloc[0]
        # Create two columns
        col1, col2 = st.columns([1, 2])  # Adjust column width ratios as needed
        with col1:
            if image_url:
                st.image(
                    image_url,
                    caption=f"{selected_warner_artist}",
                    use_column_width=True  # Let the image fill this column's width
                )
            else:
                st.write("Image not found.")
        with col2:
            st.subheader(f"Information for {selected_warner_artist}:")
            st.write(f"**Track name:** {last_track['track_name']}")
            st.write(f"**Release Date:** {last_track['release_date'].strftime('%Y-%m-%d')}")
            st.write(f"**Popularity:** {last_track['popularity']}")
            st.write(f"**Followers:** {last_track['followers']}")
            components.iframe(track_url)
    else:
        st.write(f"Sorry, no Wikipedia page found for {selected_warner_artist}.")
    # 2. Select a competitor label with placeholder (default message)
    selected_label = st.selectbox(
        'Select a label for collaboration',
        options=['Select a label'] + list(other_labels),  # Placeholder
        index=0  # Default selection
    )
    # Ensure a label is selected before proceeding
    if selected_label == 'Select a label':
        st.warning("Please select a label before proceeding.")
    else:
        # Filter artists from the selected competitor label
        filtered_artists = filtred[filtred['record_label'] == selected_label]
        # Function to evaluate collaboration compatibility
        def is_compatible(artist1, artist2):
            return (
                abs(artist1['danceability'] - artist2['danceability']) <= 0.1 and
                abs(artist1['energy'] - artist2['energy']) <= 0.1 and
                abs(artist1['valence'] - artist2['valence']) <= 0.1 and
                abs(artist1['tempo_adjusted'] - artist2['tempo_adjusted']) <= 0.5 and
                abs(artist1['popularity'] - artist2['popularity']) <= 10
            )
        # Evaluate compatibility
        compatible_artists = filtered_artists[
            filtered_artists.apply(lambda x: is_compatible(warner_artist_data.iloc[0], x), axis=1)
        ]
        # Remove duplicates and sort by popularity
        compatible_artists = compatible_artists.drop_duplicates(subset=['artist_name'])
        compatible_artists = compatible_artists.sort_values(by='popularity', ascending=False)
        # Display top 10 results
        compatible_artists_top_10 = compatible_artists.head(10)
        # Display HTML table
        html_table = compatible_artists_top_10[['artist_name', 'popularity', 'followers']].to_html(index=False)
        st.markdown(html_table, unsafe_allow_html=True)
        # Create a dropdown for selecting an artist from the compatible list
        st.subheader("Select an artist for further analysis:")
        # Add placeholder and populate dropdown with artist names
        compatible_artist_names = ['Select an artist'] + list(compatible_artists_top_10['artist_name'].unique())
        selected_compatible_artist = st.selectbox(
            "Compatible Artists",
            options=compatible_artist_names,
            index=0  # Default selection as placeholder
        )
        # Ensure an artist is selected
        if selected_compatible_artist == 'Select an artist':
            st.warning("Please select an artist from the list for further analysis.")
            # Retrieve the Spotify track URL for the selected artist
        else:
            track_url2 = artist_spotify_urls.get(selected_compatible_artist)
        
            st.write(f"You selected: **{selected_compatible_artist}**")
            # Generate Wikipedia URL
            compatible_artist_url = base_url + clean_artist_name(selected_compatible_artist)
            # Check if the Wikipedia page exists
            response = requests.get(compatible_artist_url)
            if response.status_code == 200:
                st.markdown(f"### Wikipedia Page for {selected_compatible_artist}")
                st.markdown(f"[Visit {selected_compatible_artist}'s Wikipedia Page]({compatible_artist_url})")
                # Retrieve artist image
                compatible_image_url = get_artist_image(clean_artist_name(selected_compatible_artist))
                col3, col4 = st.columns([1, 2])
                with col3:
                    if compatible_image_url:
                        st.image(
                            compatible_image_url,
                            caption=f"{selected_compatible_artist}",
                            use_column_width=True  # Let the image fill this column's width
                        )
                    else:
                        st.write("Image not found.")
                with col4:
                    # Retrieve all data for the selected compatible artist
                    compatible_artist_data = filtred[filtred['artist_name'] == selected_compatible_artist]
                    last_compatible_track = compatible_artist_data.sort_values(by='release_date', ascending=False).iloc[0]
                    # Retrieve all data for the selected compatible artist
                    compatible_artist_data = filtred[filtred['artist_name'] == selected_compatible_artist]
                    last_compatible_track = compatible_artist_data.sort_values(by='release_date', ascending=False).iloc[0]
                    # Show additional information about the latest track
                    st.subheader(f"Information for {selected_compatible_artist}:")
                    st.write(f"**Track name:** {last_compatible_track['track_name']}")
                    st.write(f"**Release Date:** {last_compatible_track['release_date']}")
                    st.write(f"**Popularity:** {last_compatible_track['popularity']}")
                    st.write(f"**Followers:** {last_compatible_track['followers']}")
                    components.iframe(track_url2)

                # Plot radial chart for both artists
                st.subheader(":bar_chart: Radial Comparison of Artist Features")
                categories = ['danceability', 'energy', 'valence', 'tempo_adjusted']

                # Ensure Warner artist's data is correctly extracted
                if not warner_artist_data.empty:
                    warner_values = [
                        warner_artist_data[cat].mean() for cat in categories
                    ]
                else:
                    st.error("Failed to retrieve data for the selected Warner Music Group artist.")
                    warner_values = [0] * len(categories)

                # Ensure Compatible artist's data is correctly extracted
                if not compatible_artist_data.empty:
                    compatible_values = [
                        compatible_artist_data[cat].mean() for cat in categories
                    ]
                else:
                    st.error("Failed to retrieve data for the selected compatible artist.")
                    compatible_values = [0] * len(categories)

                # Close the radar chart by repeating the first value and category
                categories += [categories[0]]
                warner_values += [warner_values[0]]
                compatible_values += [compatible_values[0]]

                # Create the radar chart using Plotly
                fig = go.Figure()

                # Add Warner artist trace
                fig.add_trace(go.Scatterpolar(
                    r=warner_values,
                    theta=categories,
                    fill='toself',
                    name=selected_warner_artist,
                    line=dict(color='rgba(0, 128, 255, 0.7)', width=3),
                    marker=dict(size=8, color='rgba(0, 128, 255, 0.8)'),
                    hoverinfo='all',
                ))

                # Add competitor artist trace
                fig.add_trace(go.Scatterpolar(
                    r=compatible_values,
                    theta=categories,
                    fill='toself',
                    name=selected_compatible_artist,
                    line=dict(color='rgba(255, 0, 0, 0.7)', width=3),
                    marker=dict(size=8, color='rgba(255, 0, 0, 0.8)'),
                    hoverinfo='all',
                ))

                # Update layout styling
                fig.update_layout(
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(
                            visible=True,
                            tickvals=[0, 0.25, 0.5, 0.75, 1],
                            tickfont=dict(size=12, color="white"),
                            showline=True, linewidth=2, linecolor="white"
                        ),
                        angularaxis=dict(
                            tickfont=dict(size=14, color="white"),
                            showline=True, linewidth=2, linecolor="white"
                        ),
                    ),
                    title="Feature Comparison Between Artists",
                    showlegend=True,
                    template='plotly_dark',
                    margin=dict(l=20, r=20, t=50, b=50),
                )

                # Display the radar chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)
