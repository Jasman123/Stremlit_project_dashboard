import streamlit as st

pages = {
    "System Option": [
        st.Page("dashboard.py", title="Dashboard"),
        st.Page("app_input_data.py", title="Input your data")
        
    ]
}

pg = st.navigation(pages)
pg.run()