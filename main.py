import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء الهيدر وأدوات ستريمليت */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif;
        background-color: #f4f7f9;
        color: #1e272e;
    }

    /* الهيدر الفخم */
    .hero-container {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #c49a6c, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
        padding: 60px 20px;
        text-align: center;
        border-bottom: 5px solid #c49a6c;
        border-radius: 0 0 50px 50px;
        margin-bottom: 40px;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* شريط البحث المنظم */
    .search-section {
        background: white;
        padding: 20px 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin: -50px auto 30px auto;
        max-width: 90%;
        display: flex;
        gap: 20px;
        z-index: 100;
        position: relative;
    }

    /* كارت المطور الرئيسي */
    .dev-info-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 40px;
        border-right: 10px solid #c49a6c;
        box-shadow: 0 15px 35px rgba(0,0,0,0.03);
    }

    /* شبكة الكروت (4 في الصف) */
    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 20px;
        padding: 10px;
    }

    /* تصميم الكارت الفخم والمصغر */
    .premium-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #eef0f2;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 180px;
    }
    .premium-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        border-color: #c49a6c;
    }
    
    .price-badge {
        background: rgba(196, 154, 108, 0.1);
        color: #c49a6c;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.85em;
        display: inline-block;
        margin-bottom: 10px;
        border: 1px solid #c49a6c;
    }

    .project-title {
        font-weight: 700;
        font-size: 1.1em;
        color: #1a1a1a;
        margin: 5px 0;
    }
    .project-loc {
        color: #7f8c8d;
        font-size: 0.85em;
        margin-bottom: 10px;
    }
    .dev-tag {
        color: #c49a6c;
        font-weight: 600;
        font-size: 0.8em;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
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
st.markdown('<div class="hero-container"><h1 style="font-size: 3.5em; font-weight: 900; color: white; margin:0;">مـعـلـومـاتـي</h1><p style="color: #f1e6d8; font-size: 1.1em; opacity: 0.8;">المرجع الأول لبروكر العقارات في مصر</p></div>', unsafe_allow_html=True)

if not df.empty:
    # دالة ذكية لإيجاد الأعمدة
    def find_col(options, idx):
        for opt in options:
            if opt in df.columns: return opt
        return df.columns[idx] if len(df.columns) > idx else df.columns[0]

    C_DEV = find_col(["المطور", "الشركة"], 0)
    C_OWNER = find_col(["المالك", "الاونر"], 1)
    C_BIO = find_col(["سيرة عن الشركة والاونر"], 2)
    C_PROJ = find_col(["المشروع", "اسم المشروع"], 3)
    C_REG = find_col(["المنطقة", "المنطقه"], 4)
    C_PRICE = find_col(["السعر"], 5)

    # شريط الفلاتر
    st.markdown('<div class="search-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: s_dev = st.selectbox("🏢 الشركة المطورة", ["عرض جميع المطورين"] + sorted(df[C_DEV].unique().tolist()))
    with col2: s_reg = st.selectbox("📍 المنطقة / الموقع", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    if s_dev != "عرض جميع المطورين":
        dev_info = df[df[C_DEV] == s_dev].iloc[0]
        st.markdown(f"""
            <div class="dev-info-card">
                <h2 style="color:#c49a6c; margin-bottom:10px; font-weight:900;">{s_dev}</h2>
                <p style="font-size:1.1em;"><b>👤 الإدارة والملكية:</b> {dev_info[C_OWNER]}</p>
                <hr style="opacity:0.05; margin:15px 0;">
                <p style="line-height:1.7; color:#444;">{dev_info[C_BIO]}</p>
            </div>
            <h4 style="margin-right:10px; margin-bottom:20px; color:#0f172a; font-weight:900;">🏗️ المشاريع المتاحة:</h4>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in df[df[C_DEV] == s_dev].iterrows():
            if r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="premium-card">
                        <div>
                            <div class="price-badge">{r[C_PRICE]}</div>
                            <div class="project-title">{r[C_PROJ]}</div>
                            <div class="project-loc">📍 {r[C_REG]}</div>
                        </div>
                        <div style="font-size:0.8em; color:#999; border-top:1px solid #f9f9f9; pt:10px;">
                            📋 {r.get('السداد', 'نظام السداد متاح')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # العرض العام لجميع المشاريع
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        
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
    st.warning("جاري مزامنة البيانات من السحابة...")
