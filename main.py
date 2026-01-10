import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي مخصص (بدون فراغ علوي + شكل بيضاوي خلف العنوان)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء العناصر الافتراضية وتصفير المسافات */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child {
        padding-top: 0rem !important;
    }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #ffffff;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* حاوية الدخول الرئيسية */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; /* تبدأ من أعلى الصفحة */
        min-height: 100vh;
        width: 100%;
    }

    /* الشكل البيضاوي الأسود خلف جملة العنوان */
    .hero-oval {
        background: #000000;
        border: 4px solid #f59e0b; /* فريم ذهبي */
        padding: 40px 80px;
        border-radius: 0px 0px 300px 300px; /* شكل بيضاوي منسدل */
        text-align: center;
        width: 100%;
        max-width: 700px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 40px;
    }

    .hero-oval h1 {
        color: #f59e0b;
        font-weight: 900;
        font-size: 2.5rem;
        margin: 0;
    }

    /* رمز القفل الذهبي */
    .gold-lock {
        font-size: 60px;
        color: #f59e0b;
        margin-bottom: 20px;
        text-shadow: 0px 0px 10px rgba(245, 158, 11, 0.5);
    }

    /* حاوية مدخلات الدخول */
    .login-box {
        width: 100%;
        max-width: 400px;
        text-align: center;
        padding: 20px;
    }

    /* ستايل حقل الباسورد (مكان الكتابة أسود على خلفية بيضاء) */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        border-radius: 15px !important;
        text-align: center;
        font-size: 1.2rem !important;
        height: 55px !important;
        font-weight: 700;
        box-shadow: 4px 4px 0px #f59e0b !important;
    }

    /* زر الدخول */
    div.stButton > button {
        background-color: #000000 !important;
        color: #f59e0b !important;
        border: 3px solid #f59e0b !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        width: 100% !important;
        height: 60px !important;
        margin-top: 20px;
        box-shadow: 6px 6px 0px #000 !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translate(-3px, -3px);
        box-shadow: 8px 8px 0px #f59e0b !important;
        background-color: #f59e0b !important;
        color: #000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام التحقق
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_page():
    # عرض صفحة الدخول
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # الجزء العلوي: الشكل البيضاوي الأسود خلف الجملة
    st.markdown("""
        <div class="hero-oval">
            <h1>منصة معلوماتي العقارية</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # الجزء الأوسط: رمز القفل والمدخلات
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="gold-lock">🔒</div>', unsafe_allow_html=True)
    
    pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور هنا", label_visibility="collapsed")
    
    if st.button("دخول"):
        if pwd == "Ma3lomati_2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("⚠️ الرمز السري غير صحيح")
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# تفعيل الحماية
if not st.session_state.auth:
    login_page()
    st.stop()

# --- محتوى المنصة بعد الدخول ---
st.markdown('<div style="padding:20px; text-align:center;"><h2>مرحباً بك في المنصة</h2></div>', unsafe_allow_html=True)
if st.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
