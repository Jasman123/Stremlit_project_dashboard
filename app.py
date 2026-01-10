import streamlit as st

pages = {
    "System Option": [
        st.Page("dashboard_1.py", title="Dashboard"),
        st.Page("app_input_data.py", title="Input your data")
        
    ]
}

pg = st.navigation(pages)
pg.run()