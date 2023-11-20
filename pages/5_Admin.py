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

    DivW = DivW.applymap(lambda x: re.sub(r'[^\x00-\x7F]+', '', str(x)) if isinstance(x, str) else x)
    DivW.columns = DivW.columns.map(lambda x: re.sub(r'[^\x00-\x7F]+', '', str(x)))
    DivW1 = DivW.copy()
    DivW = DivW.iloc[:, [3, 4, 6, 15, 18]]
    DivW = DivW.sort_values(by=[DivW.columns[2], DivW.columns[3], DivW.columns[4]],ascending=[False, True, True])
    DivW['Attend'] = None
    DivW.reset_index(inplace=True, drop=True)
    DivW.to_csv('attendance_list.csv', index=False)

    st.markdown("## For SAA")

    st.dataframe(DivW)

    with open("attendance_list.csv", "rb") as fp:
        btn = st.download_button(
            label="Obtain attendance list here",
            data=fp,
            file_name='attendance_list.csv'
        )

    st.markdown("## For Toastmaster")
    for i, col_name in enumerate(DivW1.columns):
        st.write(f"Column {i}: {col_name}")
    DivW1 = DivW1.iloc[:, [3, 12, 4, 18, 13]]
    DivW1 = DivW1.sort_values(by=[DivW1.columns[3]])
    DivW1.reset_index(inplace=True, drop=True)
    st.dataframe(DivW1)
    DivW1.to_csv('aia_list.csv', index=False)

    with open("aia_list.csv", "rb") as fp:
        btn = st.download_button(
            label="Obtain aia list here",
            data=fp,
            file_name='aia_list.csv'
        )


else:
    st.error('Wrong password. Please try again.')