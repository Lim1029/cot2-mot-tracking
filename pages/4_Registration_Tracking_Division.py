import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title="Registration_Tracking", page_icon="📊")
st.markdown("# Registration Tracking for OC")

conn = st.experimental_connection("gsheets2", type=GSheetsConnection)
df = conn.read()
DivW = df[df[df.columns[10]].str.startswith('Div W')]
DivW.reset_index(inplace=True)
# st.write(DivW)
# st.write(DivW.columns)

#remove non club officer

# Combine the selected columns into a single column
columns_to_combine = DivW.columns[18:25]
DivW['Total Counts'] = DivW[columns_to_combine].apply(lambda row: ''.join(row.astype(str)), axis=1)
DivW['Total Counts'] = DivW['Total Counts'].str.replace('nan', '')
# Drop the original columns if needed
DivW = DivW.drop(columns=columns_to_combine)

st.write("DivW COT2 Registration for Club Officers")
DivW_CO = DivW[DivW[DivW.columns[6]]=='Club Officer 分会执委']
st.write(DivW_CO[DivW_CO.columns[3]])


st.write("DivW COT2 Registration for NON Club Officers")
DivW_NCO = DivW[~(DivW[DivW.columns[6]]=='Club Officer 分会执委')]
st.write(DivW_NCO[DivW_NCO.columns[3]])

st.write("Attendees meal option")

meal_counts = DivW[DivW.columns[5]].value_counts()
origin_counts = DivW['Total Counts'].value_counts()
st.write(meal_counts)

st.write("Participants by Club")

st.write(origin_counts)

# name_list = df[df['Your Club Name:']==option]
# st.write(name_list['Name'])
# st.write("Obtain your club's survey result here: *Coming Soon*")