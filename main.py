import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة (إخفاء كل زوائد ستريمليت لتبدو كمنصة مستقلة)
st.set_page_config(page_title="معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والقوائم تماماً */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #f8f9fa; color: #1a1a1a;
    }

    /* هيدر ناوي (أبيض فخم مع لوجو ذهبي) */
    .nawy-header {
        background: #ffffff; padding: 20px; text-align: center;
        border-bottom: 1px solid #e0e0e0; margin-bottom: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* كارت المطور (Profile Card) */
    .dev-profile {
        background: #ffffff; border-radius: 16px; padding: 30px;
        margin-bottom: 30px; border: 1px solid #e0e0e0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .dev-title { color: #c49a6c; font-weight: 900; font-size: 2.2em; margin-bottom: 10px; }

    /* شبكة المشاريع (Nawy Grid) */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 25px;
    }
    .project-card {
        background: #ffffff; border-radius: 12px; overflow: hidden;
        border: 1px solid #eee; transition: 0.3s; position: relative;
    }
    .project-card:hover { transform: translateY(-8px); box-shadow: 0 12px 30px rgba(0,0,0,0.12); }
    
    .card-content { padding: 20px; }
    .price-tag {
        color: #c49a6c; font-weight: 700; font-size: 1.2em; margin-bottom: 8px;
    }
    .project-name { font-weight: 700; font-size: 1.3em; margin-bottom: 5px; }
    .location-tag { color: #666; font-size: 0.9em; display: flex; align-items: center; gap: 5px; }
    
    /* الفلاتر */
    .filter-section {
        background: #ffffff; padding: 20px; border-radius: 12px;
        margin-bottom: 30px; border: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
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

# الهيدر العلوي
st.markdown("""
    <div class="nawy-header">
        <h1 style="color: #1a1a1a; margin:0; font-weight:900; letter-spacing:-1px;">معلوماتي <span style="color:#c49a6c;">العقارية</span></h1>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # الفلاتر بتصميم نظيف
    with st.container():
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: s_dev = st.selectbox("🏢 المطور العقاري", ["عرض كل المطورين"] + sorted(df['المطور'].unique().tolist()))
        with c2: s_reg = st.selectbox("📍 المنطقة", ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist()))
        st.markdown('</div>', unsafe_allow_html=True)

    if s_dev != "عرض كل المطورين":
        dev_rows = df[df['المطور'] == s_dev]
        main = dev_rows.iloc[0]
        
        # بروفايل المطور
        st.markdown(f"""
            <div class="dev-profile">
                <div class="dev-title">{s_dev}</div>
                <div style="color:#555; margin-bottom:15px;"><b>رئيس مجلس الإدارة:</b> {main.get('المالك', '-')}</div>
                <div style="background:#fcf8f3; padding:20px; border-radius:8px; color:#444; line-height:1.8;">
                    <b>عن الشركة:</b><br>{main.get('سابقة_الأعمال', '-')}
                </div>
            </div>
            <h3 style="margin-bottom:20px;">مشاريع {s_dev}</h3>
        """, unsafe_allow_html=True)
        
        # شبكة مشاريع المطور
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in dev_rows.iterrows():
            if r['المشروع'] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="card-content">
                            <div class="price-tag">{r.get('السعر', 'اتصل بنا')}</div>
                            <div class="project-name">{r['المشروع']}</div>
                            <div class="location-tag">📍 {r['المنطقة']}</div>
                            <hr style="margin:15px 0; opacity:0.1;">
                            <div style="font-size:0.85em; color:#888;">نظام السداد: {r.get('السداد','-')}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="card-content">
                        <div class="price-tag">{r.get('السعر', 'اتصل بنا')}</div>
                        <div class="project-name">{r['المشروع']}</div>
                        <div style="font-weight:600; color:#c49a6c; margin-bottom:5px;">{r['المطور']}</div>
                        <div class="location-tag">📍 {r['المنطقة']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("جاري مزامنة البيانات من جوجل شيت...")
