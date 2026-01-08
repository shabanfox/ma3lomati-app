import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# الرابط المباشر للبيانات
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# إدارة حالة تسجيل الدخول
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# 2. تصميم الواجهة (Premium CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0b0e14; color: white; }
    
    /* إخفاء القائمة الجانبية تماماً */
    [data-testid="stSidebar"] { display: none; }

    /* حاوية تسجيل الدخول */
    .login-container {
        background: #161b22;
        border: 2px solid #d4af37;
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
    }

    .gold { color: #d4af37 !important; font-weight: 900; }
    
    /* كروت المشاريع */
    .project-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-5px); transition: 0.3s; }
    
    .price-tag { 
        background: #d4af37; color: black; padding: 5px 15px; 
        border-radius: 8px; font-weight: 800; float: left;
    }

    .info-box {
        background: rgba(212, 175, 55, 0.05);
        border-right: 4px solid #d4af37;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }

    /* جعل حقل البحث احترافي وفي المنتصف */
    .stTextInput > div > div > input {
        background-color: #161b22 !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 12px !important;
        height: 50px; text-align: center; font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=10)
def load_sheet_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except:
        return pd.DataFrame()

# --- التحكم في عرض الصفحات ---

if not st.session_state['auth']:
    # صفحة تسجيل الدخول المنفصلة تماماً
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    
    with c2:
        st.markdown("""
            <div class="login-container">
                <h1 class="gold">منصة معلوماتي</h1>
                <p style="opacity:0.8;">بوابة بروكرز مصر العقارية</p>
            </div>
        """, unsafe_allow_html=True)
        
        choice = st.tabs(["🔐 تسجيل الدخول", "✉️ إنشاء حساب"])
        
        with choice[0]:
            st.text_input("اسم المستخدم أو الإيميل")
            st.text_input("كلمة المرور", type="password")
            if st.button("دخول للمنصة الآن", use_container_width=True):
                st.session_state['auth'] = True
                st.rerun()
        
        with choice[1]:
            st.text_input("الاسم بالكامل")
            st.text_input("رقم الموبايل")
            st.button("تسجيل حساب مجاني", use_container_width=True)

else:
    # الصفحة الرئيسية (قاعدة بيانات المشاريع)
    st.markdown("<h2 class='gold' style='text-align:center; margin-top:20px;'>🏠 قاعدة بيانات المشاريع</h2>", unsafe_allow_html=True)
    
    # محرك البحث في المنتصف
    s1, s2, s3 = st.columns([1, 2, 1])
    with s2:
        search = st.text_input("", placeholder="🔍 ابحث عن المطور، المنطقة، أو اسم المشروع...")

    df = load_sheet_data()
    
    if not df.empty:
        # فلترة النتائج
        if search:
            df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
        st.markdown(f"<p style='text-align:center; opacity:0.7;'>تم إيجاد {len(df)} مشروع متاح</p>", unsafe_allow_html=True)

        # عرض الكروت
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', 'اتصل')}</div>
                    <div class="gold" style="font-size: 0.8em; font-weight: bold;">PROJECT REPORT</div>
                    <h2 style="margin: 5px 0;">{row.get('المشروع', '-')}</h2>
                    <p style="font-size: 1.1em; opacity: 0.9;">📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                    
                    <div class="info-box">
                        <b class="gold">📜 سابقة الأعمال والخبرة:</b><br>
                        {row.get('سابقة_الأعمال', 'لا توجد بيانات')}
                    </div>
                    
                    <div style="display: flex; gap: 40px; border-top: 1px solid #30363d; padding-top: 15px; font-size: 0.9em;">
                        <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                        <div><span class="gold">💳 نظام السداد:</span> {row.get('السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # زر خروج
        if st.button("تسجيل الخروج"):
            st.session_state['auth'] = False
            st.rerun()
    else:
        st.info("🔄 جاري تحميل البيانات...")
