import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة (تصميم ناي الأصلي)
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f7f9fc !important;
        font-family: 'Cairo', sans-serif;
        direction: ltr !important;
    }

    .nawy-header {
        background: white; padding: 15px 40px; border-bottom: 1px solid #e2e8f0;
        margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;
    }

    .dev-sidebar {
        background: white; border-radius: 12px; padding: 25px;
        border: 1px solid #e2e8f0; position: sticky; top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    .inventory-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
    }

    .nawy-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        padding: 24px; transition: 0.3s ease; display: flex;
        flex-direction: column; justify-content: space-between; min-height: 170px;
    }
    .nawy-card:hover {
        border-color: #0052cc; transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    .price-nawy { color: #0052cc; font-weight: 900; font-size: 1.2rem; }
    .title-nawy { font-weight: 700; font-size: 1.1rem; color: #1e293b; margin: 10px 0; }
    .loc-nawy { color: #64748b; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب الداتا (حل مشكلة الـ KeyError نهائياً)
@st.cache_data(ttl=2)
def load_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        r = requests.get(URL); r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        return df.fillna("-")
    except: return pd.DataFrame()

df = load_data()

# الهيدر العلوي
st.markdown('<div class="nawy-header"><h2 style="margin:0; color:#0052cc; font-weight:900;">MA3LOMATI <span style="color:#1e293b">PRO</span></h2></div>', unsafe_allow_html=True)

if not df.empty and len(df.columns) >= 6:
    # الفلاتر (البحث والمكان)
    st.markdown('<div style="padding: 0 40px;">', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    with f1: 
        s_dev = st.selectbox("Search Developer", sorted(df.iloc[:, 0].unique().tolist()))
    with f2: 
        s_reg = st.selectbox("Location", ["All Egypt"] + sorted(df.iloc[:, 4].unique().tolist()))
    st.markdown('</div><br>', unsafe_allow_html=True)

    # تقسيم الشاشة (يمين معلومات | يسار مشاريع)
    col_cards, col_sidebar = st.columns([2.6, 1.4], gap="large")

    dev_df = df[df.iloc[:, 0] == s_dev]

    with col_sidebar:
        # لوحة الشركة (على اليمين ثابتة)
        res = dev_df.iloc[0]
        st.markdown(f"""
            <div class="dev-sidebar">
                <p style="color:#0052cc; font-size:11px; font-weight:900; margin-bottom:5px; letter-spacing:1px;">CORPORATE PROFILE</p>
                <h2 style="margin:0 0 20px 0; color:#0f172a;">{s_dev}</h2>
                <div style="background:#f1f5f9; padding:15px; border-radius:10px; margin-bottom:20px; border-right: 5px solid #0052cc;">
                    <small style="color:#64748b;">Chairman / Owner</small><br>
                    <b style="color:#1e293b; font-size:1.15rem;">{res.iloc[1]}</b>
                </div>
                <p style="color:#475569; font-size:14px; line-height:1.7; text-align:justify;">{res.iloc[2]}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_cards:
        # شبكة المشاريع (على اليسار)
        final_df = dev_df
        if s_reg != "All Egypt": 
            final_df = dev_df[dev_df.iloc[:, 4] == s_reg]
        
        st.markdown(f"<p style='color:#64748b; font-weight:600; margin-bottom:15px; padding-left:10px;'>Inventory ({len(final_df)} Projects)</p>", unsafe_allow_html=True)
        st.markdown('<div class="inventory-grid">', unsafe_allow_html=True)
        for _, r in final_df.iterrows():
            if str(r.iloc[3]) != "-":
                st.markdown(f"""
                    <div class="nawy-card">
                        <div>
                            <div class="price-nawy">EGP {r.iloc[5]}</div>
                            <div class="title-nawy">{r.iloc[3]}</div>
                        </div>
                        <div class="loc-nawy">📍 {r.iloc[4]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data Sync Error: Please check your Google Sheet public link.")
