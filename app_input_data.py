import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from datetime import date


SUB_CATEGORY = {
    "Die Bond": ["IC Bonding", "Pd/VC Bonding"],
    "Machine Only": ["Wire Bonding", "Wire Checking", "Lens Bonding", "Lens CCD Position Check"],
    "Dispensing": ["Module Dispensing", "UV Curing dispense", "U Lens", "Bake/Oven", "Dispensing Reverse"],
    "Function": ["Incoming Check", "Upload Program", "Divide Board", "Labeling", "BERT Test"],
    "Packing": ["Check Connector", "Packing"]
}

OPERATOR_LIST = [
    "Operator A",
    "Operator B",
    "Operator C",
    "Operator D",
    "Operator E",
    "Operator F",
    "Operator G",
    "Operator H"
]

SUPPLIER_LIST = [
    "Supplier X",
    "Supplier Y",
    "Supplier Z"
]

DATABASE_COLOUMNS = ['Date', 'Station Name', 'Model Type', 'OK Quantity', 'NG Quantity', 'Batch Number', 'Product Line']

CUSTOM_ORDER = [
    "Incoming Check",
    "Module Dispensing",
    "UV Curing dispense",
    "IC Bonding",
    "Pd/VC Bonding",
    "Wire Bonding",
    "Wire Checking",
    "Lens Bonding",
    "Lens CCD Position Check",
    "U Lens",
    "Bake/Oven",
    "Upload Program",
    "Divide Board",
    "Labeling",
    "BERT Test",
    "Dispensing Reverse",
    "Check Connector",
    "Packing"
]

CUSTOM_ORDER_TIME = [
    '10:00', '12:00', '15:00', '17:00',
    '20:00', '22:00', '00:00', '03:00', '05:00', '08:00'
]


st.set_page_config(
    page_title="COB Production Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

if "record_data" not in st.session_state:
    st.session_state.record_data = pd.DataFrame(
        columns=DATABASE_COLOUMNS
    )

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
        ["TX", "RX"],
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
# Action Section
# -----------------------------
st.divider()

col_btn1, col_btn2 = st.columns([1, 6])



with col_btn1:
    submit = st.button("💾 Save Record", use_container_width=True)

if submit:
    if not all([station_name, model_type, product_line]):
        st.warning("⚠️ Please complete all required fields.")
    else:
        new_record = {
        'Date': date.today().strftime("%Y-%m-%d"),
        'Station Name': station_name,
        'Model Type': model_type,
        'OK Quantity': ok_quantity,
        'NG Quantity': ng_quantity,
        'Batch Number': batch_number,
        'Product Line': product_line
    }

        st.session_state.record_data = pd.concat(
            [st.session_state.record_data, pd.DataFrame([new_record])],
            ignore_index=False
        )
        st.success("✅ Production data saved successfully!")

with st.container(height=500):
    st.subheader("📋 Production Records")
    st.dataframe(
        st.session_state.record_data,
        use_container_width=True,
        hide_index=True
    )


st.download_button(
    "⬇️ Download CSV",
    st.session_state.record_data.to_csv(index=False),
    "cob_production_records.csv",
    "text/csv"
)


st.divider()
st.subheader("🗑️ Delete Production Record")

col_d1, col_d2, col_d3, col_d4 = st.columns([1, 1.2, 2, 1])

with col_d1:
    del_batch = st.number_input("Batch Number", min_value=1, step=1)

with col_d2:
    del_time = st.selectbox("Production Time", CUSTOM_ORDER_TIME)

with col_d3:
    del_station = st.selectbox("Station Name", CUSTOM_ORDER)

with col_d4:
    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    delete_btn = st.button("🗑️ Delete", use_container_width=True)
    
if delete_btn:
    mask = ~(
        (st.session_state.record_data["Batch Number"] == del_batch)
        & (st.session_state.record_data["Production Time"] == del_time)
        & (st.session_state.record_data["Station Name"] == del_station)
    )

    st.session_state.record_data = st.session_state.record_data[mask]
    st.success("✅ Selected record deleted successfully.")