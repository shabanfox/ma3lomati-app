import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة (نظام التطبيقات)
st.set_page_config(page_title="MA3LOMATI Platform", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء كل زوائد ستريمليت */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b0e14 !important; /* خلفية داكنة فخمة */
        font-family: 'Cairo', sans-serif;
        color: #e0e0e0;
        direction: ltr !important;
    }

    /* الهيدر المتحرك السينمائي */
    .hero-banner {
        background: linear-gradient(-45deg, #0b0e14, #1c1f26, #c49a6c, #0b0e14);
        background_size: 400% 400%;
        animation: gradient 12s ease infinite;
        padding: 60px 20px;
        text-align: center;
        border-radius: 0 0 50px 50px;
        margin-bottom: 40px;
        border-bottom: 2px solid #c49a6c;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* تقسيم الشاشة: يمين (معلومات) | يسار (كروت) */
    .main-grid {
        display: flex;
        gap: 30px;
        padding: 0 40px;
        flex-direction: row-reverse; /* لضمان الشركة على اليمين */
    }

    /* لوحة الشركة - تصميم Dark Card */
    .company-panel {
        flex: 1;
        background: #161a23;
        border-radius: 25px;
        padding: 30px;
        border: 1px solid #2d333f;
        height: fit-content;
        position: sticky; top: 40px;
    }

    /* شبكة الكروت الصغيرة - تصميم Micro-Cards */
    .projects-container {
        flex: 2.5;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 15px;
    }

    .micro-card {
        background: #1c212c;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #2d333f;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .micro-card:hover {
        transform: scale(1.05);
        border-color: #c49a6c;
        box-shadow: 0 10px 30px rgba(196, 154, 108, 0.2);
    }

    .price-badge {
        color: #c49a6c;
        font-weight: 900;
        font-size: 0.8rem;
        margin-bottom: 10px;
        display: block;
    }
    .proj-name {
        font-weight: 700;
        font-size: 0.95rem;
        color: #ffffff;
    }
    .loc-tag {
        color: #8a8f98;
        font-size: 0.75rem;
        margin-top: 8px;
    }

    /* ستايل أدوات البحث */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1c212c;
        border-radius: 12px;
        color: white;
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

# 3. الهيدر المتحرك
st.markdown('<div class="hero-banner"><h1>MA3LOMATI</h1><p style="color:#c49a6c; letter-spacing:2px;">PREMIUM REAL ESTATE INTELLIGENCE</p></div>', unsafe_allow_html=True)

if not df.empty:
    # الفلاتر (أعلى الصفحة بشكل نظيف)
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("🏗️ Developer", sorted(df.iloc[:, 0].unique().tolist()))
    with c2: s_reg = st.selectbox("📍 Region", ["All Locations"] + sorted(df.iloc[:, 4].unique().tolist()))

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. توزيع المحتوى (يمين معلومات | يسار مشاريع)
    col_left, col_right = st.columns([2.5, 1], gap="large")

    dev_data = df[df.iloc[:, 0] == s_dev]

    with col_right:
        # كارت المطور
        row = dev_data.iloc[0]
        st.markdown(f"""
            <div class="company-panel">
                <span style="color:#c49a6c; font-size:0.7rem; font-weight:900;">OFFICIAL DATA</span>
                <h2 style="margin:5px 0 15px 0; color:#fff;">{s_dev}</h2>
                <div style="background:#1c212c; padding:15px; border-radius:15px;">
                    <small style="color:#8a8f98;">Owner / Chairman</small><br>
                    <b style="font-size:1.1rem; color:#c49a6c;">{row.iloc[1]}</b>
                </div>
                <p style="margin-top:20px; font-size:0.9rem; line-height:1.6; color:#b0b5bc;">{row.iloc[2]}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_left:
        # عرض المشاريع
        f_df = dev_data
        if s_reg != "All Locations": f_df = dev_data[dev_data.iloc[:, 4] == s_reg]
        
        st.markdown(f"<p style='margin-left:10px; color:#c49a6c;'>Showing {len(f_df)} Projects</p>", unsafe_allow_html=True)
        st.markdown('<div class="projects-container">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            if r.iloc[3] != "-":
                st.markdown(f"""
                    <div class="micro-card">
                        <span class="price-badge">{r.iloc[5]}</span>
                        <div class="proj-name">{r.iloc[3]}</div>
                        <div class="loc-tag">📍 {r.iloc[4]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data connection error.")
