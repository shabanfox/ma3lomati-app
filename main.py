import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة (يجب أن يكون السطر الأول)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# رابط البيانات المباشر
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# إدارة جلسة الدخول
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# 2. هندسة الديكور والتنسيق (Premium CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0b0e14; color: white; }
    
    /* إخفاء القائمة الجانبية في صفحة الدخول */
    [data-testid="stSidebar"] { display: none; }

    /* حاوية صفحة الدخول */
    .login-frame {
        background: #161b22;
        border: 2px solid #d4af37;
        border-radius: 30px;
        padding: 50px;
        margin-top: 50px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.7);
        text-align: center;
    }

    .gold-title { color: #d4af37 !important; font-weight: 900; font-size: 2.5em; margin-bottom: 10px; }
    
    /* تصميم كروت المشاريع */
    .project-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        transition: 0.4s;
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-5px); }
    
    .price-tag { 
        background: #d4af37; color: #000; padding: 5px 20px; 
        border-radius: 10px; font-weight: 800; font-size: 1.2em; float: left;
    }

    .details-box {
        background: rgba(212, 175, 55, 0.05);
        border-right: 5px solid #d4af37;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=10)
def fetch_data():
    try:
        res = requests.get(CSV_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except: return pd.DataFrame()

# --- منطق عرض الصفحات ---

if not st.session_state['auth']:
    # صفحة تسجيل الدخول المستقلة
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
            <div class="login-frame">
                <div class="gold-title">منصة معلوماتي</div>
                <p style="font-size: 1.2em; opacity: 0.8;">بوابة بروكرز مصر العقارية</p>
                <hr style="border-color: #d4af37; margin: 20px 0;">
            </div>
        """, unsafe_allow_html=True)
        
        mode = st.radio("", ["تسجيل الدخول", "إنشاء حساب جديد"], horizontal=True)
        
        if mode == "تسجيل الدخول":
            st.text_input("اسم المستخدم أو الإيميل")
            st.text_input("كلمة المرور", type="password")
            if st.button("دخول المنصة الآمنة", use_container_width=True):
                st.session_state['auth'] = True
                st.rerun()
        else:
            st.text_input("الاسم بالكامل")
            st.text_input("رقم الهاتف (واتساب)")
            st.button("تقديم طلب انضمام مجاني", use_container_width=True)

else:
    # صفحة المشاريع (تظهر فقط بعد الدخول)
    st.markdown("<h1 class='gold-title' style='text-align:center;'>🏠 قاعدة بيانات المشاريع</h1>", unsafe_allow_html=True)
    
    # محرك البحث في المنتصف
    s1, s2, s3 = st.columns([1, 2, 1])
    with s2:
        search = st.text_input("", placeholder="🔍 ابحث عن مطور، منطقة، أو اسم مشروع...")

    df = fetch_data()
    if not df.empty:
        # فلترة
        f_df = df.copy()
        if search:
            f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
        st.write(f"تم إيجاد {len(f_df)} مشروع")

        # عرض الكروت
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', 'اتصل')}</div>
                    <div style="color: #d4af37; font-size: 0.9em; font-weight: bold;">PROJECT REPORT</div>
                    <h2 style="margin: 5px 0;">{row.get('المشروع', '-')}</h2>
                    <p style="font-size: 1.1em; opacity: 0.9;">📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                    
                    <div class="details-box">
                        <b style="color: #d4af37;">📜 سابقة الأعمال والخبرة:</b><br>
                        {row.get('سابقة_الأعمال', 'لا توجد بيانات')}
                    </div>
                    
                    <div style="display: flex; gap: 40px; border-top: 1px solid #333; padding-top: 15px; font-size: 0.9em;">
                        <div><span style="color: #d4af37;">👤 المالك:</span> {row.get('المالك', '-')}</div>
                        <div><span style="color: #d4af37;">💳 نظام السداد:</span> {row.get('السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("تسجيل الخروج"):
            st.session_state['auth'] = False
            st.rerun()
