import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة وإخفاء كل زوائد المنصة
st.set_page_config(page_title="معلوماتي العقارية | الدليل الشامل", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والقوائم تماماً */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #05070a; color: #ffffff;
    }

    /* الهيدر الفخم بخلفية سينمائية متحركة */
    .hero-container {
        background: linear-gradient(-45deg, #05070a, #1c2128, #2d240a, #05070a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        padding: 80px 20px; text-align: center;
        border-bottom: 3px solid #d4af37; border-radius: 0 0 60px 60px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.8); margin-bottom: 50px;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* كارت المطور الملكي */
    .developer-profile {
        background: #111418; border: 1px solid #d4af37; border-radius: 25px;
        padding: 40px; margin-bottom: 40px; position: relative;
        overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .developer-profile::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 5px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
    }

    /* شبكة المشاريع (Nawy Grid) */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 25px; margin-top: 20px;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 20px;
        padding: 25px; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
    }
    .project-card:hover {
        border-color: #d4af37; transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(212, 175, 55, 0.2);
    }
    .price-label {
        background: #d4af37; color: #000; padding: 6px 15px;
        border-radius: 10px; font-weight: 900; position: absolute; left: 20px; top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* تعديل الفلاتر */
    .stSelectbox label { color: #d4af37 !important; font-weight: bold; margin-bottom: 10px; }
    div[data-baseweb="select"] { background-color: #1c2128; border-radius: 12px; border: 1px solid #d4af37; }
    </style>
""", unsafe_allow_html=True)

# 2. تحميل البيانات
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

# الهيدر السينمائي
st.markdown("""
    <div class="hero-container">
        <h1 style="font-size: 4em; font-weight: 900; color: #d4af37; letter-spacing: -1px; margin:0;">مـعـلـومـاتـي</h1>
        <p style="font-size: 1.4em; color: #ffffff; opacity: 0.9; margin-top:15px; font-weight: 300;">
            المرجع الأول والكامل لسوق العقارات المصري
        </p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # منطقة البحث (تصميم نظيف)
    st.markdown("<div style='max-width: 900px; margin: 0 auto;'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("🏗️ ابحث عن مطور", ["عرض الكل"] + sorted(df['المطور'].unique().tolist()))
    with c2: s_reg = st.selectbox("📍 اختر المنطقة", ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist()))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    if s_dev != "عرض الكل":
        # عرض بروفايل المطور بذكاء
        dev_group = df[df['المطور'] == s_dev]
        main_info = dev_group.iloc[0]
        
        st.markdown(f"""
            <div class="developer-profile">
                <h2 style="color:#d4af37; font-size: 2.5em; margin-bottom:10px;">{s_dev}</h2>
                <div style="display: flex; gap: 20px; color: #aaa; margin-bottom: 20px;">
                    <span>👤 رئيس مجلس الإدارة: <b>{main_info.get('المالك', '-')}</b></span>
                    <span>📅 تأسيس: <b>{main_info.get('تأسيس', '-')}</b></span>
                </div>
                <hr style="border-color: rgba(212,175,55,0.1);">
                <h4 style="color:#d4af37;">📜 سابقة الأعمال والنبذة التاريخية:</h4>
                <p style="font-size: 1.1em; line-height: 1.9; color: #eee; text-align: justify;">
                    {main_info.get('سابقة_الأعمال', 'التفاصيل قيد التحديث...')}
                </p>
            </div>
            <h3 style="text-align: center; color: #d4af37; margin-bottom: 30px;">🏗️ مشاريع الشركة الحالية</h3>
        """, unsafe_allow_html=True)
        
        # عرض المشاريع في شبكة
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, p in dev_group.iterrows():
            if p['المشروع'] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-label">{p.get('السعر', '-')}</div>
                        <h3 style="color:#d4af37; margin-top:40px;">{p['المشروع']}</h3>
                        <p style="margin: 15px 0;">📍 {p['المنطقة']} | 🏗️ {p.get('النوع','-')}</p>
                        <div style="background: rgba(212,175,55,0.05); padding: 10px; border-radius: 10px; font-size: 0.9em;">
                            💳 نظام السداد: {p.get('السداد','-')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث العام (شبكة مشاريع كاملة)
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-label">{row.get('السعر', '-')}</div>
                    <h3 style="color:#d4af37; margin-top:40px;">{row['المشروع']}</h3>
                    <p>🏢 {row['المطور']}</p>
                    <p style="font-size: 0.9em; opacity: 0.8;">📍 {row['المنطقة']}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ لم نتمكن من الوصول لبيانات الإكسيل. تأكد من إعدادات النشر.")
