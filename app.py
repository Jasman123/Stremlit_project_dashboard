import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

# Replace with the path to your downloaded JSON key
creds = ServiceAccountCredentials.from_json_keyfile_name(".venv/nth-canto-468405-c8-552f3d3718ae.json", scope)
client = gspread.authorize(creds)


# Replace with your Google Sheet name
sheet = client.open("HourlyLineRecord").worksheet("DataBase Try")

# Load data into pandas DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

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
    index='Time',        # rows
    columns='Station',   # columns
    values='OK',         # values to aggregate
    aggfunc='sum',       # sum OK values
    fill_value=0         # fill missing values with 0
)

# Add row-wise total: Total Production per station
pivot_1['Total Production/Station'] = pivot_1.sum(axis=1)

# Add column-wise total: Total Product station per day
pivot_1.loc['Total Product Station/Day'] = pivot_1.sum(numeric_only=True)
# ------------------------------
# Display DataFrame
st.subheader("Station Record Preview")
st.dataframe(pivot_1)

# ------------------------------
# Plotly chart
# Replace 'Date' and 'Value' with your actual column names
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

st.subheader("Top NG Line")
group_1 = df.groupby('Station', as_index=False)['NG'].sum()
top5_NG = group_1.nlargest(5, 'NG')
fig = px.scatter(
    top5_NG,
    x="Station",
    y="NG",
    color="Station",
    size="NG",  # optional: size bubbles by NG
    text="NG",  # show NG values on points
    title="Top 5 NG by Station"
)

fig.update_traces(textposition="top center")
st.plotly_chart(fig)