import streamlit as st
import pandas as pd
import plotly.express as px
from services.sheets_service import update_google_sheet

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="🚚 Delivery Allocation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center; color: #00FFFF;'>🚚 Delivery Allocation Dashboard</h1>", unsafe_allow_html=True)

# ------------------ Cached CSV Processing ------------------
@st.cache_data
def process_csv(file):
    df = pd.read_csv(file)
    # Assign dummy Driver/Vehicle if not present
    if "Driver" not in df.columns:
        df["Driver"] = ["Driver " + str(i//35 + 1) for i in range(len(df))]
    if "Vehicle" not in df.columns:
        df["Vehicle"] = ["Vehicle " + str(i//35 + 1) for i in range(len(df))]
    return df

# ------------------ Upload CSV ------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = process_csv(uploaded_file)

    # Validate required columns
    required_cols = ["Address", "Customer ID", "Pincode", "Cylinder Type"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"CSV must include columns: {required_cols}")
    else:
        st.success("CSV uploaded successfully!")
        st.dataframe(df)

        # Update Google Sheet
        sheet_url = update_google_sheet(df)
        if sheet_url:
            st.success(f"✅ Dashboard Uploaded! [Open Sheet]({sheet_url})")

        # ------------------ Modern AI-Style Charts ------------------
        st.markdown("### 📊 Delivery Summary Charts")
        st.markdown("<hr>", unsafe_allow_html=True)

        # 1️⃣ Deliveries per Pincode
        fig1 = px.histogram(
            df, x="Pincode", title="Deliveries per Pincode",
            color="Pincode", template="plotly_dark"
        )

        # 2️⃣ Deliveries per Driver
        fig2 = px.histogram(
            df, x="Driver", title="Deliveries per Driver",
            color="Driver", template="plotly_dark"
        )

        # 3️⃣ Deliveries per Vehicle
        fig3 = px.histogram(
            df, x="Vehicle", title="Deliveries per Vehicle",
            color="Vehicle", template="plotly_dark"
        )

        # Display charts in 3-column layout
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig1, use_container_width=True)
        col2.plotly_chart(fig2, use_container_width=True)
        col3.plotly_chart(fig3, use_container_width=True)

        # ------------------ Optional: KPIs ------------------
        st.markdown("### ⚡ Key Insights")
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Deliveries", len(df))
        col2.metric("Total Drivers", df["Driver"].nunique())
        col3.metric("Total Vehicles", df["Vehicle"].nunique())
