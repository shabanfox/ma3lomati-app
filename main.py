import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة وإخفاء هوية المنصة تماماً
st.set_page_config(page_title="معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والسهم تماماً */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #05070a; color: #ffffff;
    }

    /* هيدر احترافي بخلفية متحركة */
    .hero-section {
        background: linear-gradient(-45deg, #05070a, #1c2128, #2d240a, #05070a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        padding: 80px 20px; text-align: center;
        border-bottom: 3px solid #d4af37; border-radius: 0 0 50px 50px;
        margin-bottom: 40px; box-shadow: 0 15px 40px rgba(0,0,0,0.7);
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* كارت المطور الملكي (Nawy Style) */
    .dev-profile-card {
        background: #111418; border: 1px solid #d4af37; border-radius: 25px;
        padding: 40px; margin-bottom: 40px; border-right: 12px solid #d4af37;
    }

    /* شبكة المشاريع المنظمة */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 25px; margin-top: 20px;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 20px;
        padding: 25px; position: relative; transition: all 0.4s ease;
    }
    .project-card:hover {
        border-color: #d4af37; transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(212, 175, 55, 0.2);
    }
    .price-badge {
        background: #d4af37; color: #000; padding: 6px 15px;
        border-radius: 10px; font-weight: 900; position: absolute; left: 20px; top: 20px;
    }

    /* تنسيق الفلاتر */
    .stSelectbox label { color: #d4af37 !important; font-size: 1.2em !important; font-weight: bold; }
    div[data-baseweb="select"] { background-color: #111418 !important; border: 1px solid #d4af37 !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات وتأمين الأعمدة
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# الهيدر الفخم
st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 4em; font-weight: 900; color: #d4af37; margin:0;">مـعـلـومـاتـي</h1>
        <p style="font-size: 1.4em; color: #ffffff; opacity: 0.8; margin-top:10px;">المنصة الذكية للعقارات في مصر</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # دالة لتجنب أخطاء KeyError
    def get_col(names):
        for n in names:
            if n in df.columns: return n
        return df.columns[0]

    C_DEV = get_col(["المطور", "Developer"])
    C_REG = get_col(["المنطقة", "Location"])
    C_PROJ = get_col(["المشروع", "Project"])
    C_OWNER = get_col(["المالك", "Owner"])
    C_BIO = get_col(["سابقة_الأعمال", "Bio"])

    # البحث (تصميم نظيف)
    col1, col2 = st.columns(2)
    with col1: s_dev = st.selectbox("🏢 المطور العقاري", ["عرض الكل"] + sorted(df[C_DEV].unique().tolist()))
    with col2: s_reg = st.selectbox("📍 المنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))

    st.markdown("<br><br>", unsafe_allow_html=True)

    if s_dev != "عرض الكل":
        # عرض المطور كبروفايل احترافي واحد
        dev_group = df[df[C_DEV] == s_dev]
        main_info = dev_group.iloc[0]
        
        st.markdown(f"""
            <div class="dev-profile-card">
                <h2 style="color:#d4af37; font-size: 2.5em; margin-bottom:10px;">{s_dev}</h2>
                <p style="font-size:1.2em;">👤 <b>الإدارة:</b> {main_info.get(C_OWNER, '-')}</p>
                <hr style="opacity:0.1; margin:20px 0;">
                <h4 style="color:#d4af37;">📜 سابقة الأعمال وتاريخ الشركة:</h4>
                <p style="line-height:1.9; color:#eee;">{main_info.get(C_BIO, '-')}</p>
            </div>
            <h3 style="text-align:center; color:#d4af37; margin-bottom:30px;">🏗️ مشاريع الشركة المتاحة</h3>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, p in dev_group.iterrows():
            if p[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-badge">{p.get('السعر', '-')}</div>
                        <h3 style="color:#d4af37; margin-top:40px;">{p[C_PROJ]}</h3>
                        <p style="margin: 15px 0;">📍 {p[C_REG]} | 🏗️ {p.get('النوع','-')}</p>
                        <div style="background: rgba(212,175,55,0.05); padding: 10px; border-radius: 10px; font-size: 0.85em; color: #aaa;">
                            💳 نظام السداد: {p.get('السداد','-')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث العام (شبكة مشاريع)
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{r.get('السعر', '-')}</div>
                    <h3 style="color:#d4af37; margin-top:40px;">{r[C_PROJ]}</h3>
                    <p style="margin: 5px 0;">🏢 {r[C_DEV]}</p>
                    <p style="font-size: 0.9em; opacity: 0.7;">📍 {r[C_REG]}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("جاري تحميل البيانات... تأكد من نشر الشيت بصيغة CSV.")
