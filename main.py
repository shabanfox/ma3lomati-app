import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة (Nawy-Style)
st.set_page_config(page_title="Ma3lomati | Pro Platform", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Cairo:wght@600;700;900&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f7fa !important;
        font-family: 'Inter', 'Cairo', sans-serif;
    }

    /* الهيدر العلوي */
    .nawy-nav {
        background: #ffffff;
        padding: 15px 50px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    /* كارت البروفايل (يمين) */
    .dev-profile-box {
        background: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        position: sticky; top: 20px;
    }

    /* كروت المشاريع (يسار) */
    .project-card-v2 {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        transition: 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 140px;
    }
    .project-card-v2:hover {
        border-color: #0052cc;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    .price-label { color: #0052cc; font-weight: 800; font-size: 1.1rem; }
    .project-title { font-weight: 700; font-size: 1rem; color: #1a202c; margin: 8px 0; }
    .loc-label { color: #718096; font-size: 0.85rem; }

    /* شبكة الكروت */
    .inventory-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب الداتا
@st.cache_data(ttl=5)
def load_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        res = requests.get(URL); res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# Navbar
st.markdown('<div class="nawy-nav"><h2 style="margin:0; color:#0052cc; font-weight:900;">MA3LOMATI</h2><span style="color:#718096; font-weight:600;">BROKER PLATFORM</span></div>', unsafe_allow_html=True)

if not df.empty:
    # المنطقة العلوية للفلاتر
    st.markdown('<div style="padding: 0 50px;">', unsafe_allow_html=True)
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1: s_dev = st.selectbox("Search Developer", sorted(df.iloc[:, 0].unique().tolist()))
    with c_f2: s_reg = st.selectbox("Filter Location", ["All Egypt"] + sorted(df.iloc[:, 4].unique().tolist()))
    st.markdown('</div><br>', unsafe_allow_html=True)

    # تقسيم الشاشة (يسار للمشاريع | يمين للمعلومات)
    col_content, col_info = st.columns([2.5, 1], gap="large")

    dev_data = df[df.iloc[:, 0] == s_dev]

    with col_info:
        # كارت معلومات المطور (على اليمين)
        if not dev_data.empty:
            row = dev_data.iloc[0]
            st.markdown(f"""
                <div class="dev-profile-box">
                    <p style="color:#0052cc; font-size:12px; font-weight:800; letter-spacing:1px; margin-bottom:10px;">DEVELOPER INTELLIGENCE</p>
                    <h2 style="margin:0 0 15px 0; color:#1a202c; font-size:24px;">{s_dev}</h2>
                    <div style="background:#f8f9fb; padding:15px; border-radius:10px; margin-bottom:20px;">
                        <small style="color:#718096;">Chairman / Owner</small><br>
                        <b style="color:#1a202c; font-size:18px;">{row.iloc[1]}</b>
                    </div>
                    <p style="color:#4a5568; font-size:14px;
