import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# الرابط المباشر للبيانات
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# إدارة حالة الدخول
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# 2. تصميم الواجهة الاحترافي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    
    /* إخفاء السايد بار لزيادة التركيز */
    [data-testid="stSidebar"] { display: none; }

    /* تنسيق صفحة الدخول */
    .login-card {
        background: #161b22;
        border: 2px solid #d4af37;
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        margin-top: 100px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }

    /* تنسيق كروت المشاريع */
    .project-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-3px); transition: 0.3s; }
    
    .price-badge { 
        background: #d4af37; color: #000; padding: 5px 15px; 
        border-radius: 8px; font-weight: 900; font-size: 1.1em; float: left;
    }

    .gold { color: #d4af37 !important; }
    
    .info-section {
        background: rgba(212, 175, 55, 0.05);
        border-right: 4px solid #d4af37;
        padding: 15px;
        margin: 15px 0;
        border-radius: 4px 10px 10px 4px;
        line-height: 1.6;
    }
    
    /* تنسيق محرك البحث */
    .stTextInput > div > div > input {
        background-color: #161b22 !important;
        color: white !important;
        border: 2px solid #30363d !important;
        border-radius: 12px !important;
        height: 50px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def get_data():
    try:
        r = requests.get(CSV_URL)
        r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except: return pd.DataFrame()

# --- الصفحات ---

if not st.session_state['authenticated']:
    # صفحة الدخول (Login Page)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with col2 := c2:
        st.markdown("""
            <div class="login-card">
                <h1 class="gold">منصة معلوماتي</h1>
                <p>بوابة بروكرز مصر العقارية - الإصدار الاحترافي</p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 دخول", "✍️ تسجيل"])
        with tab1:
            st.text_input("اسم المستخدم")
            st.text_input("كلمة المرور", type="password")
            if st.button("دخول للمنصة", use_container_width=True):
                st.session_state['authenticated'] = True
                st.rerun()
        with tab2:
            st.text_input("الاسم")
            st.text_input("الموبايل")
            st.button("إنشاء حساب مجاني", use_container_width=True)
else:
    # الصفحة الرئيسية (المشاريع فقط)
    st.markdown("<h2 class='gold' style='text-align:center;'>🏠 قاعدة بيانات المشاريع</h2>", unsafe_allow_html=True)
    
    # محرك البحث
    s1, s2, s3 = st.columns([1, 2, 1])
    with s2:
        search_query = st.text_input("", placeholder="🔍 ابحث عن المطور، المنطقة، أو اسم المشروع...")

    data = get_data()
    if not data.empty:
        # تصفية
        if search_query:
            data = data[data.apply(lambda r: search_query.lower() in str(r).lower(), axis=1)]
        
        st.write(f"تم إيجاد {len(data)} مشروع")

        # عرض الكروت بشكل احترافي
        for _, row in data.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{row.get('السعر', 'اتصل')}</div>
                    <div class="gold" style="font-size: 0.8em; font-weight: bold;">PROJECT REPORT</div>
                    <h2 style="margin: 10px 0;">{row.get('المشروع', '-')}</h2>
                    <p style="font-size: 1.1em; opacity: 0.9;">📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                    
                    <div class="info-section">
                        <b class="gold">📜 سابقة الأعمال والخبرة:</b><br>
                        {row.get('سابقة_الأعمال', 'لا توجد بيانات')}
                    </div>
                    
                    <div style="display: flex; gap: 40px; border-top: 1px solid #30363d; padding-top: 15px; font-size: 0.9em;">
                        <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                        <div><span class="gold">💳 نظام السداد:</span> {row.get('السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("تسجيل الخروج"):
            st.session_state['authenticated'] = False
            st.rerun()
    else:
        st.warning("🔄 لا توجد بيانات متاحة حالياً.")
