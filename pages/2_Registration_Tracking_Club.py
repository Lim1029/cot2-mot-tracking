import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title="Registration_Tracking_For_Club", page_icon="📊")
st.markdown("# Registration Tracking For Club")
st.sidebar.header("Registration Tracking For Club")

conn = st.experimental_connection("gsheets2", type=GSheetsConnection)
df = conn.read()

# Combine the selected columns into a single column
columns_to_combine = df.columns[18:25]
df['Total Counts'] = df[columns_to_combine].apply(lambda row: ''.join(row.astype(str)), axis=1)
df['Total Counts'] = df['Total Counts'].str.replace('nan', '')
# Drop the original columns if needed
df = df.drop(columns=columns_to_combine)
columns = df.columns
option = st.selectbox(
    'Choose a club to see who has registered (Missing option means zero submission for the particular club.)',
    df[columns[18]].unique())

name_list = df[df[columns[18]]==option]
st.write(name_list[[columns[2],columns[6],columns[10]]])
# st.write("Obtain your club's registration result here: *Coming Soon*")