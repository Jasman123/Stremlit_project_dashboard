import streamlit as st
import pandas as pd
from datetime import date
from sqlalchemy import text
from db import engine

st.set_page_config(
    page_title="Production Dashboard",
    layout="wide"
)

# -------------------------
# HEADER
# -------------------------
st.title("📊 Production Dashboard (Supabase + PostgreSQL)")

# -------------------------
# FORM INPUT
# -------------------------
st.subheader("➕ Input Production Data")

with st.form("production_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        production_date = st.date_input("Date", value=date.today())
        station_name = st.text_input("Station Name")
        model_type = st.text_input("Model Type")

    with col2:
        ok_qty = st.number_input("OK Quantity", min_value=0, step=1)
        ng_qty = st.number_input("NG Quantity", min_value=0, step=1)
        production_time = st.number_input(
            "Production Time (Minutes)", min_value=0, step=1
        )

    with col3:
        batch_number = st.text_input("Batch Number")
        product_line = st.text_input("Product Line")

    submitted = st.form_submit_button("💾 Save Data")

    if submitted:
        if not station_name or not model_type:
            st.error("Station Name and Model Type are required!")
        else:
            query = text("""
                INSERT INTO production_dashboard
                (production_date, station_name, model_type,
                 ok_quantity, ng_quantity, production_time_min,
                 batch_number, product_line)
                VALUES
                (:date, :station, :model, :ok, :ng, :ptime, :batch, :line)
            """)

            with engine.begin() as conn:
                conn.execute(
                    query,
                    {
                        "date": production_date,
                        "station": station_name,
                        "model": model_type,
                        "ok": ok_qty,
                        "ng": ng_qty,
                        "ptime": production_time,
                        "batch": batch_number,
                        "line": product_line
                    }
                )

            st.success("✅ Data successfully saved!")

# -------------------------
# LOAD DATA
# -------------------------
st.divider()
st.subheader("📋 Production Data")

df = pd.read_sql(
    "SELECT * FROM production_dashboard ORDER BY production_date DESC",
    engine
)

if not df.empty:
    df = df.rename(columns={
        "production_date": "Date",
        "station_name": "Station Name",
        "model_type": "Model Type",
        "ok_quantity": "OK Quantity",
        "ng_quantity": "NG Quantity",
        "production_time_min": "Production Time",
        "batch_number": "Batch Number",
        "product_line": "Product Line"
    })

    st.dataframe(df, use_container_width=True)

    # -------------------------
    # KPI METRICS
    # -------------------------
    st.subheader("📈 KPI Summary")

    total_ok = df["OK Quantity"].sum()
    total_ng = df["NG Quantity"].sum()
    total_prod = total_ok + total_ng

    col1, col2, col3 = st.columns(3)
    col1.metric("Total OK", total_ok)
    col2.metric("Total NG", total_ng)
    col3.metric(
        "Yield (%)",
        f"{(total_ok / total_prod * 100):.2f} %" if total_prod > 0 else "0 %"
    )

else:
    st.info("No data available yet.")

# -------------------------
# FOOTER
# -------------------------
st.caption("🚀 Powered by Streamlit + Supabase PostgreSQL")
