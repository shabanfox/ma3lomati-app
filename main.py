import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (معدل للمحاذاة العلوية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* حاوية ترفع الكارت لأعلى الصفحة */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: flex-start; /* المحاذاة للأعلى */
        padding-top: 40px;      /* مسافة بسيطة من السقف */
        height: 100vh;
        width: 100%;
    }

    .login-card {
        background: #000000;
        padding: 40px;
        border-radius: 30px;
        border: 4px solid #f59e0b;
        box-shadow: 15px 15px 0px rgba(0,0,0,0.1);
        text-align: center;
        width: 100%;
        max-width: 450px;
    }

    .login-card h1 { color: #f59e0b; font-weight: 900; font-size: 2.5rem; margin-bottom: 5px; }
    .login-card p { color: #fff; margin-bottom: 25px; opacity: 0.8; }

    /* ستايل مدخل كلمة المرور */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: #f59e0b !important;
        border: 2px solid #333 !important;
        border-radius: 12px !important;
        text-align: center;
        font-size: 1.2rem !important;
        height: 55px !important;
    }

    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 50px !important;
    }

    /* زر الدخول الذهبي */
    .login-card div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        border: none !important;
        width: 100% !important;
    }

    /* زر الخروج العائم */
    .logout-box { position: fixed; top: 15px; right: 15px; z-index: 999; }
    </style>
""", unsafe_allow_html=True)

# 3. نظام التحقق
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_screen():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1>معلوماتى</h1>', unsafe_allow_html=True)
        st.markdown('<p>سجل دخولك للوصول إلى قاعدة البيانات</p>', unsafe_allow_html=True)
        
        pwd = st.text_input("كلمة المرور", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        if st.button("دخول آمن 🔓"):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# تفعيل الحماية
if not st.session_state.auth:
    login_screen()
    st.stop()

# --- محتوى المنصة (يظهر بعد الدخول) ---
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"):
    st.session_state.auth = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# هنا تكملة كود المنصة الرئيسي الخاص بك (Hero Banner, Buttons, etc.)
st.markdown('<div style="margin-top:80px;"></div>', unsafe_allow_html=True) # تعويض مساحة زر الخروج
st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
