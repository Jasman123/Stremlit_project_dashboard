import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

def bar_plot (df, x_axis, y_axis, color, title):
    fig = px.bar(
    df,
    x=x_axis,
    y=y_axis,
    color=color,
    barmode="group",
    text_auto=True,  
    title= title,
    custom_data=[df[color]] 
)
    
    fig.update_traces(
    hovertemplate=(
            "<b>Station:</b> %{customdata[0]}"
            "<br><b>Time:</b> %{x}"
            "<br><b>OK:</b> %{y}"
            "<extra></extra>"
        ),
    marker_line_width=1.2,
    marker_line_color="white",
)
    fig.update_layout(
        legend=dict(
            title="Station",
            font=dict(size=25),
            itemsizing="trace",  
            itemwidth=60,
        ),
        title_font=dict(size=18),
        xaxis_title_font=dict(size=16),
        yaxis_title_font=dict(size=16),
     
)
    return fig

def scatter_plot(df, x_axis, y_axis, color, title):
    fig = px.scatter(
    df,
    x=x_axis,
    y=y_axis,
    color=color,
    size=y_axis,
    text=y_axis,
    title=title
)

    fig.update_traces(
    textposition="top center",
    textfont=dict(size=14, color="#333", family="Arial Black"),
    marker=dict(
        line=dict(width=2, color="white"),
        opacity=0.9
    ),
    hovertemplate="<b>Station:</b> %{x}<br><b>NG Count:</b> %{y}<extra></extra>"

)
    return fig

st.set_page_config(
    page_title="Real-time Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------
# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, limit=None, key="refresh")

# ------------------------------
# Google Sheets CSV URL (must be CSV export)
# region Reading add google sheet verificarion
SHEET_ID = "1oOJu04mdSgeGALFv9orv9LnvTf_HRBOlnLJVv4I07xc"
GID = "190517020"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)  # cache for 60 seconds
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()
df["DateTime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce")

# endregion

st.markdown("""
    <div style="
        background-color:#0078FF;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 30px;
        font-weight: bold;
        letter-spacing: 1px;
    ">
        🏭 COB Line Real-Time Production Dashboard
    </div>
""", unsafe_allow_html=True
)

# ------------------------------
# Filter by TYPE
# region filterring data
st.markdown("---")  # horizontal line separator

col1, col2,col3, col4, col5 = st.columns([1, 1, 1, 1,0.5])

with col1:
    st.markdown(
        "<h4 style='color:#2C3E50; margin-top:24px;'>🔍 Select Category:</h4>",
        unsafe_allow_html=True
    )

with col2:
    categories_1 = ["All"] + sorted(df['TYPE'].dropna().unique().tolist())
    selected_category_1 = st.selectbox(
        "Type Module",
        options=categories_1,
        index=0,
        key="category_filter_1"
    )

with col3:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    categories_2 = ["All"] + sorted(
        df['Date'].dropna().dt.strftime('%Y-%m-%d').unique().tolist()
    )
    selected_category_2 = st.selectbox(
        "Star Date",
        options=categories_2,
        index=0,
        key="category_filter_2"
    )

with col4:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    categories_3 = ["All"] + sorted(
        df['Date'].dropna().dt.strftime('%Y-%m-%d').unique().tolist()
    )
    selected_category_3 = st.selectbox(
        "End Date",
        options=categories_3,
        index=0,
        key="category_filter_3"
    )

with col5:
    st.markdown(
        f"""
        <div style='
            background-color:#eef6ff;
            border-left:5px solid #0078ff;
            padding:8px 14px;
            border-radius:8px;
            font-size:15px;
            color:#2C3E50;
            margin-top:28px;
        '>
            📦 Showing: <b>{selected_category_1}</b><br>
            📅 From <b>{selected_category_2}</b> to <b>{selected_category_3}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

filtered_df = df.copy()

if selected_category_1 != "All":
    filtered_df = filtered_df[filtered_df['TYPE'] == selected_category_1]

# Filter by DATE
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], errors='coerce')

# Filter by Date Range
if selected_category_2 != "All" and selected_category_3 != "All":
    start_date = pd.to_datetime(selected_category_2)
    end_date = pd.to_datetime(selected_category_3)
    filtered_df = filtered_df[
        (filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)
    ]
# endregion

# ------------------------------
# Create pivot table
pivot_1 = filtered_df.pivot_table(
    index='Time',
    columns='Station',
    values='OK',
    aggfunc='sum',
    fill_value=0
)
pivot_1['Total per Time'] = pivot_1.sum(axis=1)
pivot_1.loc['Grand Total'] = pivot_1.sum(numeric_only=True)
pivot_1 = pivot_1.applymap(lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)


# ------------------------------
# Display DataFrame
st.subheader("📋 Station Record Summary")
st.dataframe(
    pivot_1,
    use_container_width=True,
    hide_index=False
)


# ------------------------------
# Plotly bar chart
st.subheader("Production Station Pcs")
st.plotly_chart(bar_plot(filtered_df,"DateTime","OK","Station","Ouput Production Daily"))

# ------------------------------
# Top NG Line
st.subheader("🚨 Top 5 NG Line")
group_1 = df.groupby('Station', as_index=False)['NG'].sum()
top5_NG = group_1.nlargest(5, 'NG')

st.plotly_chart(scatter_plot(top5_NG, "Station", "NG","Station","Top 5 NG by Station")
, use_container_width=True)

