import altair as alt
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re

import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title="Registration_Tracking", page_icon="📊")
st.markdown("# Registration Tracking for OC")

pwd = st.text_input("Enter password to access the data", type="password")

if pwd == 'DivWCOT2':

    conn = st.experimental_connection("gsheets2", type=GSheetsConnection)
    df = conn.read()
    DivW = df[df[df.columns[10]].str.startswith('Div W')]
    DivW.reset_index(inplace=True)
    # Combine the selected columns into a single column
    columns_to_combine = DivW.columns[18:25]
    DivW['Club Name'] = DivW[columns_to_combine].apply(lambda row: ''.join(row.astype(str)), axis=1)
    DivW['Club Name'] = DivW['Club Name'].str.replace('nan', '')
    # Drop the original columns if needed
    DivW = DivW.drop(columns=columns_to_combine)
    # for i, col_name in enumerate(DivW.columns):
        # st.write(f"Column {i}: {col_name}")
    DivW = DivW.iloc[:, [3, 4, 6, 15, 18]]
    DivW = DivW.sort_values(by=[DivW.columns[2], DivW.columns[3], DivW.columns[4]],ascending=[False, True, True])
    DivW = DivW.applymap(lambda x: re.sub(r'[^\x00-\x7F]+', '', str(x)) if isinstance(x, str) else x)
    DivW.columns = DivW.columns.map(lambda x: re.sub(r'[^\x00-\x7F]+', '', str(x)))
    DivW = DivW.sort_values(by=[DivW.columns[2], DivW.columns[3], DivW.columns[4]])
    DivW['Attend'] = None
    DivW.reset_index(inplace=True, drop=True)
    DivW.to_csv('attendance_list.csv', index=False)

    st.dataframe(DivW)

    with open("attendance_list.csv", "rb") as fp:
        btn = st.download_button(
            label="Obtain attendance list here",
            data=fp,
            file_name='attendance_list.csv'
        )

else:
    st.error('Wrong password. Please try again.')