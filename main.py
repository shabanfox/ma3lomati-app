import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة بأسلوب Nawy
st.set_page_config(page_title="Ma3lomati | Pro Broker Tool", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء عناصر ستريمليت */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    /* التصميم العام (Clean & Professional) */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8f9fb !important;
        font-family: 'Cairo', sans-serif;
        color: #1a202c;
        direction: ltr !important;
    }

    /* هيدر يشبه Nawy */
    .nawy-header {
        background: #ffffff;
        padding: 15px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e2e8f0;
        position: sticky; top: 0; z-index: 1000;
    }

    /* كارت المطور (يمين) - ستايل Nawy Sidebar */
    .dev-sidebar {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        position: sticky; top: 100px;
    }

    /* كروت المشاريع (يسار) - Clean Cards */
    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
    }

    .nawy-card {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 20px;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
    }
    .nawy-card:hover {
        border-color: #0056b3;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    .price-nawy {
        color: #0056b3;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 8px;
    }

    .title-nawy {
        font-weight: 700;
        font-size: 1rem;
        color: #2d3748;
        margin-bottom: 4px;
    }

    .loc-nawy {
        color: #718096;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
    }

    /* تخصيص صناديق الاختيار */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
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

# Header
st.markdown("""
    <div class="nawy-header">
        <div style="font-size: 1.4rem; font-weight: 900; color: #0056b3;">MA3LOMATI<span style="color:#1a202c;">PRO</span></div>
        <div style="font-size: 0.85rem; color: #718096; font-weight: 600;">Internal Broker Portal</div>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # المنطقة العلوية للفلاتر (Clean Search Bar style)
    st.markdown('<div style="padding: 20px 40px 0 40px;">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1: s_dev = st.selectbox("Search Developer", sorted(df.iloc[:, 0].unique().tolist()))
    with c2: s_reg = st.selectbox("Location", ["All Egypt"] + sorted(df.iloc[:, 4].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    # المحتوى الرئيسي
    col_left, col_right = st.columns([2.5, 1], gap="large")

    dev_data = df[df.iloc[:, 0] == s_dev]

    with col_right:
        # لوحة معلومات المطور (Right Sidebar)
        row = dev_data.iloc[0]
        st.markdown(f"""
            <div class="dev-sidebar">
                <h2 style="margin:0 0 10px 0; font-size:1.5rem; color:#1a202c;">{s_dev}</h2>
                <div style="margin-bottom:20px;">
                    <small style="color:#718096; text-transform:uppercase; font-weight:700;">Chairman</small><br>
                    <b style="color:#2d3748; font-size:1.1rem;">{row.iloc[1]}</b>
                </div>
                <hr style="opacity:0.1">
                <p style="color:#4a5568; font-size:0.95rem; line-height:1.6; text-align:justify;">{row.iloc[2]}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_left:
        # عرض المشاريع (Inventory Grid)
        f_df = dev_data
        if s_reg != "All Egypt": f_df = dev_data[dev_data.iloc[:, 4] == s_reg]
        
        st.markdown(f"<p style='color:#718096; font-weight:600; margin-bottom:20px; padding-left:10px;'>{len(f_df)} Results found</p>", unsafe_allow_html=True)
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            if r.iloc[3] != "-":
                st.markdown(f"""
                    <div class="nawy-card">
                        <div class="price-nawy">{r.iloc[5]}</div>
                        <div class="title-nawy">{r.iloc[3]}</div>
                        <div class="loc-nawy">📍 {r.iloc[4]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Connection Error with Sheets")
