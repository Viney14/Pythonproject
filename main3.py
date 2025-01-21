import streamlit as st
import pandas as pd

#@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

file_path = r"C:\Users\tober\Documents\HYper\git2\warner_new.csv"  #assign path

# Load the data
data = load_data("warner_new.csv")

# Title
st.title("Warner Music Group")
st.subheader('Our Artists')

# Dropdown options based on artist names in the CSV
options = data['artist_name'].unique()  

# Dropdown selection
selected_artist = st.selectbox("Select an artist:", options)

# Display data for the selected artist
if selected_artist:
    artist_data = data[data['artist_name'] == selected_artist]  # Filter data for the selected artist
    st.subheader(f"Details for {selected_artist}")
    st.write(artist_data)  # Display the filtered data