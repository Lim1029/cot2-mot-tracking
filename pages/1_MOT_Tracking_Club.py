import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title="MOT_Tracking_For_Club", page_icon="📊")
st.markdown("# MOT Tracking For Club")
st.sidebar.header("MOT Tracking For Club")

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
df = conn.read()

option = st.selectbox(
    'Choose a club to see who has submitted MOT (Missing option means zero submission for the particular club.)',
    df['Your Club Name:'].unique())

name_list = df[df['Your Club Name:']==option]
st.write(name_list['Name'])
filename = f'{option}_MOT_results.csv'
name_list.to_csv(filename)
# st.button("Obtain your club's survey result here", type="primary" on_click=)
with open(filename, "rb") as fp:
    btn = st.download_button(
        label="Obtain your club's survey result here",
        data=fp,
        file_name=filename
    )
# st.write("Obtain your club's survey result here: *Coming Soon*")