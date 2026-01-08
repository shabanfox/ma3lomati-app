import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة - أسلوب Nawy الاحترافي
st.set_page_config(page_title="MA3LOMATI | Pro Broker", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;900&family=Inter:wght@400;600&display=swap');
    
    /* تنظيف الواجهة من زوائد ستريمليت */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        font-family: 'Inter', 'Cairo', sans-serif;
        direction: ltr !important;
    }

    /* هيدر المنصة العلوي */
    .nawy-style-nav {
        background: white;
        padding: 15px 40px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    /* كارت معلومات المطور (الجهة اليمنى) */
    .sticky-dev-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        position: sticky; top: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* كروت المشاريع (الجهة اليسرى) */
    .nawy-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 16px;
    }

    .property-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 150px;
    }
    .property-card:hover {
        border-color: #0052cc;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.04);
    }

    .price-nawy { color: #0052cc; font-weight: 800; font-size: 1.15rem; }
    .title-nawy { font-weight: 700; font-size: 1rem; color: #1e293b; margin: 8px 0; }
    .loc-nawy { color: #64748b; font-size: 0.85rem; font-weight: 500; }

    /* تحسين شكل الفلاتر */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        border-radius: 8px !important;
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

# Navbar
st.markdown('<div class="nawy-style-nav"><h2 style="margin:0; color:#0052cc; font-weight:900; font-size:1.5rem;">MA3LOMATI</h2><span style="color:#64748b; font-weight:600;">BROKER INTERNAL TOOL</span></div>', unsafe_allow_html=True)

if not df.empty:
    # شريط البحث والفلاتر
    st.markdown('<div style="padding: 0 40px;">', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    with f1: s_dev = st.selectbox("Search Developer", sorted(df.iloc[:, 0].unique().tolist()))
    with f2: s_reg = st.selectbox("Area", ["All Areas"] + sorted(df.iloc[:, 4].unique().tolist()))
    st.markdown('</div><br>', unsafe_allow_html=True)

    # التوزيع الرئيسي للمحتوى
    col_content, col_sidebar = st.columns([2.8, 1.2], gap="large")

    dev_data = df[df.iloc[:, 0] == s_dev]

    # الجانب الأيمن: بروفايل الشركة
    with col_sidebar:
        if not dev_data.empty:
            info = dev_data.iloc[0]
            st.markdown(f"""
                <div class="sticky-dev-card">
                    <p style="color:#0052cc; font-size:11px; font-weight:800; letter-spacing:1px; margin-bottom:10px;">CORPORATE DATA</p>
                    <h2 style="margin:0 0 20px 0; color:#0f172a; font-size:1.8rem;">{s_dev}</h2>
                    <div style="background:#f1f5f9; padding:15px; border-radius:10px; margin-bottom:20px;">
                        <small style="color:#64748b;">Chairman / Owner</small><br>
                        <b style="color:#1e293b; font-size:1.1rem;">{info.iloc[1]}</b>
                    </div>
                    <p style="color:#475569; font-size:0.95rem; line-height:1.7;">{info.iloc[2]}</p>
                </div>
            """, unsafe_allow_html=True)

    # الجانب الأيسر: المشاريع
    with col_content:
        display_df = dev_data
        if s_reg != "All Areas":
            display_df = dev_data[dev_data.iloc[:, 4] == s_reg]
        
        st.markdown(f"<p style='color:#64748b; font-weight:600; margin-bottom:15px; padding-left:5px;'>Results ({len(display_df)})</p>", unsafe_allow_html=True)
        st.markdown('<div class="nawy-grid">', unsafe_allow_html=True)
        for _, r in display_df.iterrows():
            if r.iloc[3] != "-":
                st.markdown(f"""
                    <div class="property-card">
                        <div>
                            <div class="price-nawy">EGP {r.iloc[5]}</div>
                            <div class="title-nawy">{r.iloc[3]}</div>
                        </div>
                        <div class="loc-nawy">📍 {r.iloc[4]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data connection failed.")
