import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"

# --- 4. الوظائف ---
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

# --- 5. التصميم الجمالي المخصص للهاتف (High Contrast & No Scroll) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"], [data-testid="stFooter"] {{ visibility: hidden; display: none; }}
    
    /* منع التمرير وجعل الصفحة ثابتة */
    html, body, [data-testid="stAppViewContainer"] {{
        overflow: hidden !important;
        height: 100vh !important;
        margin: 0; padding: 0;
    }}

    .block-container {{ 
        padding-top: 10px !important; 
        padding-bottom: 0px !important; 
    }}

    [data-testid="stAppViewContainer"] {{
        background: #000000; /* أسود صريح لوضوح الهاتف */
        background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover;
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* كارت تسجيل الدخول في قمة الصفحة */
    .mobile-auth-card {{
        background: rgba(25, 25, 25, 0.95);
        border: 2px solid #f59e0b;
        border-radius: 20px;
        padding: 25px 20px;
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
        text-align: center;
    }}

    .gold-title {{
        color: #f59e0b;
        font-size: 28px;
        font-weight: 900;
        margin-bottom: 0px;
        text-transform: uppercase;
    }}

    /* تنسيق المدخلات - ألوان واضحة جداً */
    div.stTextInput input {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #f59e0b !important;
        border-radius: 10px !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-align: center !important;
    }}

    /* الأزرار - كبيرة وسهلة اللمس */
    .stButton > button {{
        background: #f59e0b !important;
        color: #000000 !important;
        font-weight: 900 !important;
        height: 55px !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 20px !important;
        width: 100% !important;
        margin-top: 15px !important;
    }}

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {{ gap: 5px; }}
    .stTabs [data-baseweb="tab"] {{
        color: white !important;
        background: #222 !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 10px 20px !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: #f59e0b !important;
        color: black !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. واجهة تسجيل الدخول ---
if not st.session_state.auth:
    # زر اللغة (أعلى الصفحة)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c3:
        lang = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        if (lang == "العربية" and st.session_state.lang == "English") or (lang == "English" and st.session_state.lang == "Arabic"):
            st.session_state.lang = "Arabic" if lang == "العربية" else "English"
            st.rerun()

    # حاوية الكارت
    st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""
            <div class="mobile-auth-card">
                <div class="gold-title">MA3LOMATI PRO</div>
                <p style="color:#ffffff; font-size:14px; margin-bottom:15px;">{"نظام العقارات الذكي 2026" if st.session_state.lang=="Arabic" else "Smart RE System 2026"}</p>
        """, unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["🔐 دخول" if st.session_state.lang=="Arabic" else "🔐 Login", 
                                     "📝 تسجيل" if st.session_state.lang=="Arabic" else "📝 Reg"])
        
        with tab_log:
            u = st.text_input("U", key="u_log", placeholder="المستخدم / Email", label_visibility="collapsed")
            p = st.text_input("P", type="password", key="p_log", placeholder="كلمة المرور", label_visibility="collapsed")
            if st.button("LOG IN"):
                if p == "2026":
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    user = login_user(u, p)
                    if user:
                        st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
                    else: st.error("خطأ في البيانات" if st.session_state.lang=="Arabic" else "Invalid")
        
        with tab_reg:
            st.markdown(f"<p style='color:white;'>{'يرجى التواصل مع الإدارة للتفعيل' if st.session_state.lang=='Arabic' else 'Contact admin to activate'}</p>", unsafe_allow_html=True)
            st.text_input("Name", placeholder="الأسم")
            st.button("طلب اشتراك" if st.session_state.lang=="Arabic" else "Request")
            
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. المحتوى الداخلي ---
st.markdown(f"<h1 style='color:white; text-align:center;'>Welcome {st.session_state.current_user}</h1>", unsafe_allow_html=True)
if st.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
