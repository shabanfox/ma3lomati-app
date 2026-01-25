import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"

# --- 4. وظائف الدخول ---
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if res.status_code == 200:
            users = res.json()
            u, p = str(u).strip().lower(), str(p).strip()
            for user in users:
                name = str(user.get('Name', user.get('name', ''))).strip()
                email = str(user.get('Email', user.get('email', ''))).strip()
                pwd = str(user.get('Password', user.get('password', ''))).strip()
                if (u == name.lower() or u == email.lower()) and p == pwd:
                    return name
        return None
    except: return None

# --- 5. التصميم الجمالي للهاتف (ألوان واضحة + منع Scroll) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"], [data-testid="stFooter"] {{ visibility: hidden; display: none; }}
    
    /* منع التمرير نهائياً وجعل الصفحة ثابتة للهاتف */
    html, body, [data-testid="stAppViewContainer"] {{
        overflow: hidden !important;
        height: 100vh !important;
        background-color: #000000 !important;
    }}

    .block-container {{ padding: 0rem !important; }}

    [data-testid="stAppViewContainer"] {{
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تسجيل الدخول في قمة الصفحة */
    .auth-container {{
        display: flex; flex-direction: column; align-items: center;
        padding-top: 15px; width: 100%;
    }}

    .login-card {{
        background: #111111;
        border: 2px solid #f59e0b;
        border-radius: 20px;
        padding: 30px 20px;
        width: 92%;
        max-width: 400px;
        text-align: center;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.3);
    }}

    .title-text {{
        color: #f59e0b; font-size: 30px; font-weight: 900; margin-bottom: 5px;
    }}

    /* حقول الإدخال - تباين عالي جداً (أبيض وأسود) */
    div.stTextInput input {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-align: center !important;
    }}

    /* الأزرار - كبيرة وواضحة */
    .stButton > button {{
        background: #f59e0b !important;
        color: #000000 !important;
        font-weight: 900 !important;
        height: 55px !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        width: 100% !important;
        border: none !important;
    }}

    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] {{ border: none; }}
    .stTabs [data-baseweb="tab"] {{
        color: #888 !important; padding: 10px 20px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important; border-bottom: 3px solid #f59e0b !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. واجهة تسجيل الدخول ---
if not st.session_state.auth:
    # شريط اللغة العلوي
    c1, c2, c3 = st.columns([0.1, 0.6, 0.3])
    with c3:
        lang_sel = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        if (lang_sel == "العربية" and st.session_state.lang == "English") or (lang_sel == "English" and st.session_state.lang == "Arabic"):
            st.session_state.lang = "Arabic" if lang_sel == "العربية" else "English"
            st.rerun()

    # الكارت المرفوع للأعلى
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""
            <div class="login-card">
                <div class="title-text">MA3LOMATI</div>
                <p style="color:white; margin-bottom:20px; opacity:0.8;">{"نظام العقارات لعام 2026" if st.session_state.lang=="Arabic" else "Real Estate System 2026"}</p>
        """, unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["🔐 دخول" if st.session_state.lang=="Arabic" else "🔐 Login", 
                                     "📝 اشتراك" if st.session_state.lang=="Arabic" else "📝 Sign"])
        
        with tab_log:
            u = st.text_input("U", key="user_field", placeholder="Username", label_visibility="collapsed")
            p = st.text_input("P", type="password", key="pass_field", placeholder="Password", label_visibility="collapsed")
            if st.button("LOG IN NOW"):
                if p == "2026":
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    res_user = login_user(u, p)
                    if res_user:
                        st.session_state.auth = True; st.session_state.current_user = res_user; st.rerun()
                    else: st.error("خطأ" if st.session_state.lang=="Arabic" else "Error")
        
        with tab_reg:
            st.markdown("<p style='color:white; font-size:12px;'>تواصل مع الإدارة للحصول على صلاحية</p>", unsafe_allow_html=True)
            st.text_input("Name", placeholder="الأسم")
            st.button("Request Account")
            
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. المحتوى الداخلي ---
st.markdown(f"<h1 style='color:white; text-align:center; margin-top:50px;'>Welcome {st.session_state.current_user}</h1>", unsafe_allow_html=True)
if st.button("Logout"):
    st.session_state.auth = False
    st.rerun()
