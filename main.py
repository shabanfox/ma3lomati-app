import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"

# --- 4. الوظائف البرمجية ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            pwd_input = str(pwd_input).strip()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower() or user_input == email_s.lower()) and pwd_input == pass_s:
                    return name_s
        return None
    except: return None

def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

# --- 5. التصميم الجمالي CSS (تركيز على وضع الكارت في القمة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر الافتراضي وتقليل المسافات */
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; padding-bottom: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تسجيل الدخول تبدأ من أعلى الصفحة تماماً */
    .auth-top-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; /* تبدأ من القمة */
        padding-top: 20px !important; /* مسافة بسيطة جداً من الحافة العلوية */
        min-height: 100vh;
    }}

    .luxury-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 30px;
        padding: 40px;
        width: 95%;
        max-width: 450px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.5);
        text-align: center;
    }}

    .gold-title {{
        background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 5px;
    }}

    /* تنسيق المدخلات */
    div.stTextInput input {{
        background: rgba(0,0,0,0.4) !important;
        color: white !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-radius: 12px !important;
        height: 48px !important;
        text-align: center !important;
    }}

    /* تنسيق الأزرار */
    .stButton > button {{
        background: linear-gradient(45deg, #f59e0b, #d97706) !important;
        color: black !important;
        font-weight: 900 !important;
        height: 48px !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        margin-top: 10px;
    }}

    /* شريط اللغة العلوي */
    .lang-bar {{
        width: 100%;
        display: flex;
        justify-content: flex-end;
        padding: 10px 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. واجهة تسجيل الدخول (في بداية الصفحة) ---
if not st.session_state.auth:
    # 1. زر اللغة في أقصى الزاوية العلوية
    c_lang = st.columns([0.85, 0.15])
    with c_lang[1]:
        lang_choice = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        st.session_state.lang = "Arabic" if lang_choice == "العربية" else "English"

    # 2. الكارت يبدأ فوراً بعد شريط اللغة
    st.markdown('<div class="auth-top-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""
            <div class="luxury-card">
                <div class="gold-title">MA3LOMATI PRO</div>
                <p style="color:#aaa; font-size:14px;">{"بوابتك الذكية للعقارات 2026" if st.session_state.lang=="Arabic" else "Smart Real Estate Portal 2026"}</p>
        """, unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["🔐 دخول" if st.session_state.lang=="Arabic" else "🔐 Login", 
                                     "📝 اشتراك" if st.session_state.lang=="Arabic" else "📝 Signup"])
        
        with tab_log:
            u = st.text_input("User", key="u_log", placeholder="الإيميل أو المستخدم", label_visibility="collapsed")
            p = st.text_input("Pass", type="password", key="p_log", placeholder="كلمة المرور", label_visibility="collapsed")
            if st.button("SIGN IN"):
                if p == "2026":
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    user_verified = login_user(u, p)
                    if user_verified:
                        st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                    else: st.error("خطأ في البيانات")
        
        with tab_reg:
            rn = st.text_input("Full Name", placeholder="الاسم")
            re = st.text_input("Email", placeholder="البريد")
            rw = st.text_input("WhatsApp", placeholder="واتساب")
            rp = st.text_input("Password", type="password", placeholder="كلمة المرور", key="p_reg")
            if st.button("CREATE ACCOUNT"):
                if signup_user(rn, rp, re, rw, "Company"): st.success("تم بنجاح")
                else: st.error("فشل")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. الموقع من الداخل (يظهر بعد تسجيل الدخول) ---
st.sidebar.title(f"مرحباً {st.session_state.current_user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

st.title("لوحة تحكم معلوماتي برو")
st.write("أهلاً بك في النسخة الاحترافية، يمكنك الآن الوصول لكافة البيانات.")

