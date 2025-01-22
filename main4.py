import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np

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

# Streamlit UI
st.title(':notes: Warner Music Group Collaboration Tool')

# 1. Select a Warner Music Group artist with placeholder (default message)
selected_warner_artist = st.selectbox(
    'Select an artist from Warner Music Group',
    options=['Select an artist'] + list(artist_names),  # Placeholder
    index=0  # Default selection
)

# Ensure an artist is selected before proceeding
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
            st.write(f"**Release Date:** {last_track['release_date']}")
            st.write(f"**Popularity:** {last_track['popularity']}")
            st.write(f"**Followers:** {last_track['followers']}")


        
       
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
        else:
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

                # Plot radial chart for both artists
                st.subheader(":bar_chart: Radial Comparison of Artist Features")
                
                categories = ['danceability', 'energy', 'valence', 'tempo_adjusted']

                # Ensure Warner artist's data is correctly extracted
                if not warner_artist_data.empty:
                    warner_values = [
                        warner_artist_data.iloc[0][cat] for cat in categories
                    ]
                else:
                    st.error("Failed to retrieve data for the selected Warner Music Group artist.")
                    warner_values = [0] * len(categories)

                # Ensure Compatible artist's data is correctly extracted
                if not compatible_artist_data.empty:
                    compatible_values = [
                        last_compatible_track[cat] for cat in categories
                    ]
                else:
                    st.error("Failed to retrieve data for the selected compatible artist.")
                    compatible_values = [0] * len(categories)

                # Normalize data using global maximums for each category
                max_values_global = [
                    max(df[cat].max(), 1) for cat in categories
                ]

                warner_normalized = [warner_values[i] / max_values_global[i] for i in range(len(categories))]
                compatible_normalized = [compatible_values[i] / max_values_global[i] for i in range(len(categories))]

                # Create radar chart
                angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
                warner_normalized += warner_normalized[:1]
                compatible_normalized += compatible_normalized[:1]
                angles += angles[:1]

                fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'polar': True})

                ax.fill(angles, warner_normalized, color='blue', alpha=0.25, label=selected_warner_artist)
                ax.plot(angles, warner_normalized, color='blue', linewidth=2)

                ax.fill(angles, compatible_normalized, color='red', alpha=0.25, label=selected_compatible_artist)
                ax.plot(angles, compatible_normalized, color='red', linewidth=2)

                ax.set_yticks([])
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(categories)
                ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

                st.pyplot(fig)
