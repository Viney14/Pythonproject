import pandas as pd


labels = pd.read_csv('filtered_scrape.csv')
labels.head()
final_tracks = pd.read_csv('final_tracks.csv')
print(final_tracks)

import streamlit as st
st.title('Warner Music group')

import streamlit as st

# Title
st.title("Warner Artists")

# Dropdown options
options = [ 'Benson Boone', 
               'Burna Boy',
              'Charlie Puth',
          'Bailey Zimmerman',
             'David Guetta',
               'Anne-Marie',
                   'Ava Max',
    'A Boogie Wit da Hoodie',
               ' Charli xcx',
             'Cody Johnson',
                   'Cardi B',
                   'Eagles',
               'Bruno Mars',
               'Bebe Rexha',
                   'Madonna',
                   'Anitta',
     ' The Notorious B.I.G.']

# Dropdown selection
selected_option = st.selectbox("Choose an option:", options)

# Display the selected option
st.write(f"You selected: {selected_option}")


