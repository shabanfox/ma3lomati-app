import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="MA3LOMATI | Elite Dashboard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: ltr !important;
        font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
        background: radial-gradient(circle at top right, #fdfcfb 0%, #e2d1c3 100%);
        color: #1a1e23;
    }

    /* Top Glass Nav */
    .top-nav {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(10px);
        padding: 15px 40px;
        color: white;
        border-bottom: 2px solid #c49a6c;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky; top: 0; z-index: 1000;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    /* Sidebar Info Panel - Glass Effect */
    .info-panel-premium {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        position: sticky; top: 100px;
    }

    /* Project Cards - Modern Grid */
    .project-grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 20px;
    }

    .project-card-luxury {
        background: white;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid transparent;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 180px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }

    .project-card-luxury:hover {
        transform: scale(1.03);
        border-color: #c49a6c;
        box-shadow: 0 25px 50px rgba(196, 154, 108, 0.15);
    }

    .status-badge {
        background: linear-gradient(135deg, #c49a6c 0%, #a67c52 100%);
        color: white;
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 800;
        width: fit-content;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }

    .card-title {
        font-weight: 800;
        font-size: 1.1rem;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .card-loc {
        display: flex;
        align-items: center;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Smooth Filter Box */
    .filter-dock {
        background: white;
        border-radius: 20px;
        padding: 20px 30px;
        margin-bottom: 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
        border: 1px solid #f1f5f9;
    }

    h1, h2, h3 { font-family: 'Cairo', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 2. Data Load
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

# Navigation
st.markdown("""
    <div class="top-nav">
        <div style="font-size: 1.8rem; font-weight: 900; letter-spacing: 2px;">MA3LOMATI<span style="color:#c49a6c">.</span></div>
        <div style="font-size: 0.9rem; font-weight: 400; color: #94a3b8;">Real Estate Portfolio v2.0</div>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    C_DEV = df.columns[0]; C_OWNER = df.columns[1]; C_BIO = df.columns[2]
    C_PROJ = df.columns[3]; C_REG = df.columns[4]; C_PRICE = df.columns[5]

    # Filter Dock
    st.markdown('<div style="padding: 0 40px;">', unsafe_allow_html=True)
    st.markdown('<div class="filter-dock">', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1: s_dev = st.selectbox("🏢 Select Real Estate Giant", sorted(df[C_DEV].unique().tolist()))
    with f2: s_reg = st.selectbox("📍 Target Location", ["All Locations"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    # Content Grid
    col_cards, col_info = st.columns([2.8, 1.2], gap="large")

    dev_data = df[df[C_DEV] == s_dev]

    with col_info:
        if not dev_data.empty:
            info = dev_data.iloc[0]
            st.markdown(f"""
                <div class="info-panel-premium">
                    <div style="width: 50px; height: 5px; background: #c49a6c; margin-bottom: 20px; border-radius: 10px;"></div>
                    <h1 style="margin: 0 0 10px 0; font-size: 2.5rem; color: #0f172a; font-weight: 900;">{s_dev}</h1>
                    <div style="background: #f8fafc; padding: 15px; border-radius: 15px; margin: 20px 0;">
                        <span style="display:block; font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Ownership</span>
                        <span style="font-size: 1.1rem; color: #0f172a; font-weight: 700;">{info[C_OWNER]}</span>
                    </div>
                    <p style="line-height: 1.8; color: #475569; font-size: 0.95rem;">{info[C_BIO]}</p>
                </div>
            """, unsafe_allow_html=True)

    with col_cards:
        display_df = dev_data
        if s_reg != "All Locations":
            display_df = dev_data[dev_data[C_REG] == s_reg]
        
        st.markdown(f'<h3 style="margin-left: 10px; margin-bottom: 25px; color: #0f172a; display: flex; align-items: center;">Available Inventory <span style="margin-left: 15px; background: #0f172a; color: white; padding: 2px 12px; border-radius: 10px; font-size: 0.9rem;">{len(display_df)}</span></h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="project-grid-container">', unsafe_allow_html=True)
        for _, row in display_df.iterrows():
            if row[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="project-card-luxury">
                        <div>
                            <div class="status-badge">{row[C_PRICE]}</div>
                            <div class="card-title">{row[C_PROJ]}</div>
                        </div>
                        <div class="card-loc">
                            <span style="margin-right: 5px;">📍</span> {row[C_REG]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Connection Lost. Re-syncing...")
