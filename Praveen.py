import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="Warner Music Group Dashboard",
    page_icon=":musical_note:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
df = pd.read_csv('/Users/akashmohan/Desktop/Last version/final_tracks.csv')
filtred = pd.read_csv('/Users/akashmohan/Desktop/Last version/filtered_data.csv')
df.drop(columns=['instrumentalness', "tempo"], inplace=True)

# Filter data
warner_artists = df[df['record_label'] == 'Warner Music Group'].sort_values(by='popularity', ascending=False)
artist_names = warner_artists['artist_name'].unique()
other_labels = filtred[filtred['record_label'] != 'Warner Music Group']['record_label'].unique()

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
st.sidebar.dataframe(filtered_warner_artists[['artist_name', 'popularity', 'followers']], use_container_width=True)

# Select Warner artist
selected_warner_artist = st.selectbox(
    'Select an artist from Warner Music Group',
    options=['Select an artist'] + list(artist_names),
    index=0
)

if selected_warner_artist == 'Select an artist':
    st.warning("Please select an artist before proceeding.")
else:
    # Get data for selected artist
    warner_artist_data = df[df['artist_name'] == selected_warner_artist]
    warner_artist_data['release_date'] = pd.to_datetime(warner_artist_data['release_date'], errors='coerce')
    last_track = warner_artist_data.sort_values(by='release_date', ascending=False).iloc[0]

    # Wikipedia Integration
    base_url = "https://en.wikipedia.org/wiki/"
    artist_url = base_url + clean_artist_name(selected_warner_artist)
    response = requests.get(artist_url)

    col1, col2 = st.columns([1, 2])

    with col1:
        if response.status_code == 200:
            st.markdown(f"[Visit {selected_warner_artist}'s Wikipedia Page]({artist_url})")
            image_url = get_artist_image(clean_artist_name(selected_warner_artist))
            if image_url:
                st.image(image_url, caption=f"{selected_warner_artist}", use_column_width=True)
            else:
                st.write("Image not found.")
        else:
            st.write(f"No Wikipedia page found for {selected_warner_artist}.")

    with col2:
        st.subheader(f"Information for {selected_warner_artist}:")
        st.write(f"**Track name:** {last_track['track_name']}")
        st.write(f"**Release Date:** {last_track['release_date'].strftime('%Y-%m-%d')}")
        st.write(f"**Popularity:** {last_track['popularity']}")
        st.write(f"**Followers:** {last_track['followers']}")

    # Select label for collaboration
    selected_label = st.selectbox(
        'Select a label for collaboration',
        options=['Select a label'] + list(other_labels),
        index=0
    )

    if selected_label == 'Select a label':
        st.warning("Please select a label before proceeding.")
    else:
        filtered_artists = filtred[filtred['record_label'] == selected_label]

        compatible_artists = filtered_artists[
            (filtered_artists['danceability'] >= warner_artist_data['danceability'].iloc[0] - 0.2) &
            (filtered_artists['danceability'] <= warner_artist_data['danceability'].iloc[0] + 0.2) &
            (filtered_artists['popularity'] >= warner_artist_data['popularity'].iloc[0] - 10) &
            (filtered_artists['popularity'] <= warner_artist_data['popularity'].iloc[0] + 10)
        ]

        if compatible_artists.empty:
            st.warning("No compatible artists found with the current filters.")
        else:
            # Display Top 10 Compatible Artists Table
            compatible_artists = compatible_artists.drop_duplicates(subset=['artist_name'])
            compatible_artists = compatible_artists.sort_values(by='popularity', ascending=False)
            compatible_artists_top_10 = compatible_artists.head(10)

            st.subheader("Top 10 Compatible Artists:")
            st.table(compatible_artists_top_10[['artist_name', 'popularity', 'followers']])

            # Radial Plot
            st.subheader(":bar_chart: Radial Comparison of Artist Features")
            categories = ['danceability', 'energy', 'valence', 'tempo_adjusted']

            # Ensure data columns exist
            if all(cat in warner_artist_data.columns for cat in categories) and all(cat in compatible_artists.columns for cat in categories):
                warner_values = [warner_artist_data[cat].mean() for cat in categories]
                compatible_values = [compatible_artists[cat].mean() for cat in categories]

                categories += [categories[0]]
                warner_values += [warner_values[0]]
                compatible_values += [compatible_values[0]]

                fig = go.Figure()

                fig.add_trace(go.Scatterpolar(
                    r=warner_values,
                    theta=categories,
                    fill='toself',
                    name=selected_warner_artist
                ))
                fig.add_trace(go.Scatterpolar(
                    r=compatible_values,
                    theta=categories,
                    fill='toself',
                    name="Top Compatible Artists"
                ))

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Required columns for the plot are missing in the dataset.")
