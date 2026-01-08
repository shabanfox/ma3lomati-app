import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS) - إخفاء عناصر Streamlit ونقل السكرول لليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء زر GitHub والقائمة العلوية وعلامة Deploy */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    /* نقل شريط التمرير لليسار */
    html { direction: ltr !important; }
    body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
        background-color: #0d1117;
        color: white;
    }
    
    /* شكل شريط التمرير في اليسار */
    ::-webkit-scrollbar { width: 18px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { 
        background: #d4af37 !important; 
        border-radius: 10px; 
    }

    /* الهيدر المودرن */
    .hero-section {
        position: relative; height: 250px; overflow: hidden;
        border-radius: 25px; margin-bottom: 30px;
        display: flex; align-items: center; justify-content: center;
    }
    .hero-bg {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1600&q=80');
        background-size: cover; background-position: center;
        animation: kenburns 20s infinite alternate; z-index: 1;
    }
    .hero-overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(13,17,23,0.6); z-index: 2;
    }
    .hero-content { position: relative; z-index: 3; text-align: center; }
    
    @keyframes kenburns { 0% {transform: scale(1);} 100% {transform: scale(1.1);} }

    /* الكروت */
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 20px; margin-bottom: 20px; text-align: right;
    }
    .price-badge { background: #d4af37; color: black; padding: 4px 12px; border-radius: 6px; font-weight: bold; float: left; }
    </style>
    
    <div class="hero-section">
        <div class="hero-bg"></div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 style="color:#d4af37; font-size:2.5em; margin:0;">منصة معلوماتي العقارية</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. جلب البيانات وعرضها
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        return pd.read_csv(StringIO(res.text)).fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()
if not df.empty:
    c1, c2, c3 = st.columns(3)
    with c1: s_reg = st.text_input("📍 المنطقة")
    with c2: s_pri = st.text_input("💰 السعر")
    with c3: s_typ = st.text_input("🏗️ النوع")

    f_df = df.copy()
    # فلترة سريعة
    if s_reg: f_df = f_df[f_df.iloc[:, 1].str.contains(s_reg, case=False)] # بافتراض العمود 2 هو المنطقة
    
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">{row.get('السعر', '-')}</div>
                <h3 style="color:#d4af37; margin:0;">{row.get('المشروع', '-')}</h3>
                <p>🏢 {row.get('المطور', '-')} | 📍 {row.get('المنطقة', '-')}</p>
            </div>
        """, unsafe_allow_html=True)
