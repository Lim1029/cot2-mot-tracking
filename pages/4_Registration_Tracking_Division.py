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

Non_DivW = df[~df[df.columns[10]].str.startswith('Div W')]
Non_DivW.reset_index(inplace=True)
# st.write(Non_DivW)
# st.write(DivW.columns)

#remove non club officer

# Combine the selected columns into a single column
columns_to_combine = DivW.columns[18:25]
DivW['Total Counts'] = DivW[columns_to_combine].apply(lambda row: ''.join(row.astype(str)), axis=1)
DivW['Total Counts'] = DivW['Total Counts'].str.replace('nan', '')
# Drop the original columns if needed
DivW = DivW.drop(columns=columns_to_combine)

Non_DivW['Total Counts'] = Non_DivW[columns_to_combine].apply(lambda row: ''.join(row.astype(str)), axis=1)
Non_DivW['Total Counts'] = Non_DivW['Total Counts'].str.replace('nan', '')
# Drop the original columns if needed
Non_DivW = Non_DivW.drop(columns=columns_to_combine)

st.write("DivW COT2 Registration for Club Officers")
DivW_CO = DivW[DivW[DivW.columns[6]]=='Club Officer 分会执委']
st.write(DivW_CO[DivW_CO.columns[3]])


st.write("DivW COT2 Registration for NON Club Officers")
DivW_NCO = DivW[~(DivW[DivW.columns[6]]=='Club Officer 分会执委')]
st.write(DivW_NCO[DivW_NCO.columns[3]])

st.write("Attendees meal option")

meal_counts = DivW[DivW.columns[5]].value_counts()
origin_counts = DivW['Total Counts'].value_counts()
origin_non_divW_counts = Non_DivW['Total Counts'].value_counts()
st.write(meal_counts)

st.write("Participants by Division")
# st.dataframe(DivW)
st.dataframe(DivW[DivW.columns[15]].value_counts())
DivW['Area'] = DivW[DivW.columns[18]].str[:2]
st.write("Participants by Area")
st.dataframe(DivW['Area'].value_counts())

st.write("Participants by Role")
st.dataframe(DivW[DivW.columns[6]].value_counts())

st.write("Participants by Officer Role")
st.dataframe(DivW[DivW.columns[7]].value_counts())

origin_counts = origin_counts.to_frame()
origin_non_divW_counts = origin_non_divW_counts.to_frame()
st.write("Participants by Club")


club_count = origin_counts.merge(origin_non_divW_counts, how='outer', left_index=True, right_index=True)
club_count = club_count.rename(columns={'Total Counts_x': 'Div W'})
club_count = club_count.rename(columns={'Total Counts_y': 'Other Div'})

st.write(club_count)
# st.write(type(origin_counts))
# name_list = df[df['Your Club Name:']==option]
# st.write(name_list['Name'])
# st.write("Obtain your club's survey result here: *Coming Soon*")