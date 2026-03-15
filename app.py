import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px
from lifetimes import BetaGeoFitter

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Customer Insights Engine", layout="wide")

# --- 1. SIDEBAR / USER GUIDE ---
with st.sidebar:
    st.header("🎯 RFM Analytics Guide")
    st.markdown("""
    **What is RFM?**
    - **Recency:** Days since last order.
    - **Frequency:** Total number of orders.
    - **Monetary:** Total revenue from customer.

    **The Prediction Logic:**
    We use the **BG/NBD Model** to estimate the 
    *Probability of Being Alive* (P-Alive). If a 
    frequent buyer stops suddenly, their 
    P-Alive score drops.
    """)
    st.divider()
    st.info("Upload your CSV to begin.")

# --- 2. DATA VALIDATOR FUNCTION ---
def validate_and_clean(df):
    logs = []
    required_cols = ['CustomerID', 'TransactionDate', 'TransactionAmount']
    
    # Check columns
    if not all(col in df.columns for col in required_cols):
        st.error(f"Required columns missing. Please ensure your CSV has: {required_cols}")
        return None, None

    # Cleaning
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], errors='coerce')
    original_count = len(df)
    df = df.dropna(subset=['TransactionDate', 'CustomerID'])
    df = df[df['TransactionAmount'] > 0]
    
    if len(df) < original_count:
        logs.append(f"⚠️ Removed {original_count - len(df)} rows with invalid dates, IDs, or $0 amounts.")
    
    return df, logs

# --- 3. MAIN INTERFACE ---
st.title("🚀 Customer Segmentation & Predictive Engine")

uploaded_file = st.file_uploader("Upload Transactional Data (CSV)", type="csv")

if uploaded_file:
    raw_data = pd.read_csv(uploaded_file)
    df, cleaning_logs = validate_and_clean(raw_data)

    if df is not None:
        if cleaning_logs:
            with st.expander("🛠️ Data Cleaning Report"):
                for log in cleaning_logs:
                    st.write(log)

        # --- RFM CALCULATION ---
        snapshot_date = df['TransactionDate'].max() + dt.timedelta(days=1)
        
        # Aggregating for RFM + T (Age of customer for predictive model)
        rfm = df.groupby('CustomerID').agg({
            'TransactionDate': [
                lambda x: (x.max() - x.min()).days, # Recency (for model: duration between first/last)
                lambda x: (snapshot_date - x.min()).days, # T (Age)
                lambda x: (snapshot_date - x.max()).days  # Actual Recency (Days since last)
            ],
            'CustomerID': 'count',
            'TransactionAmount': 'sum'
        })

        # Rename columns
        rfm.columns = ['Model_Recency', 'T', 'Recency_Days', 'Frequency', 'Monetary']
        rfm = rfm.reset_index()

        # Simple Scoring (1-5)
        rfm['R_Score'] = pd.qcut(rfm['Recency_Days'], 5, labels=[5, 4, 3, 2, 1])
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
        
        # Segment Assignment
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str)
        seg_map = {
            r'[1-2][1-2]': 'Hibernating',
            r'[1-2][3-4]': 'At Risk',
            r'3[1-3]': 'Needs Attention',
            r'[4-5][4-5]': 'Champions',
            r'[4-5][1-3]': 'Promising'
        }
        rfm['Segment'] = rfm['RFM_Score'].replace(seg_map, regex=True)

        # --- PREDICTIVE MODELING (BG/NBD) ---
        try:
            bgf = BetaGeoFitter(penalizer_coef=0.01)
            # Lifetimes model uses 'Frequency' as 'Repeat Purchases' (Total - 1)
            bgf.fit(rfm['Frequency'] - 1, rfm['Model_Recency'], rfm['T'])
            rfm['P_Alive'] = bgf.conditional_probability_alive(rfm['Frequency']-1, rfm['Model_Recency'], rfm['T'])
        except:
            rfm['P_Alive'] = "N/A"

        # --- DASHBOARD VISUALS ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Customers", len(rfm))
        col2.metric("Total Revenue", f"${rfm['Monetary'].sum():,.0f}")
        col3.metric("Avg. P(Alive)", f"{rfm['P_Alive'].mean()*100:.1f}%" if isinstance(rfm['P_Alive'].mean(), float) else "N/A")

        st.subheader("Customer Segments by Value")
        fig = px.treemap(rfm, path=['Segment'], values='Monetary', color='Segment',
                         color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig, use_container_width=True)

        # --- EXPORT SECTION ---
        st.divider()
        st.subheader("📥 Export Actionable Lists")
        target_seg = st.selectbox("Select Segment to Download:", rfm['Segment'].unique())
        
        subset = rfm[rfm['Segment'] == target_seg][['CustomerID', 'Recency_Days', 'Frequency', 'Monetary', 'P_Alive']]
        
        st.dataframe(subset.head(10), use_container_width=True)
        
        csv = subset.to_csv(index=False).encode('utf-8')
        st.download_button(f"Download {target_seg} List", data=csv, file_name=f"{target_seg}_customers.csv", mime="text/csv")

else:
    st.info("Please upload a CSV file with CustomerID, TransactionDate, and TransactionAmount to begin.")