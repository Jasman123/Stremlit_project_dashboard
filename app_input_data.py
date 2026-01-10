from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
# from streamlit_autorefresh import st_autorefresh
from datetime import date
import os
from database_connect import (
    create_connection,
    insert_production_record,
    create_production_table
)

from data_info import (
    CUSTOM_ORDER, 
    CUSTOM_ORDER_TIME, 
    DATABASE_COLOUMNS,
    OPERATOR_LIST,
    SUPPLIER_LIST,
    MODULE_TYPE_LIST
)




st.set_page_config(
    page_title="COB Production Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_dotenv()

conn = create_connection(
    os.getenv("DB_NAME", "mydb"),
    os.getenv("DB_USER", "postgres"),
    os.getenv("DB_PASSWORD", "123"),
    os.getenv("DB_HOST", "localhost"),
    os.getenv("DB_PORT", "5432")
)

if conn:
    create_production_table(conn)
    record = pd.read_sql(
        "SELECT * FROM production_data;",
        conn
    )
else:
    st.error("❌ Database connection failed")
    record = pd.DataFrame(columns=DATABASE_COLOUMNS)


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div style="
    background-color:#0E4BF1;
    padding:18px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-size:28px;
    font-weight:600;
">
    COB Production Data Input
</div>
""", unsafe_allow_html=True)

st.write("")



# -----------------------------
st.subheader("Running Model Information")

col1, col2, col3, col4, col5, col6 = st.columns([2, 0.5, 0.5, 0.5, 1,1])

with col1:
    station_name = st.selectbox(
        "Station Name",
        CUSTOM_ORDER,
        index=None,
        placeholder="Select station",
        help="Select current manufacturing station"
    )

with col2:
    model_type = st.selectbox(
        "Model Type",
        MODULE_TYPE_LIST,
        index=None,
        placeholder="Select model",
        help="Product model type"
    )

with col3:
    batch_number = st.number_input(
        "Batch Number",
        min_value=1,
        step=1,
        value=1,
        format="%d",
        help="Production batch identifier"
    )

with col4:
   
    tray_number = st.number_input(
        "Tray Number",
        min_value=1,
        step=1,
        value=1,
        format="%d",
        help="Production tray identifier"
    )

with col5:
      product_line = st.selectbox(
        "Product Line",
        ["Indo #1", "Indo #2"],
        index=None,
        placeholder="Select line",
        help="Production line location"
    )
     
with col6:
     supplier = st.selectbox(
        "Supplier",
        SUPPLIER_LIST,
        index=None,
        placeholder="Select supplier",
        help="Supplier of the materials"
    )

#-----------------------------
st.subheader("Process Station information")

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
     ok_quantity = st.number_input(
        "OK Quantity",
        min_value=0,
        step=1,
        value=0,
        format="%d",
        help="Number of good units produced"
    )
     
with col2:
    ng_quantity = st.number_input(
        "NG Quantity",
        min_value=0,
        step=1,
        value=0,
        format="%d",
        help="Number of defective units"
    )

with col3:
    defect_type = st.text_input(
        "Remark Defect Type",
        value="",
        placeholder="Enter defect type",
        help="Type of defect observed"
    )

with col4:
    operator_select = st.selectbox(
        "Operator",
        OPERATOR_LIST,
        index=None,
        placeholder="Select operator",
        help="Operator responsible for production"
    )
# -----------------------------


col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 3])


with col_btn1:
    submit = st.button("💾 Save Record", use_container_width=True)

if submit:
    new_record = {
        "Station Name": station_name,
        "Model Type": model_type,
        "Batch Number": batch_number,
        "Tray Number": tray_number,
        "Product Line": product_line,
        "Supplier": supplier,
        "OK Quantity": ok_quantity,
        "NG Quantity": ng_quantity,
        "Operator Name": operator_select,
        "Remarks": defect_type
    }
    insert_production_record(conn, new_record)
    record = pd.read_sql(
        "SELECT * FROM production_data;",
        conn
    )

with col_btn2:
    st.success("✅ Record saved successfully!")

with st.container(height=500):
    st.subheader("📋 Production Records")
    st.dataframe(
        record,
        use_container_width=True,
        hide_index=True
    )

st.download_button(
    "⬇️ Download CSV",
    record.to_csv(index=False),
    "cob_production_records.csv",
    "text/csv"
)




