import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from datetime import date 
import os
from dotenv import load_dotenv
from database_connect import (
    create_connection,
    insert_production_record,
    create_production_table,
    delete_production_record
)


from data_info import (
    CUSTOM_ORDER,  
    CUSTOM_ORDER_TIME,
    DATABASE_COLOUMNS,
    OPERATOR_LIST,
    SUPPLIER_LIST,
    MODULE_TYPE_LIST,
    SUB_CATEGORY
)

conn = create_connection(
    os.getenv("DB_NAME", "mydb"),
    os.getenv("DB_USER", "postgres"),
    os.getenv("DB_PASSWORD", "123"),
    os.getenv("DB_HOST", "localhost"),
    os.getenv("DB_PORT", "5432")
)


def bar_plot (df, x_axis, y_axis, color, title, CUSTOM_ORDER=None):
    if CUSTOM_ORDER and color in df.columns:
        df[color] = pd.Categorical(df[color], categories=CUSTOM_ORDER, ordered=True)
        df = df.sort_values(by=color)
        

    fig = px.bar(
        df,
        x=x_axis,
        y=y_axis,
        color=color,
        barmode="group",
        text_auto=True,
        title=title,
        custom_data=[df[color]],
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

def scatter_plot(df, x_axis, y_axis, color, symbol, title):
    fig = px.scatter(
    df,
    x=x_axis,
    y=y_axis,
    color=color,
    symbol=symbol,
    size=y_axis,
    text=y_axis,
    title=title,

    symbol_map={
            "RX": "circle",
            "TX": "diamond"
        },
        category_orders={
            symbol: ["RX", "TX"]
        }
    
    )

    for trace in fig.data:
        trace_symbol = trace.name.split(",")[-1].strip() 
        trace.customdata = [[trace_symbol]] * len(trace.x)  

    fig.update_traces(
        textposition="top center",
        textfont=dict(size=14, color="#333", family="Arial Black"),
        marker=dict(line=dict(width=2, color="white"), opacity=0.9),
        hovertemplate="<b>Station:</b> %{x}<br><b>Type:</b> %{customdata[0]}<br><b>NG Count:</b> %{y}<extra></extra>"
    )

    fig.update_yaxes(range=[0, df[y_axis].max() * 1.3])

    

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title=dict(x=0.5),
        font=dict(family="Arial", size=13),
        legend_title=f"{color} / {symbol}"
    )


    return fig

st.set_page_config(
    page_title="Real-time Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def make_card(title, value, subtitle, color="#27AE60"):
    st.markdown(f"""
    <div style="
        background-color: #ffffff;
        border-left: 8px solid {color};
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    ">
        <h4 style="color:#2C3E50;">{title}</h4>
        <h2 style="color:{color}; margin:0;">{value}</h2>
        <p style="color:gray;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

st_autorefresh(interval=30000, limit=None, key="refresh")



@st.cache_data(ttl=60)  # cache for 60 seconds
def load_data():
    if conn:
        create_production_table(conn)
        df = pd.read_sql(
            "SELECT * FROM production_data;",
            conn
        )
        return df
    return pd.DataFrame()


df = load_data()
# st.write(df.columns)

df['production_date'] = pd.to_datetime(df['production_date'])
df['model_type'] = df['model_type'].astype(str)
df['batch_number'] = df['batch_number'].astype(str)
batchs_available = ["All"] + df['batch_number'].unique().tolist()

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

st.markdown("---")  # horizontal line separator

filtered_df = df.copy()

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 0.5])

with col1:
    st.markdown(
        "<h4 style='color:#2C3E50; margin-top:24px;'>🔍 Select Category:</h4>",
        unsafe_allow_html=True
    )

with col2:
    categories_1 = ["All"] + sorted(df['model_type'].dropna().unique().tolist())
    selected_category_1 = st.selectbox(
        "Type Module",
        options=categories_1,
        index=0,
        key="category_filter_1"
    )

    if selected_category_1 != "All":
        filtered_df = filtered_df[filtered_df['model_type'] == selected_category_1]

with col3:
    selected_category_2 = st.date_input(
        "Start Date",
        value=date.today(),
        key="category_filter_2"
    )

with col4:
    selected_category_3 = st.date_input(
        "End Date",
        value=date.today(),
        key="category_filter_3"
    )

    # ✅ Apply date filtering (no "All" string check)
    start_date = pd.to_datetime(selected_category_2)
    end_date = pd.to_datetime(selected_category_3)
    filtered_df = filtered_df[
        (filtered_df['production_date'] >= start_date) &
        (filtered_df['production_date'] <= end_date)
    ]

with col5:
    selected_category_4 = st.selectbox(
        "Batch",
        options=batchs_available,
        index=0,
        key="category_filter_4"
    )

    if selected_category_4 != "All":
        filtered_df = filtered_df[filtered_df['batch_number'] == selected_category_4]

with col6:
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


pivot_df = filtered_df.copy()
pivot_df.drop(columns=['id', 'production_date'], inplace=True)


with st.container(height=500):
    st.subheader("📋 Production Records")
    st.dataframe(
        pivot_df,
        use_container_width=True,
        hide_index=False
    )





