import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS - تحديث مكان الكارت وتوسيطه
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #f8f9fa; /* لون خلفية هادئ */
    }

    /* --- حاوية التوسيط المطلق لكارت الدخول --- */
    .main-login-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 85vh; /* يضمن التوسط الرأسي */
        width: 100%;
    }

    .login-card {
        background: #000000;
        padding: 60px 40px;
        border-radius: 40px;
        border: 4px solid #f59e0b;
        box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.4);
        text-align: center;
        width: 100%;
        max-width: 480px;
    }
    
    .login-card h1 { color: #f59e0b; font-weight: 900; font-size: 3.2rem; margin-bottom: 10px; }
    .login-card p { color: #fff; font-size: 1.2rem; margin-bottom: 35px; opacity: 0.8; }

    /* زر الخروج العائم */
    .logout-box { position: fixed; top: 20px; right: 20px; z-index: 9999; }

    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 55px !important;
        width: 100% !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }

    /* زر الدخول الذهبي */
    .login-card div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        border: none !important;
    }

    /* حقل كلمة المرور */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: #f59e0b !important;
        border: 2px solid #333 !important;
        border-radius: 15px !important;
        text-align: center;
        font-size: 1.3rem !important;
        height: 65px !important;
        margin-bottom: 10px;
    }
    
    /* ستايلات المنصة بعد الدخول */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000; margin-top: 60px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام التحقق من الهوية
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_screen():
    # استخدام حاوية التغليف لضمان التوسيط
    st.markdown('<div class="main-login-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1>معلوماتى</h1>', unsafe_allow_html=True)
        st.markdown('<p>المنصة العقارية الأكثر دقة</p>', unsafe_allow_html=True)
        
        pwd = st.text_input("كلمة المرور", type="password", placeholder="رمز الدخول", label_visibility="collapsed")
        
        if st.button("دخول آمن للمنصة 🔒"):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# التحقق من الحالة
if not st.session_state.auth:
    login_screen()
    st.stop()

# --- محتوى المنصة بعد الدخول ---
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"):
    st.session_state.auth = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# باقي كود المنصة (Main, Comp, Tools) يوضع هنا...
st.markdown('<div class="hero-banner"><h1>🏠 مرحباً بك في منصة معلوماتى</h1></div>', unsafe_allow_html=True)

# أزرار التنقل الرئيسية
c1, c2 = st.columns(2)
with c1:
    if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
        st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
with c2:
    if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
        st.session_state.view = 'tools'; st.rerun()
