import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة (يجب أن يظل أول سطر)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS) - الهيدر المتحرك وشريط التمرير
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    [data-testid="stSidebar"] { display: none; }
    
    /* شريط التمرير الذهبي العريض */
    ::-webkit-scrollbar { width: 22px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; border: 4px solid #161b22; }

    /* الهيدر المودرن المتحرك */
    .hero-section {
        position: relative;
        height: 350px;
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
        background-image: url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        z-index: 1;
        animation: kenburns 20s infinite alternate;
    }
    .hero-overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(to bottom, rgba(13,17,23,0.3), rgba(13,17,23,0.9));
        z-index: 2;
    }
    .hero-content {
        position: relative;
        z-index: 3;
        text-align: center;
    }
    .gold-title {
        color: #d4af37;
        font-size: 3.5em;
        font-weight: 900;
        text-shadow: 2px 2px 15px rgba(0,0,0,0.8);
        margin: 0;
    }

    @keyframes kenburns {
        0% { transform: scale(1); }
        100% { transform: scale(1.2); }
    }

    /* تنسيق الكروت والفلاتر */
    .stTextInput > div > div > input {
        background-color: #1c2128 !important; color: white !important;
        border: 1px solid #d4af37 !important; border-radius: 12px !important;
        height: 50px; text-align: center; font-size: 1.1em;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 20px;
        padding: 30px; margin-bottom: 25px; transition: 0.3s;
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-5px); }
    .price-badge { background: #d4af37; color: black; padding: 5px 15px; border-radius: 8px; font-weight: bold; float: left; }
    .gold { color: #d4af37; font-weight: bold; }
    </style>
    
    <div class="hero-section">
        <div class="hero-bg"></div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 class="gold-title">منصة معلوماتي العقارية</h1>
            <p style="font-size: 1.2em; text-shadow: 1px 1px 5px black;">دليلك الذكي للمشروعات والمطورين في مصر</p>
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
    st.markdown("<h3 style='text-align:center;'>🔍 ابحث عن عقارك المفضل</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: s_region = st.text_input("📍 المنطقة", placeholder="مثال: التجمع / زايد")
    with c2: s_price = st.text_input("💰 السعر", placeholder="مثال: 5,000,000")
    with c3: s_type = st.text_input("🏗️ نوع الوحدة", placeholder="مثال: سكني / تجاري")

    # منطق الفلترة
    f_df = df.copy()
    if s_region: f_df = f_df[f_df['المنطقة'].str.contains(s_region, case=False)]
    if s_price: f_df = f_df[f_df['السعر'].str.contains(s_price, case=False)]
    if s_type:
        col_to_search = 'النوع' if 'النوع' in f_df.columns else f_df.columns[0]
        f_df = f_df[f_df[col_to_search].str.contains(s_type, case=False)]

    st.markdown(f"<p style='opacity:0.6;'>تم إيجاد {len(f_df)} مشروع</p>", unsafe_allow_html=True)

    # 6. عرض النتائج
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">{row.get('السعر', '-')}</div>
                <h2 style="color:#d4af37; margin-top:0;">{row.get('المشروع', '-')}</h2>
                <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                <div style="background:rgba(212,175,55,0.05); padding:15px; border-right:4px solid #d4af37; border-radius:5px;">
                    <span class="gold">📜 التفاصيل:</span> {row.get('سابقة_الأعمال', '-')}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("جاري مزامنة البيانات...")
