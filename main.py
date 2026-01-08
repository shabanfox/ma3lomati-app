import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة (تصميم نظيف وفاخر)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء زوائد المنصة */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #f8f9fa; color: #1e272e;
    }

    /* الهيدر المتحرك الجذاب */
    .hero-container {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #c49a6c, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
        padding: 80px 20px; text-align: center;
        border-bottom: 5px solid #c49a6c; border-radius: 0 0 60px 60px;
        margin-bottom: 40px; box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* كروت المشاريع والمطورين */
    .info-card {
        background: white; border-radius: 20px; padding: 30px;
        margin-bottom: 30px; border-right: 10px solid #c49a6c;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    }
    
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 25px;
    }
    .project-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 1px solid #eee; transition: 0.3s; position: relative;
    }
    .project-card:hover { transform: translateY(-5px); border-color: #c49a6c; box-shadow: 0 12px 30px rgba(0,0,0,0.1); }
    
    .price-badge {
        background: #c49a6c; color: white; padding: 4px 12px;
        border-radius: 8px; font-weight: 700; position: absolute; left: 15px; top: 15px;
    }

    /* شريط البحث */
    .search-section { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-top: -60px; z-index: 100; position: relative; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات (CSV)
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

# الهيدر
st.markdown('<div class="hero-container"><h1 style="font-size: 4em; font-weight: 900; color: white; margin:0;">مـعـلـومـاتـي</h1><p style="color: #f1e6d8; font-size: 1.2em; opacity: 0.9;">دليل البروكر الذكي لشركات التطوير العقاري</p></div>', unsafe_allow_html=True)

if not df.empty:
    # دالة للبحث عن الأعمدة بأي اسم قريب
    def find_col(possible_names, default_idx):
        for name in possible_names:
            if name in df.columns: return name
        return df.columns[default_idx] if len(df.columns) > default_idx else df.columns[0]

    C_DEV = find_col(["المطور", "الشركة", "اسم الشركة"], 0)
    C_OWNER = find_col(["المالك", "الاونر", "اسم الاونر"], 1)
    C_BIO = find_col(["سيرة عن الشركة والاونر", "سابقة الاعمال", "سيرة الشركة"], 2)
    C_PROJ = find_col(["المشروع", "اسم المشروع"], 3)
    C_REG = find_col(["المنطقة", "المنطقه", "مكان"], 4)
    C_PRICE = find_col(["السعر", "سعر"], 5)

    # شريط البحث
    st.markdown('<div class="search-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: s_dev = st.selectbox("🏢 اختر المطور العقاري", ["عرض الكل"] + sorted(df[C_DEV].unique().tolist()))
    with col2: s_reg = st.selectbox("📍 فلتر حسب المنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div><br><br>', unsafe_allow_html=True)

    if s_dev != "عرض الكل":
        dev_info = df[df[C_DEV] == s_dev].iloc[0]
        st.markdown(f"""
            <div class="info-card">
                <h2 style="color:#c49a6c; margin-bottom:10px;">{s_dev}</h2>
                <p style="font-size:1.2em;">👤 <b>المالك:</b> {dev_info[C_OWNER]}</p>
                <hr style="opacity:0.1;">
                <p style="line-height:1.8;"><b>📜 معلومات الشركة:</b><br>{dev_info[C_BIO]}</p>
            </div>
            <h3 style="margin-bottom:20px; font-weight:700;">🏗️ مشاريع الشركة</h3>
        """, unsafe_allow_html=True)
        
        # عرض مشاريع المطور
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in df[df[C_DEV] == s_dev].iterrows():
            if r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-badge">{r[C_PRICE]}</div>
                        <h4 style="margin-top:35px;">{r[C_PROJ]}</h4>
                        <p style="color:#666; font-size:0.9em;">📍 {r[C_REG]}</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            if r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-badge">{r[C_PRICE]}</div>
                        <h4 style="margin-top:35px;">{r[C_PROJ]}</h4>
                        <p style="color:#c49a6c; font-weight:bold;">🏢 {r[C_DEV]}</p>
                        <p style="color:#666; font-size:0.9em;">📍 {r[C_REG]}</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("جاري تحميل البيانات... تأكد من نشر الشيت بصيغة CSV.")
