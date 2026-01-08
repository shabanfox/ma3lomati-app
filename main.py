import streamlit as st
import pandas as pd
import requests
from io import StringIO
import re

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    #MainMenu, header, footer, .stDeployButton {visibility: hidden;}
    html { direction: ltr !important; }
    body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
        background-color: #0d1117; color: white;
    }
    ::-webkit-scrollbar { width: 14px !important; }
    ::-webkit-scrollbar-track { background: #0d1117 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 20px; }
    
    .hero-section {
        position: relative; height: 250px; border-radius: 30px; margin-bottom: 40px;
        display: flex; align-items: center; justify-content: center; overflow: hidden;
    }
    .hero-bg {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1600&q=80');
        background-size: cover; z-index: 1; animation: kenburns 15s infinite alternate;
    }
    .hero-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(13,17,23,0.7); z-index: 2; }
    .main-title { color: #d4af37; font-size: 3em; font-weight: 900; z-index: 3; position: relative; }
    
    .project-card {
        background: rgba(28, 33, 40, 0.9); border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px; padding: 25px; margin-bottom: 25px; transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); border-color: #d4af37; }
    .price-badge { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 10px; font-weight: 900; float: left; }
    </style>
    
    <div class="hero-section">
        <div class="hero-bg"></div>
        <div class="hero-overlay"></div>
        <h1 class="main-title">منصة معلوماتي</h1>
    </div>
    """, unsafe_allow_html=True)

# 4. جلب ومعالجة البيانات
@st.cache_data(ttl=5)
def load_and_clean_data():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text)).fillna("غير مدرج").astype(str)
        df.columns = [str(c).strip() for c in df.columns]
        
        # استخراج المناطق الفريدة بشكل ذكي
        all_regions = []
        for reg in df['المنطقة'].unique():
            # تقسيم الاسم لو فيه (و، أو، فواصل، أو علامات)
            parts = re.split(r'[،و\-]|أو', reg)
            for p in parts:
                clean_p = p.strip()
                if clean_p and clean_p != "غير مدرج":
                    all_regions.append(clean_p)
        
        unique_regions = ["كل المناطق"] + sorted(list(set(all_regions)))
        return df, unique_regions
    except: return pd.DataFrame(), ["كل المناطق"]

df, regions_options = load_and_clean_data()

if not df.empty:
    c1, c2, c3 = st.columns(3)
    with c1:
        s_reg = st.selectbox("📍 اختر المنطقة", options=regions_options)
    with c2:
        s_pri = st.text_input("💰 ميزانية السعر")
    with c3:
        s_typ = st.text_input("🏗️ نوع الوحدة")

    # منطق الفلترة المطور
    f_df = df.copy()
    if s_reg != "كل المناطق":
        # البحث عن المنطقة المختارة داخل نص عمود المنطقة (عشان لو مكتوب "التجمع وزايد" تظهر في الاتنين)
        f_df = f_df[f_df['المنطقة'].str.contains(s_reg, case=False)]
    
    if s_pri: f_df = f_df[f_df['السعر'].str.contains(s_pri, case=False)]
    if s_typ:
        col = 'النوع' if 'النوع' in f_df.columns else f_df.columns[0]
        f_df = f_df[f_df[col].str.contains(s_typ, case=False)]

    st.markdown(f"**النتائج: {len(f_df)}**")

    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">{row.get('السعر', '-')}</div>
                <h2 style="color:#d4af37; margin-bottom:10px;">{row.get('المشروع', '-')}</h2>
                <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                <div style="background:rgba(212,175,55,0.05); padding:15px; border-right:4px solid #d4af37; border-radius:10px;">
                    {row.get('سابقة_الأعمال', '-')}
                </div>
            </div>
        """, unsafe_allow_html=True)
