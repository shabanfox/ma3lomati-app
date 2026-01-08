import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة (يجب أن يظل أول سطر)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS) - نقل شريط التمرير لليسار + التصميم المودرن
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* --- خدعة نقل شريط التمرير لليسار --- */
    html {
        direction: ltr !important; /* نقل كل شيء لليسار بما في ذلك السكرول */
    }
    body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; /* إعادة الكلام والمحتوى لليمين مرة أخرى */
        font-family: 'Cairo', sans-serif;
        background-color: #0d1117;
        color: white;
    }
    
    [data-testid="stSidebar"] { display: none; }
    
    /* --- تخصيص شكل شريط التمرير (الآن في اليسار) --- */
    ::-webkit-scrollbar { width: 22px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { 
        background: #d4af37 !important; 
        border-radius: 10px; 
        border: 4px solid #161b22; 
    }

    /* الهيدر المودرن المتحرك */
    .hero-section {
        position: relative;
        height: 300px;
        overflow: hidden;
        border-radius: 25px;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .hero-bg {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        z-index: 1;
        animation: kenburns 20s infinite alternate;
    }
    .hero-overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(to bottom, rgba(13,17,23,0.2), rgba(13,17,23,0.8));
        z-index: 2;
    }
    .hero-content { position: relative; z-index: 3; text-align: center; }
    .gold-title { color: #d4af37; font-size: 3em; font-weight: 900; margin: 0; }

    @keyframes kenburns {
        0% { transform: scale(1); }
        100% { transform: scale(1.1); }
    }

    /* تنسيق الكروت والفلاتر */
    .stTextInput > div > div > input {
        background-color: #1c2128 !important; color: white !important;
        border: 1px solid #d4af37 !important; border-radius: 12px !important;
        text-align: center;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 20px;
        padding: 25px; margin-bottom: 20px; transition: 0.3s;
        text-align: right;
    }
    .project-card:hover { border-color: #d4af37; }
    .price-badge { background: #d4af37; color: black; padding: 5px 15px; border-radius: 8px; font-weight: bold; float: left; }
    </style>
    
    <div class="hero-section">
        <div class="hero-bg"></div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 class="gold-title">منصة معلوماتي العقارية</h1>
            <p style="font-size: 1.1em;">دليلك العقاري الأسرع في مصر</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. دالة جلب البيانات
@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(PROJECTS_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("غير مدرج").astype(str)
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # 5. ثلاث خانات بحث
    c1, c2, c3 = st.columns(3)
    with c1: s_region = st.text_input("📍 تصفية بالمنطقة")
    with c2: s_price = st.text_input("💰 تصفية بالسعر")
    with c3: s_type = st.text_input("🏗️ نوع الوحدة")

    # منطق الفلترة
    f_df = df.copy()
    if s_region: f_df = f_df[f_df['المنطقة'].str.contains(s_region, case=False)]
    if s_price: f_df = f_df[f_df['السعر'].str.contains(s_price, case=False)]
    if s_type:
        col = 'النوع' if 'النوع' in f_df.columns else f_df.columns[0]
        f_df = f_df[f_df[col].str.contains(s_type, case=False)]

    st.markdown(f"**عدد المشاريع: {len(f_df)}**")

    # 6. عرض النتائج
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">{row.get('السعر', '-')}</div>
                <h3 style="color:#d4af37; margin:0;">{row.get('المشروع', '-')}</h3>
                <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                <div style="background:rgba(212,175,55,0.05); padding:10px; border-right:3px solid #d4af37; border-radius:5px;">
                    <small><b>الوصف:</b> {row.get('سابقة_الأعمال', '-')}</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("جاري التحميل...")
