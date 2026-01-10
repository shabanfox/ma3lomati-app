import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي مخصص لطلبك
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f6; 
    }

    /* حاوية التوسيط الكامل */
    .main-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 90vh;
        width: 100%;
    }

    /* كارت الدخول البيضاوي */
    .oval-card {
        background: #000000;
        padding: 60px 50px;
        border-radius: 100px; /* جعل الشكل بيضاوي */
        border: 5px solid #f59e0b; /* فريم ذهبي */
        box-shadow: 0px 15px 50px rgba(0,0,0,0.5);
        text-align: center;
        width: 100%;
        max-width: 550px;
        color: white;
    }

    .oval-card h1 {
        color: #f59e0b;
        font-weight: 900;
        font-size: 2.2rem;
        margin-bottom: 20px;
    }

    /* رمز القفل الذهبي */
    .lock-icon {
        font-size: 50px;
        color: #f59e0b;
        margin-bottom: 15px;
    }

    /* ستايل حقل الباسورد (نص أسود على خلفية بيضاء) */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 3px solid #f59e0b !important;
        border-radius: 50px !important;
        text-align: center;
        font-size: 1.2rem !important;
        height: 55px !important;
        font-weight: bold;
    }

    /* ستايل زر الدخول */
    div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        border: 2px solid #000 !important;
        border-radius: 50px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        width: 100% !important;
        height: 55px !important;
        margin-top: 15px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #ffffff !important;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام التحقق
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_screen():
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="oval-card">', unsafe_allow_html=True)
        
        # رمز القفل الذهبي (باستخدام Emoji أو يمكنك وضع رابط صورة)
        st.markdown('<div class="lock-icon">🔒</div>', unsafe_allow_html=True)
        
        st.markdown('<h1>منصة معلوماتي العقارية</h1>', unsafe_allow_html=True)
        
        # حقل كلمة المرور
        pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور هنا", label_visibility="collapsed")
        
        # زر الدخول
        if st.button("دخول"):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("⚠️ كلمة المرور غير صحيحة")
                
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# تشغيل صفحة الدخول
if not st.session_state.auth:
    login_screen()
    st.stop()

# --- محتوى المنصة (يظهر بعد الدخول الصحيح) ---
st.success("تم تسجيل الدخول بنجاح")
if st.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
