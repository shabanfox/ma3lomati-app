import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة وإخفاء كل شيء (Clean UI)
st.set_page_config(page_title="معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والقوائم */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #0d1117; color: #ffffff;
    }

    /* هيدر احترافي بخلفية متحركة */
    .hero-section {
        background: linear-gradient(-45deg, #0d1117, #1c2128, #2d240a, #0d1117);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        padding: 80px 20px; text-align: center;
        border-bottom: 2px solid #d4af37; border-radius: 0 0 50px 50px;
        margin-bottom: 40px;
    }
    @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    /* كارت المطور (مرة واحدة فقط) */
    .dev-main-card {
        background: #1c2128; border: 1px solid #d4af37; border-radius: 20px;
        padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* شبكة المشاريع (Grid) */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 20px; margin-top: 20px;
    }
    .project-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 15px;
        padding: 20px; position: relative; transition: 0.3s;
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-5px); }
    .price-tag {
        background: #d4af37; color: #000; padding: 5px 12px;
        border-radius: 8px; font-weight: 900; position: absolute; left: 15px; top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

@st.cache_data(ttl=2)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3.5em; font-weight: 900; color: #d4af37; margin:0;">مـعـلـومـاتـي</h1>
        <p style="font-size: 1.2em; opacity: 0.8;">دليل مطوري العقارات في مصر</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # الفلاتر
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("🏢 اختر المطور", ["كل المطورين"] + sorted(df['المطور'].unique().tolist()))
    with c2: s_reg = st.selectbox("📍 اختر المنطقة", ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist()))

    if s_dev != "كل المطورين":
        # عرض بيانات المطور مرة واحدة فقط
        dev_data = df[df['المطور'] == s_dev]
        first = dev_data.iloc[0]
        
        st.markdown(f"""
            <div class="dev-main-card">
                <h2 style="color:#d4af37;">{s_dev}</h2>
                <p><b>👤 المالك:</b> {first.get('المالك', '-')}</p>
                <hr style="opacity:0.1;">
                <h4 style="color:#d4af37;">📜 سابقة الأعمال:</h4>
                <p style="line-height:1.7;">{first.get('سابقة_الأعمال', '-')}</p>
            </div>
            <h3 style="text-align:center; color:#d4af37; margin:30px 0;">🏗️ مشاريع {s_dev}</h3>
        """, unsafe_allow_html=True)

        # عرض مشاريع المطور في شبكة
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, row in dev_data.iterrows():
            if row['المشروع'] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-tag">{row.get('السعر', '-')}</div>
                        <h4 style="margin-top:30px; color:#d4af37;">{row['المشروع']}</h4>
                        <p style="font-size:0.9em; opacity:0.8;">📍 {row['المنطقة']} | 🏗️ {row.get('النوع','-')}</p>
                        <p style="font-size:0.8em; color:#aaa;">💳 السداد: {row.get('السداد','-')}</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث العام (شبكة لكل المشاريع)
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', '-')}</div>
                    <h4 style="margin-top:30px; color:#d4af37;">{row['المشروع']}</h4>
                    <p style="font-size:0.9em; opacity:0.8;">🏢 {row['المطور']} | 📍 {row['المنطقة']}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
