import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# الرابط المباشر للبيانات (CSV)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# إدارة حالة تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 2. تصميم الواجهة (Premium UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp { background-color: #0d1117; font-family: 'Cairo', sans-serif; color: white; }
    
    /* تنسيق صفحة الدخول */
    .login-container {
        max-width: 450px; margin: auto; padding: 40px;
        background: #161b22; border-radius: 25px;
        border: 1px solid #d4af37; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .gold { color: #d4af37 !important; font-weight: 900; }
    
    /* تنسيق الكروت (المشاريع) */
    .project-card {
        background: linear-gradient(145deg, #1c2128, #0d1117);
        border: 1px solid #30363d; border-radius: 20px;
        padding: 30px; margin-bottom: 30px; 
        direction: rtl; text-align: right;
    }
    .project-card:hover { border-color: #d4af37; transform: scale(1.01); transition: 0.3s; }
    
    .price-tag { 
        background: #d4af37; color: black; padding: 7px 20px; 
        border-radius: 12px; font-weight: 800; float: left; font-size: 1.1em;
    }

    /* إخفاء السايد بار تماماً لجعل الصفحة صافية */
    [data-testid="stSidebar"] { display: none; }
    
    /* تنسيق حقل البحث */
    .stTextInput > div > div > input {
        background-color: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 15px !important;
        height: 55px; font-size: 1.2em; text-align: center;
    }
    .stTextInput > div > div > input:focus { border-color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        df.columns = [str(c).strip() for c in df.columns]
        df = df.astype(str).replace(['nan', 'NaN', 'None'], 'غير مدرج')
        return df
    except: return pd.DataFrame()

# --- المنطق البرمجي ---

if not st.session_state['logged_in']:
    # الصفحة الأولى: تسجيل الدخول فقط
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown(f"""
            <div style="text-align:center; margin-bottom:30px;">
                <h1 class="gold">🏠 منصة معلوماتي</h1>
                <p style="opacity:0.8;">بوابة بروكرز مصر العقارية</p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 دخول", "📝 حساب جديد"])
        
        with tab1:
            st.text_input("البريد الإلكتروني", key="user_email")
            st.text_input("كلمة المرور", type="password", key="user_pass")
            if st.button("دخول المنصة الآن", use_container_width=True):
                st.session_state['logged_in'] = True
                st.rerun()
        
        with tab2:
            st.text_input("الاسم بالكامل")
            st.text_input("رقم الموبايل")
            st.button("إنشاء حساب مجاني", use_container_width=True)

else:
    # الصفحة الثانية: المشاريع فقط
    st.markdown("<br>", unsafe_allow_html=True)
    
    # رأس الصفحة والبحث
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h2 style='text-align:center;' class='gold'>📁 قاعدة بيانات المشاريع</h2>", unsafe_allow_html=True)
        search = st.text_input("", placeholder="🔍 ابحث عن أي مطور أو مشروع أو منطقة...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    df = load_data()
    if not df.empty:
        # تصفية البيانات
        f_df = df.copy()
        if search:
            f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
        # عرض المشاريع
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', 'طلب السعر')}</div>
                    <div class="gold" style="font-size: 0.9em; letter-spacing: 1px;">PROJECT FILE</div>
                    <h2 style="margin: 10px 0;">{row.get('المشروع', '-')}</h2>
                    <div style="font-size: 1.1em; margin-bottom: 15px;">🏢 {row.get('المطور', '-')} | 📍 {row.get('المنطقة', '-')}</div>
                    
                    <div style="background: rgba(212, 175, 55, 0.05); border-right: 5px solid #d4af37; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <b class="gold" style="font-size: 1.1em;">📜 سابقة الأعمال:</b><br>
                        <span style="line-height: 1.8;">{row.get('سابقة_الأعمال', 'لا توجد بيانات مسجلة')}</span>
                    </div>
                    
                    <div style="display: flex; gap: 50px; font-size: 1em; border-top: 1px solid #30363d; padding-top: 20px;">
                        <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                        <div><span class="gold">💳 نظام السداد:</span> {row.get('السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # زر خروج هادئ في الأسفل
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("تسجيل الخروج", use_container_width=False):
            st.session_state['logged_in'] = False
            st.rerun()
    else:
        st.info("🔄 جاري مزامنة المشاريع...")
