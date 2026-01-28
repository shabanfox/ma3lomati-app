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

# --- إدارة الحالة والاستقرار (بما في ذلك الثيم) ---
params = st.query_params
if 'auth' not in st.session_state:
    if params.get("logged_in") == "true":
        st.session_state.auth = True
        st.session_state.current_user = params.get("user", "User")
    else:
        st.session_state.auth = False

# إضافة حالة الثيم (افتراضي داكن)
if 'theme' not in st.session_state:
    st.session_state.theme = params.get("theme", "dark")

if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- وظائف الاستقرار ---
def set_login_state(user_name):
    st.session_state.auth = True
    st.session_state.current_user = user_name
    st.query_params["logged_in"] = "true"
    st.query_params["user"] = user_name
    st.query_params["theme"] = st.session_state.theme

def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

# --- 3. تحديد الألوان بناءً على الثيم ---
if st.session_state.theme == "light":
    bg_color = "rgba(255, 255, 255, 0.95)"
    text_color = "#111111"
    card_bg = "#f0f2f6"
    card_text = "#333333"
    border_color = "#dddddd"
    main_bg_overlay = "rgba(255,255,255,0.85)"
else:
    bg_color = "rgba(0,0,0,0.96)"
    text_color = "#ffffff"
    card_bg = "rgba(20, 20, 20, 0.9)"
    card_text = "#ffffff"
    border_color = "#333333"
    main_bg_overlay = "rgba(0,0,0,0.96)"

# --- 5. التصميم الجمالي CSS المحدث ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient({main_bg_overlay}, {main_bg_overlay}), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
        color: {text_color};
    }}

    /* Auth Styling */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); color: #000; }}
    
    /* Content Cards */
    .detail-card, .tool-card {{ 
        background: {card_bg}; 
        padding: 25px; border-radius: 20px; 
        border-top: 5px solid #f59e0b; 
        color: {card_text}; 
        border: 1px solid {border_color}; 
        margin-bottom:20px; 
    }}
    
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 10px; }}
    .val-white {{ color: {card_text}; font-size: 18px; border-bottom: 1px solid {border_color}; padding-bottom:5px; margin-bottom: 10px; }}

    /* Ticker */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid {border_color}; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    
    /* Buttons */
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: 1px solid #ddd !important; display: block !important; width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    # (كود الدخول يظل كما هو في ردك السابق مع استخدام set_login_state)
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    with tab_login:
        u_input = st.text_input("User", placeholder="الأسم أو الجيميل", label_visibility="collapsed", key="log_user")
        p_input = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="log_pass")
        if st.button("SIGN IN 🚀", use_container_width=True):
            if p_input == "2026": 
                set_login_state("Admin")
                st.rerun()
            # ... (هنا يوضع كود التحقق من جوجل شيت)
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- زر تبديل الثيم والخروج ---
col_theme, col_user, col_logout = st.columns([0.2, 0.6, 0.2])
with col_theme:
    current_theme = "🌙 الداكن" if st.session_state.theme == "dark" else "☀️ الفاتح"
    if st.button(f"الوضع: {current_theme}", use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.query_params["theme"] = st.session_state.theme
        st.rerun()

with col_logout:
    if st.button("🚪 خروج", use_container_width=True): logout()

# --- 8. الهيدر الداخلي ---
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

# (بقية كود القائمة والمشاريع والأدوات يظل كما هو تماماً، سيقوم الـ CSS الجديد بتغيير ألوانه تلقائياً)
# ...

