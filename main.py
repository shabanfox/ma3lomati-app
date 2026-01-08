import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="MA3LOMATI Pro", layout="wide")

# 2. Advanced UI System (Clean & Sharp)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Cairo:wght@600;900&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #090b10 !important;
        font-family: 'Inter', 'Cairo', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #11141d !important;
        border-right: 1px solid #1e222d;
    }

    /* Main Dashboard Layout */
    .app-container {
        display: flex;
        gap: 20px;
        padding: 20px;
    }

    /* Left Side: Inventory Grid */
    .inventory-section {
        flex: 3;
    }

    /* Right Side: Developer Intelligence Panel */
    .intel-panel {
        flex: 1;
        background: #11141d;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #1e222d;
        position: sticky; top: 20px;
        height: fit-content;
    }

    /* Micro Property Cards */
    .prop-card {
        background: #161a23;
        border: 1px solid #1e222d;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: 0.2s ease;
        border-left: 4px solid #c49a6c;
    }
    .prop-card:hover {
        background: #1c222d;
        border-color: #c49a6c;
        transform: translateX(5px);
    }

    .prop-price {
        color: #c49a6c;
        font-weight: 900;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    .prop-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 1rem;
        margin: 5px 0;
    }
    .prop-meta {
        color: #6d7681;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* Layout Utility */
    .flex-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 12px;
    }

    h1, h2, h3 { color: white !important; font-family: 'Cairo', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 3. Data Core
@st.cache_data(ttl=5)
def get_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        r = requests.get(URL); r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = get_data()

# 4. App Structure
if not df.empty:
    # Sidebar Filters
    with st.sidebar:
        st.markdown("<h2 style='font-size:20px; margin-bottom:30px;'>MA3LOMATI <span style='color:#c49a6c'>PRO</span></h2>", unsafe_allow_html=True)
        dev_list = sorted(df.iloc[:, 0].unique().tolist())
        s_dev = st.selectbox("Developer", dev_list)
        reg_list = ["All Regions"] + sorted(df.iloc[:, 4].unique().tolist())
        s_reg = st.selectbox("Location", reg_list)
        st.markdown("---")
        st.caption("v5.5 Broker Internal System")

    # Main Area
    c_cards, c_info = st.columns([2.8, 1.2], gap="medium")

    dev_data = df[df.iloc[:, 0] == s_dev]

    with c_info:
        # Developer Intel Panel (Sticky on Right)
        first = dev_data.iloc[0]
        st.markdown(f"""
            <div class="intel-panel">
                <p style="color:#c49a6c; font-size:11px; font-weight:900; text-transform:uppercase;">Developer Info</p>
                <h2 style="margin:5px 0 20px 0; font-size:24px;">{s_dev}</h2>
                <div style="background:#090b10; padding:15px; border-radius:10px; margin-bottom:20px;">
                    <small style="color:#6d7681;">Owner / Chairman</small><br>
                    <b style="color:white; font-size:16px;">{first.iloc[1]}</b>
                </div>
                <p style="color:#adb5bd; font-size:13px; line-height:1.6;">{first.iloc[2]}</p>
            </div>
        """, unsafe_allow_html=True)

    with c_cards:
        # Inventory Section
        f_df = dev_data
        if s_reg != "All Regions": f_df = dev_data[dev_data.iloc[:, 4] == s_reg]
        
        st.markdown(f"<h3>Inventory <span style='color:#c49a6c; font-size:14px;'>({len(f_df)} Projects)</span></h3>", unsafe_allow_html=True)
        
        st.markdown('<div class="flex-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            if r.iloc[3] != "-":
                st.markdown(f"""
                    <div class="prop-card">
                        <div class="prop-price">EGP {r.iloc[5]}</div>
                        <div class="prop-title">{r.iloc[3]}</div>
                        <div class="prop-meta">📍 {r.iloc[4]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("System Offline - Check Data Source")
