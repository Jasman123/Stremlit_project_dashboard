import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv(r"C:\Users\OFFICE-COB\Documents\COB Engineer\python Project\HourlyLineRecord - DataBase Try.csv")


# Streamlit app layout
st.title(f"📊 Hourly Line Record Dashboard {df['Date'].iloc[0]}")
st.write("Visualizing production data from your CSV file")

pivot_1 = pd.pivot_table(
    df,
    columns='Station',
    index='Time',
    values='OK',
    aggfunc='sum',
    fill_value=0
)
pivot_1['Total Production/ station'] = pivot_1.sum(axis=1)
pivot_1.loc['Total Product station/Day'] = pivot_1.sum(numeric_only=True)


# Show first few rows
st.subheader("Preview of Data")
st.dataframe(pivot_1)

# Boxplot using Plotly
st.subheader("Boxplot of OK Values")
fig = px.box(df, y='OK', title='Distribution of OK Values')
st.plotly_chart(fig)
