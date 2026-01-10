import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS - التوسيط الاحترافي الفاخر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء العناصر الافتراضية لستريمليت */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* تنسيق الخلفية العامة */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #121212; /* خلفية داكنة جداً للفخامة */
    }

    /* حاوية التوسيط المطلق */
    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    /* المربع الأسود المركزي */
    .login-box {
        background: #000000;
        padding: 50px 40px;
        border-radius: 35px;
        border: 4px solid #f59e0b;
        box-shadow: 0px 0px 60px rgba(245, 158, 11, 0.15);
        text-align: center;
        width: 100%;
        max-width: 450px;
    }

    /* كلمة معلوماتى العقارية داخل المربع */
    .login-box h1 {
        color: #f59e0b;
        font-weight: 900;
        font-size: 2.8rem;
        margin-bottom: 5px;
        line-height: 1.2;
    }

    .login-box p {
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 35px;
        opacity: 0.8;
    }

    /* ستايل زر الخروج الثابت (أعلى اليمين بعد الدخول) */
    .logout-container {
        position: fixed;
        top: 25px;
        right: 25px;
        z-index: 9999;
    }

    /* ستايل حقل إدخال كلمة المرور */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #333 !important;
        border-radius: 15px !important;
        text-align: center;
        font-size: 1.2rem !important;
        height: 55px !important;
        margin-bottom: 10px;
    }
    .stTextInput input:focus {
        border-color: #f59e0b !important;
        box-shadow: 0px 0px 10px rgba(245, 158, 11, 0.3) !important;
    }

    /* ستايل زر الدخول */
    div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 15px !important;
        width: 100% !important;
        height: 55px !important;
        font-size: 1.3rem !important;
        transition: 0.4s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 10px 20px rgba(245, 158, 11, 0.3) !important;
    }

    /* تنسيق المحتوى الداخلي (الهيدر) */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 3px solid #f59e0b;
        margin-top: 100px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام تسجيل الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    # الصندوق الأسود في منتصف الصفحة
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 4rem; margin-bottom: 10px;">🏠</div>', unsafe_allow_html=True)
    st.markdown('<h1>معلوماتى العقارية</h1>', unsafe_allow_html=True)
    st.markdown('<p>نظام الدخول الآمن للمستشارين</p>', unsafe_allow_html=True)
    
    # حقل الإدخال بدون عنوان (Label) لتوفير المساحة
    pwd = st.text_input("كلمة المرور", type="password", key="login_pass", label_visibility="collapsed", placeholder="أدخل كلمة المرور هنا")
    
    if st.button("دخول للمنصة"):
        if pwd == "Ma3lomati_2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    
    st.markdown('</div>', unsafe_allow_html=True)

# فحص حالة المستخدم
if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- 4. محتوى المنصة (يظهر بعد الدخول بنجاح) ---

# زر الخروج الثابت في الزاوية
st.markdown('<div class="logout-container">', unsafe_allow_html=True)
if st.button("🔒 تسجيل الخروج", key="logout_btn"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# الهيدر الرئيسي
st.markdown('<div class="hero-banner"><h1>🏠 أهلاً بك في منصة معلوماتى</h1><p>دليلك الشامل للمطورين وأدوات السوق العقاري</p></div>', unsafe_allow_html=True)

# أزرار الأقسام
col1, col2 = st.columns(2)
with col1:
    if st.button("🏢 دليل المطورين العقاريين", use_container_width=True):
        st.info("جاري الانتقال لدليل المطورين...")
with col2:
    if st.button("🛠️ الأدوات والحاسبات الذكية", use_container_width=True):
        st.info("جاري فتح الأدوات...")
