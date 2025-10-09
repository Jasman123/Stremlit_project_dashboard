import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ------------------------------
# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, limit=None, key="refresh")

st.set_page_config(
    page_title="Real-time Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Real-time Recording Data COB Line")

# ------------------------------
# Google Sheets CSV URL (must be CSV export)
SHEET_ID = "1oOJu04mdSgeGALFv9orv9LnvTf_HRBOlnLJVv4I07xc"
GID = "190517020"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)  # cache for 60 seconds
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

# ------------------------------
# Filter by TYPE
categories = list(df['TYPE'].unique())
categories.append("All")
selected_category = st.selectbox("Select Category", options=categories)

if selected_category == "All":
    filtered_df = df.copy()  
else:
    filtered_df = df[df['TYPE'] == selected_category]

# ------------------------------
# Create pivot table
pivot_1 = filtered_df.pivot_table(
    index='Time',
    columns='Station',
    values='OK',
    aggfunc='sum',
    fill_value=0
)

# Row-wise total
pivot_1['Total Production/Station'] = pivot_1.sum(axis=1)

# Column-wise total
pivot_1.loc['Total Product Station/Day'] = pivot_1.sum(numeric_only=True)

# ------------------------------
# Display DataFrame
st.subheader("Station Record Preview")
st.dataframe(pivot_1)

# ------------------------------
# Plotly bar chart
st.subheader("Production Station Pcs")
fig = px.bar(
    df,
    x="Time",
    y="OK",
    color="Station",
    barmode="group"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig)

# ------------------------------
# Top NG Line
st.subheader("Top NG Line")
group_1 = df.groupby('Station', as_index=False)['NG'].sum()
top5_NG = group_1.nlargest(5, 'NG')

fig2 = px.scatter(
    top5_NG,
    x="Station",
    y="NG",
    color="Station",
    size="NG",
    text="NG",
    title="Top 5 NG by Station"
)
fig2.update_traces(textposition="top center")
st.plotly_chart(fig2)
