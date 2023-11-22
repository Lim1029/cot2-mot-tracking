import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re

import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title="Registration_Tracking", page_icon="📊")
st.markdown("# Div W COT2 Breakout Room Assignment")

# pwd = st.text_input("Enter password to access the data", type="password")

conn = st.experimental_connection("gsheets2", type=GSheetsConnection)
df = conn.read()
DivW = df[df[df.columns[10]].str.startswith('Div W')]
DivW.reset_index(inplace=True,drop=True)
# Combine the selected columns into a single column
columns_to_combine = DivW.columns[18:25]
DivW['Club Name'] = DivW[columns_to_combine].apply(lambda row: ''.join(row.astype(str)), axis=1)
DivW['Club Name'] = DivW['Club Name'].str.replace('nan', '')
# Drop the original columns if needed
DivW = DivW.drop(columns=columns_to_combine)

DivWCO = DivW[DivW[DivW.columns[5]].str.startswith('Club Officer')]
DivWCO.reset_index(inplace=True,drop=True)

# st.dataframe(DivWCO)

import numpy as np

# Identify clubs with non-W origin
non_w_clubs = DivWCO[~DivWCO['Club Name'].str.startswith('W')]['Club Name'].unique()

# Among these clubs, identify those with 3 or more members
club_counts = DivWCO[DivWCO['Club Name'].isin(non_w_clubs)]['Club Name'].value_counts()
non_divw_clubs = club_counts[club_counts >= 3].index

# For the remaining clubs, randomly assign them to 'W1' to 'W5'
remaining_clubs = club_counts[club_counts < 3].index
areas = ['W1', 'W3', 'W4', 'W5']
# random_assignments = np.random.choice(areas, len(remaining_clubs))
# club_to_area = dict(zip(remaining_clubs, random_assignments))

import json

# Check if the club_to_area.json file exists
try:
    with open('club_to_area.json', 'r') as f:
        club_to_area = json.load(f)
except FileNotFoundError:
    # If the file does not exist, generate the club_to_area dictionary and save it to a file
    random_assignments = np.random.choice(areas, len(remaining_clubs))
    club_to_area = dict(zip(remaining_clubs, random_assignments))
    with open('club_to_area.json', 'w') as f:
        json.dump(club_to_area, f)

# The rest of the code remains the same
def get_area(club_name):
    area = club_name[:2]
    if area in ['W1', 'W2', 'W3', 'W4', 'W5']:
        return area
    elif club_name in non_divw_clubs:
        return 'Non-DivW'
    elif club_name in club_to_area:
        return club_to_area[club_name]
    else:
        return 'Non-DivW'

def get_area(club_name):
    area = club_name[:2]
    if area in ['W1', 'W2', 'W3', 'W4', 'W5']:
        return area
    else:
        return 'Non-DivW'

DivWCO['Area'] = DivWCO['Club Name'].apply(get_area)
groups = DivWCO.groupby('Area')
counts = DivWCO['Area'].value_counts().rename_axis('Area').reset_index(name='Counts')
st.markdown("## Participant Counts by Room (Only CO)")
st.dataframe(counts)
# st.dataframe(DivWCO['Area'].value_counts())
columns = DivWCO.columns

# Iterate over the groups
for name, group in groups:
    # Select the columns to display
    display_columns = group[[columns[2], 'Club Name']]
    # Rename the columns
    display_columns.columns = ['Name', 'Club Name']
    display_columns.reset_index(inplace=True,drop=True)
    # Display the group
    st.markdown(f"## Room {name}: {len(group)} participants")
    st.dataframe(display_columns) 