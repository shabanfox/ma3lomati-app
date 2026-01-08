import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Ma3lomati Dashboard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* Hide Streamlit components */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: ltr !important;
        text-align: left !important;
        font-family: 'Cairo', sans-serif;
        background-color: #f8f9fb;
    }

    /* Animated Hero Section */
    .hero-container {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #c49a6c, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
        padding: 50px 20px;
        text-align: center;
        border-bottom: 5px solid #c49a6c;
        border-radius: 0 0 40px 40px;
        margin-bottom: 40px;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Compact Search Section */
    .search-section {
        background: white;
        padding: 15px 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin: -40px auto 30px auto;
        max-width: 85%;
        z-index: 100;
        position: relative;
    }

    /* Project Grid - Adjusted for smaller cards (5 per row) */
    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
        gap: 15px;
        padding: 0 20px;
    }

    /* Slim Luxury Card */
    .premium-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #eef0f2;
        transition: all 0.3s ease;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.08);
        border-color: #c49a6c;
    }
    
    .price-badge {
        background: #fcf8f3;
        color: #c49a6c;
        padding: 3px 10px;
        border-radius: 5px;
        font-weight: 800;
        font-size: 0.75em;
        border: 1px solid #eee;
        display: inline-block;
        margin-bottom: 8px;
    }

    .project-title {
        font-weight: 700;
        font-size: 0.95em;
        color: #1a1a1a;
        margin: 4px 0;
        line-height: 1.3;
    }
    .project-loc {
        color: #888;
        font-size: 0.8em;
        margin-bottom: 8px;
    }
    .dev-tag {
        color: #c49a6c;
        font-weight: 600;
        font-size: 0.75em;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading
RAW_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(RAW_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# Hero
st.markdown('<div class="hero-container"><h1 style="color:white; margin:0; font-size:3em; font-weight:900;">Ma3lomati</h1><p style="color:#c49a6c; font-weight:600;">Real Estate Intelligence Hub</p></div>', unsafe_allow_html=True)

if not df.empty:
    # Column Discovery
    def find_col(options, idx):
        for opt in options:
            if opt in df.columns: return opt
        return df.columns[idx] if len(df.columns) > idx else df.columns[0]

    C_DEV = find_col(["المطور", "الشركة"], 0)
    C_PROJ = find_col(["المشروع", "اسم المشروع"], 3)
    C_REG = find_col(["المنطقة", "المنطقه"], 4)
    C_PRICE = find_col(["السعر"], 5)

    # Filters
    st.markdown('<div class="search-section">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("Company", ["All Companies"] + sorted(df[C_DEV].unique().tolist()))
    with c2: s_reg = st.selectbox("Location", ["All Locations"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    # View Logic
    f_df = df.copy()
    if s_dev != "All Companies": f_df = f_df[f_df[C_DEV] == s_dev]
    if s_reg != "All Locations": f_df = f_df[f_df[C_REG] == s_reg]

    st.markdown('<div class="project-grid">', unsafe_allow_html=True)
    for _, r in f_df.iterrows():
        if r[C_PROJ] != "-":
            st.markdown(f"""
                <div class="premium-card">
                    <div>
                        <div class="price-badge">{r[C_PRICE]}</div>
                        <div class="project-title">{r[C_PROJ]}</div>
                        <div class="dev-tag">🏢 {r[C_DEV]}</div>
                    </div>
                    <div class="project-loc">📍 {r[C_REG]}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Loading inventory...")
