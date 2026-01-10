import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS - جعل الكارت في القمة تماماً بدون فراغات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء العناصر الافتراضية تماماً */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* تصفير الهوامش الافتراضية للمتصفح وStreamlit */
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child {
        padding-top: 0rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff;
        margin: 0 !important; padding: 0 !important;
    }

    /* حاوية الدخول ملتصقة بالسقف */
    .top-zero-wrapper {
        display: flex;
        justify-content: center;
        align-items: flex-start; /* المحاذاة للأعلى */
        width: 100%;
        margin: 0 !important;
    }

    .login-card {
        background: #000000;
        padding: 40px;
        /* جعل الحواف العلوية مربعة والسفلية دائرية للاندماج مع السقف */
        border-radius: 0px 0px 40px 40px; 
        border: 4px solid #f59e0b;
        border-top: none; /* إزالة الحد العلوي للالتصاق التام */
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
        text-align: center;
        width: 100%;
        max-width: 500px;
    }

    .login-card h1 { color: #f59e0b; font-weight: 900; font-size: 2.8rem; margin-bottom: 5px; }
    .login-card p { color: #fff; margin-bottom: 30px; opacity: 0.9; }

    /* ستايل المدخلات */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: #f59e0b !important;
        border: 2px solid #333 !important;
        border-radius: 12px !important;
        text-align: center;
        font-size: 1.2rem !important;
        height: 60px !important;
    }

    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 55px !important;
    }

    /* زر الدخول الذهبي */
    .login-card div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        border: none !important;
    }

    /* زر الخروج العائم */
    .logout-box { position: fixed; top: 10px; right: 10px; z-index: 999; }
    </style>
""", unsafe_allow_html=True)

# 3. نظام التحقق
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_screen():
    st.markdown('<div class="top-zero-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1>معلوماتى</h1>', unsafe_allow_html=True)
        st.markdown('<p>سجل دخولك للوصول إلى قاعدة البيانات</p>', unsafe_allow_html=True)
        
        pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل الرمز السرّي", label_visibility="collapsed")
        
        if st.button("دخول آمن للمنصة 🔓"):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("خطأ في كلمة المرور")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# تفعيل الحماية
if not st.session_state.auth:
    login_screen()
    st.stop()

# --- محتوى المنصة بعد الدخول ---
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"):
    st.session_state.auth = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Hero Banner للمنصة
st.markdown('<div style="margin-top:30px;"></div>', unsafe_allow_html=True) 
st.markdown('<div class="hero-banner" style="background:#000; color:#f59e0b; padding:25px; border-radius:20px; text-align:center; border:4px solid #f59e0b; box-shadow: 10px 10px 0px #000;"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
