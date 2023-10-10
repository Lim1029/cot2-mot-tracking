import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
def run():
    st.set_page_config(
        page_title="MOT Tracking (AD)"
    )
    st.sidebar.header("MOT Tracking For Division")
    st.markdown("# COT2 MOT Tracking")
    st.write("Data obtained from TI Dashboard")
    st.write("Only available when MOT is submitted using this link: https://docs.google.com/forms/d/19n9MhbIZ0kmD-9sI1XBAnSlXKF1tox6LozP6akpLRG0/edit")
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)

    df = conn.read()

    # #add area details, if area is available in gform this is not needed.
    df_dashboard = pd.read_csv('https://dashboards.toastmasters.org/export.aspx?type=CSV&report=districtperformance~51~9/30/2023~~2023-2024')
    # merged_df = df.merge(df_dashboard[['Club Name', 'Area']], left_on='Your Club Name:', right_on='Club Name', how='left')

    # # Drop the duplicate "Club Name" column
    # merged_df.drop('Club Name', axis=1, inplace=True)

    # Print results.
    all_divW = df_dashboard[df_dashboard['Division']=='W'][['Area','Club Name','Oct. Ren.']]
    all_divW['MOT submitted'] = all_divW['Club Name'].apply(lambda x: df['Your Club Name:'].eq(x).sum() if x != 'Club Name' else 0)
    all_divW = all_divW.rename(columns={'Oct. Ren.': 'Total Member'})
    st.write(all_divW)

if __name__ == "__main__":
    run()
