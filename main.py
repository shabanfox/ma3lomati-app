import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة (يجب أن يكون أول أمر من أوامر streamlit)
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي المطور (الأسود والذهبي الفخم)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    /* العناوين الذهبية */
    h1, h2, h3, h4 {{ color: #f59e0b !important; font-weight: 900 !important; }}
    p, span, label {{ color: #eeeeee !important; font-weight: bold; }}

    /* كروت المشاريع الاحترافية (خلفية داكنة بحد ذهبي) */
    div.stButton > button[key*="card_"], div.stButton > button[key*="ready_"] {{
        background-color: #1a1a1a !important; 
        color: #ffffff !important;
        min-height: 140px !important; 
        text-align: right !important;
        font-weight: 700 !important; 
        font-size: 16px !important;
        border: 1px solid #333 !important; 
        border-right: 6px solid #f59e0b !important;
        margin-bottom: 15px !important;
        width: 100% !important;
        transition: 0.4s all ease !important;
    }}
    
    div.stButton > button:hover {{ 
        background-color: #222 !important;
        transform: translateY(-5px) !important; 
        border-color: #f59e0b !important;
        box-shadow: 0 10px 20px rgba(245,158,11,0.2) !important;
    }}

    .smart-box {{ 
        background: #111; 
        border: 1px solid #222; 
        padding: 25px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b; 
    }}

    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; }}
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الحالة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# --- الوظائف الأساسية ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            for u in response.json():
                n, p, e = str(u.get('Name','')), str(u.get('Password','')), str(u.get('Email',''))
                if (user_input.strip().lower() in [n.lower(), e.lower()]) and str(pwd_input) == p:
                    return n
        return None
    except: return None

@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        p.rename(columns={'Area':'Location','الموقع':'Location','Project Name':'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

# 4. نظام الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; padding-top:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u_in = st.text_input("الأسم أو الجيميل")
    p_in = st.text_input("كلمة السر", type="password")
    if st.button("دخول للمنصة 🚀"):
        if p_in == "2026":
            st.session_state.auth, st.session_state.current_user = True, "Admin"
            st.rerun()
        else:
            user = login_user(u_in, p_in)
            if user:
                st.session_state.auth, st.session_state.current_user = True, user
                st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# 5. عرض التطبيق بعد الدخول
df_p, df_d = load_data()

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.selected_item = None
        st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><p>📍 الموقع: {item.get('Location')}</p><p>🏗️ المطور: {item.get('Developer')}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i, r in dff.head(10).iterrows():
        if st.button(f"🏢 {r['ProjectName']}\n📍 {r['Location']}\n🏗️ {r['Developer']}", key=f"card_p_{i}"):
            st.session_state.selected_item = r
            st.rerun()

# باقي الأقسام تتبع نفس الهيكل...
