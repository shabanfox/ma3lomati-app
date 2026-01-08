import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة (نفس الروح القديمة)
st.set_page_config(page_title="منصة معلوماتي", layout="wide")

# 2. رابط الشيت بتاعك
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

# 3. الـ CSS الأصلي اللي إنت اخترته (نضيف، فخم، ومريح للعين)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #0d1117; color: white;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1c2128; border-radius: 10px; color: #d4af37; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #d4af37 !important; color: black !important; }
    .project-card {
        background: #1c2128; border-right: 5px solid #d4af37;
        padding: 20px; border-radius: 10px; margin-bottom: 15px;
    }
    label { color: #d4af37 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. جلب الداتا بتنظيف آلي
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns] # تنظيف أسماء الأعمدة
        return df.fillna("-").astype(str)
    except:
        return pd.DataFrame()

df = load_data()

st.markdown("<h1 style='text-align:center; color:#d4af37;'>🏢 موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)

if not df.empty:
    # تحديد الأعمدة الأساسية
    C_DEV = "المطور" if "المطور" in df.columns else df.columns[1]
    C_PROJ = "المشروع" if "المشروع" in df.columns else df.columns[0]
    C_REG = "المنطقة" if "المنطقة" in df.columns else df.columns[2]
    
    # الفلاتر في الأعلى بشكل منظم
    col1, col2 = st.columns(2)
    with col1:
        s_reg = st.selectbox("📍 اختار المنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))
    with col2:
        s_dev = st.selectbox("🏢 اختار المطور", ["كل المطورين"] + sorted(df[C_DEV].unique().tolist()))

    st.markdown("---")

    if s_dev != "كل المطورين":
        # عرض "بروفايل المطور" بالتبويبات
        dev_row = df[df[C_DEV] == s_dev].iloc[0]
        
        tab_info, tab_projects = st.tabs(["ℹ️ معلومات الشركة والمالك", "🏗️ مشاريع الشركة"])
        
        with tab_info:
            st.markdown(f"""
                <div style="background:#1c2128; padding:25px; border-radius:15px; border:1px solid #d4af37;">
                    <h3 style="color:#d4af37;">👤 المالك / الإدارة</h3>
                    <p style="font-size:1.2em;">{dev_row.get('المالك', 'غير مدرج')}</p>
                    <hr style="opacity:0.2;">
                    <h3 style="color:#d4af37;">📜 سابقة الأعمال</h3>
                    <p style="line-height:1.8;">{dev_row.get('سابقة_الأعمال', 'لا توجد تفاصيل حالياً.')}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with tab_projects:
            dev_projs = df[df[C_DEV] == s_dev]
            for _, row in dev_projs.iterrows():
                st.markdown(f"""
                    <div class="project-card">
                        <h3 style="margin:0; color:#d4af37;">{row[C_PROJ]}</h3>
                        <p style="margin:5px 0;">📍 {row[C_REG]} | 🏗️ {row.get('النوع','-')}</p>
                        <p style="font-size:0.9em; opacity:0.8;">💳 نظام السداد: {row.get('السداد','-')}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <h3 style="margin:0; color:#d4af37;">{row[C_PROJ]}</h3>
                    <p style="margin:5px 0;">🏢 {row[C_DEV]} | 📍 {row[C_REG]}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("تأكد من ترتيب الأعمدة في الشيت: المشروع، المطور، المنطقة، المالك، سابقة_الأعمال")
