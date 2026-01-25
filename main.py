import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة (أهم خطوة لمنع السكرول) ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الثوابت ---
MAIN_COLOR = "#00d4ff" # لون لبني نيون هادي
BG_IMAGE = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- 4. CSS الاحترافي (بدون سكرول نهائياً في الدخول) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* إخفاء الهيدر والمارجن الافتراضي */
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
    .block-container {{ padding: 0 !important; }}
    
    /* تثبيت الشاشة في صفحة الدخول */
    {'''
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh !important;
        margin: 0; padding: 0;
    }
    ''' if not st.session_state.auth else ""}

    /* الخلفية */
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تسجيل الدخول (مركزية تماماً) */
    .login-wrapper {{
        display: flex; justify-content: center; align-items: center;
        height: 100vh; width: 100vw;
        background: url('{BG_IMAGE}') no-repeat center center/cover;
    }}
    
    .login-card {{
        background: rgba(15, 15, 15, 0.85);
        backdrop-filter: blur(20px);
        padding: 40px; border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: 380px; text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }}

    /* تنسيق المدخلات */
    div.stTextInput input {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important; border-radius: 12px !important;
        height: 45px !important; font-size: 15px !important;
        transition: 0.3s;
    }}
    div.stTextInput input:focus {{ border-color: {MAIN_COLOR} !important; }}

    /* أزرار مودرن */
    .stButton > button {{
        background: {MAIN_COLOR} !important;
        color: black !important; font-weight: 700 !important;
        border-radius: 12px !important; height: 48px !important;
        width: 100% !important; border: none !important;
        margin-top: 10px;
    }}
    
    /* التابس (الدخول/الاشتراك) */
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; justify-content: center; }}
    .stTabs [data-baseweb="tab"] {{ color: #888 !important; }}
    .stTabs [aria-selected="true"] {{ color: {MAIN_COLOR} !important; border-bottom-color: {MAIN_COLOR} !important; }}

    /* الهيدر الداخلي */
    .app-header {{
        padding: 20px; background: rgba(0,0,0,0.4);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        text-align: center;
    }}
    
    /* الكروت الداخلية */
    .project-card {{
        background: #151515; border: 1px solid #252525;
        border-radius: 16px; padding: 20px; margin-bottom: 15px;
        transition: 0.3s;
    }}
    .project-card:hover {{ border-color: {MAIN_COLOR}; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. واجهة تسجيل الدخول ---
if not st.session_state.auth:
    # استخدام HTML لعمل Wrapper كامل للشاشة
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color:white; margin-bottom:5px;">MA3LOMATI <span style="color:{MAIN_COLOR}">PRO</span></h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#666; font-size:13px; margin-bottom:30px;">Premium Real Estate Portal</p>', unsafe_allow_html=True)
        
        t1, t2 = st.tabs(["Login", "Sign Up"])
        with t1:
            u = st.text_input("Email/User", key="user", placeholder="username", label_visibility="collapsed")
            p = st.text_input("Pass", type="password", key="pass", placeholder="password", label_visibility="collapsed")
            if st.button("SIGN IN"):
                if p == "2026": 
                    st.session_state.auth = True
                    st.session_state.current_user = u if u else "Admin"
                    st.rerun()
                else: st.error("Wrong Password")
        with t2:
            st.text_input("Full Name", placeholder="Enter your name", label_visibility="collapsed")
            st.text_input("WhatsApp", placeholder="01xxxxxxxxx", label_visibility="collapsed")
            if st.button("CREATE ACCOUNT"): st.info("Under Review")
            
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 6. الواجهة الداخلية (بعد الدخول) ---
# هنا يبدأ السكرول مسموح عادي عشان البيانات
st.markdown(f"""
    <div class="app-header">
        <h3 style="margin:0; color:white;">Dashboard</h3>
        <p style="margin:0; font-size:12px; color:{MAIN_COLOR};">Welcome, {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["Home", "Projects", "Tools", "Support"], 
    icons=["house", "building", "calculator", "headset"], 
    default_index=1, orientation="horizontal",
    styles={
        "container": {"background-color": "transparent"},
        "nav-link-selected": {"background-color": MAIN_COLOR, "color": "black"}
    })

# عينة بيانات للتجربة
if menu == "Projects":
    st.write("### New Launches")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="project-card"><h4 style="color:{MAIN_COLOR}">New Capital Compound</h4><p>Starting from 4,000,000 EGP</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="project-card"><h4 style="color:{MAIN_COLOR}">North Coast Villa</h4><p>Direct on Sea - Limited Units</p></div>', unsafe_allow_html=True)

if st.button("Logout"):
    st.session_state.auth = False
    st.rerun()

